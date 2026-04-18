import argparse
import logging
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from google import genai
from google.api_core.exceptions import PermissionDenied
from google.genai import types


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_MODEL = "imagen-4.0-generate-001"
DEFAULT_TEXT_MODEL = "gemini-3-flash-preview"
DEFAULT_LOCATION = "global"
DEFAULT_PROMPTS_FILE = SCRIPT_DIR / "PROMPTS.md"
DEFAULT_TEMPLATE_FILE = SCRIPT_DIR / "PROMPT_GENERATOR_TEMPLATE.md"
SCARY_TEMPLATE_FILE = SCRIPT_DIR / "PROMPT_GENERATOR_TEMPLATE_SCARY.md"
TEMPLATE_PLACEHOLDER = "[PASTE YOUR WORDS OR EXPRESSIONS HERE]"
PROMPT_LINE_RE = re.compile(
    r"^\s*(\d+)\.\s+\*\*([^:*]+?)(?::\*\*|\*\*:)\s+(.+?)\s*$"
)


@dataclass(frozen=True)
class PromptSpec:
    title_slug: str
    prompt_text: str
    display_title: str


@dataclass(frozen=True)
class TemplateOption:
    option_id: str
    label: str
    description: str
    template_path: Path
    aliases: tuple[str, ...] = ()


TEMPLATE_OPTIONS: tuple[TemplateOption, ...] = (
    TemplateOption(
        option_id="1",
        label="Kids ESL",
        description="bright, friendly, colorful scenes",
        template_path=DEFAULT_TEMPLATE_FILE,
        aliases=("kids", "friendly", "bright"),
    ),
    TemplateOption(
        option_id="2",
        label="Halloween Dark",
        description="spooky, eerie, cinematic scenes",
        template_path=SCARY_TEMPLATE_FILE,
        aliases=("dark", "scary", "halloween", "spooky"),
    ),
)
TEMPLATE_LOOKUP: dict[str, TemplateOption] = {
    key: option
    for option in TEMPLATE_OPTIONS
    for key in (option.option_id, *option.aliases)
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read prompts from a Markdown file and generate one image per prompt."
    )
    parser.add_argument(
        "--prompts-file",
        default=DEFAULT_PROMPTS_FILE,
        help=f"Markdown file with prompts. Default: {DEFAULT_PROMPTS_FILE}",
    )
    parser.add_argument(
        "--output-dir",
        default="generated_images",
        help="Directory where generated images will be saved.",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Image generation model. Default: {DEFAULT_MODEL}",
    )
    parser.add_argument(
        "--aspect-ratio",
        default="1:1",
        help="Aspect ratio for generated images. Default: 1:1",
    )
    parser.add_argument(
        "--image-size",
        default="1K",
        help="Output image size. Default: 1K",
    )
    parser.add_argument(
        "--output-mime-type",
        default="image/jpeg",
        help="Output mime type. Default: image/jpeg",
    )
    parser.add_argument(
        "--images-per-prompt",
        type=int,
        default=1,
        help="Number of images to generate for each prompt. Default: 1",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run the script in interactive mode.",
    )
    return parser.parse_args()


def sanitize_slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return slug or "prompt"


def resolve_path(path_value: str | Path) -> Path:
    return Path(path_value).expanduser().resolve()


def parse_prompt_line(line: str) -> PromptSpec | None:
    match = PROMPT_LINE_RE.match(line.strip())
    if not match:
        return None

    title = match.group(2).strip()
    prompt_text = match.group(3).strip()
    if not prompt_text:
        return None

    return PromptSpec(
        title_slug=sanitize_slug(title),
        prompt_text=prompt_text,
        display_title=title,
    )


def parse_prompt_text(prompt_text: str, source_label: str) -> list[PromptSpec]:
    prompts: list[PromptSpec] = []
    for raw_line in prompt_text.splitlines():
        parsed = parse_prompt_line(raw_line)
        if parsed is not None:
            prompts.append(parsed)

    if not prompts:
        raise ValueError(f"No prompts found in {source_label}")

    return prompts


def parse_prompts_file(prompts_file: Path) -> list[PromptSpec]:
    prompts_path = resolve_path(prompts_file)
    if not prompts_path.exists():
        raise FileNotFoundError(f"Prompts file not found: {prompts_path}")

    return parse_prompt_text(
        prompts_path.read_text(encoding="utf-8"),
        str(prompts_path),
    )


def parse_keywords(words_input: str) -> list[str]:
    keywords = [word.strip() for word in words_input.split(",") if word.strip()]
    if not keywords:
        raise ValueError("No valid keywords were provided.")
    return keywords


def load_prompt_template(template_file: Path = DEFAULT_TEMPLATE_FILE) -> str:
    template_path = resolve_path(template_file)
    if not template_path.exists():
        raise FileNotFoundError(f"Template file not found: {template_path}")

    template = template_path.read_text(encoding="utf-8")
    if TEMPLATE_PLACEHOLDER not in template:
        raise ValueError(
            f"Template placeholder {TEMPLATE_PLACEHOLDER!r} was not found in {template_path}"
        )
    return template


def render_prompt_template(template: str, keywords: list[str]) -> str:
    rendered_items = "\n".join(f"- {keyword}" for keyword in keywords)
    return template.replace(TEMPLATE_PLACEHOLDER, rendered_items, 1)


def choose_template_file() -> Path:
    print("Choose a prompt style:")
    for option in TEMPLATE_OPTIONS:
        print(f"  {option.option_id}. {option.label} - {option.description}")

    selected = input("Template (1/2, default 1): ").strip().lower() or "1"
    option = TEMPLATE_LOOKUP.get(selected)
    if option is None:
        raise ValueError("Invalid template selection. Choose 1 or 2.")

    logging.info("Using template %s: %s", option.option_id, option.label)
    return option.template_path


def build_client() -> genai.Client:
    use_vertex = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "").strip().lower()
    if use_vertex != "true":
        raise RuntimeError(
            "Vertex AI mode is required. Set GOOGLE_GENAI_USE_VERTEXAI=true."
        )

    project = os.getenv("GOOGLE_CLOUD_PROJECT", "").strip()
    if not project:
        raise RuntimeError(
            "GOOGLE_CLOUD_PROJECT is required for Vertex AI authentication."
        )

    location = os.getenv("GOOGLE_CLOUD_LOCATION", "").strip() or DEFAULT_LOCATION
    return genai.Client(vertexai=True, project=project, location=location)


def generate_prompt_batch(client: genai.Client, rendered_template: str) -> str:
    logging.info("Using '%s' to generate rich prompts from keywords.", DEFAULT_TEXT_MODEL)
    response = client.models.generate_content(
        model=DEFAULT_TEXT_MODEL,
        contents=rendered_template,
    )

    generated_text = (response.text or "").strip()
    if not generated_text:
        raise RuntimeError("The text model returned an empty prompt batch.")

    return generated_text


def generate_prompts_from_keywords(
    keywords: list[str],
    client: genai.Client,
    template_file: Path,
) -> list[PromptSpec]:
    template = load_prompt_template(template_file)
    rendered_template = render_prompt_template(template, keywords)
    generated_text = generate_prompt_batch(client, rendered_template)
    prompts = parse_prompt_text(generated_text, "interactive prompt generation")

    if len(prompts) != len(keywords):
        raise ValueError(
            "The prompt generator returned "
            f"{len(prompts)} prompts for {len(keywords)} keywords. "
            "The response must contain exactly one prompt per keyword."
        )

    return prompts


def file_extension_for_mime_type(mime_type: str) -> str:
    if mime_type == "image/png":
        return "png"
    if mime_type == "image/webp":
        return "webp"
    return "jpg"


def generate_image(
    client: genai.Client,
    model: str,
    prompt: str,
    aspect_ratio: str,
    image_size: str,
    output_mime_type: str,
    images_per_prompt: int,
):
    return client.models.generate_images(
        model=model,
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=images_per_prompt,
            output_mime_type=output_mime_type,
            person_generation="ALLOW_ALL",
            aspect_ratio=aspect_ratio,
            image_size=image_size,
        ),
    )


def save_generated_image(generated_image, output_path: Path) -> None:
    if generated_image.image is None or not generated_image.image.image_bytes:
        filtered_reason = getattr(generated_image, "rai_filtered_reason", None)
        if filtered_reason:
            raise RuntimeError(filtered_reason)
        raise RuntimeError("The image bytes are not set.")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    generated_image.image.save(output_path)


def preview_prompts(prompts: list[PromptSpec]) -> None:
    first_prompt = prompts[0]
    logging.info("%s prompts were generated based on your keywords.", len(prompts))
    logging.info("--- Prompt Preview (first prompt) ---")
    logging.info("%s: %s", first_prompt.display_title, first_prompt.prompt_text)
    logging.info("-------------------------------------")


def process_prompts(
    prompts: list[PromptSpec], client: genai.Client, config: argparse.Namespace
) -> int:
    total = len(prompts)
    failures = 0
    output_dir = resolve_path(config.output_dir)
    extension = file_extension_for_mime_type(config.output_mime_type)

    for index, prompt_spec in enumerate(prompts, start=1):
        logging.info(
            "Generating %s/%s -> %s image(s) for %s",
            index,
            total,
            config.images_per_prompt,
            prompt_spec.title_slug,
        )

        try:
            result = generate_image(
                client=client,
                model=config.model,
                prompt=prompt_spec.prompt_text,
                aspect_ratio=config.aspect_ratio,
                image_size=config.image_size,
                output_mime_type=config.output_mime_type,
                images_per_prompt=config.images_per_prompt,
            )

            if not result.generated_images:
                raise RuntimeError("No images generated.")

            for image_index, generated_image in enumerate(result.generated_images, start=1):
                output_path = output_dir / (
                    f"{index:03d}_{prompt_spec.title_slug}_{image_index:02d}.{extension}"
                )
                save_generated_image(generated_image, output_path)
        except PermissionDenied as exc:
            failures += 1
            logging.error(
                "Failed on prompt %s (%s) due to Vertex AI permission error: %s",
                index,
                prompt_spec.title_slug,
                exc,
            )
            logging.error(
                "Check that Vertex AI is enabled for the configured project, your Google Cloud "
                "credentials are valid, and the project has permission to call the model."
            )
        except Exception as exc:
            failures += 1
            logging.error(
                "Failed on prompt %s (%s): %s",
                index,
                prompt_spec.title_slug,
                exc,
            )

    logging.info(
        "Finished. Success: %s, Failures: %s, Output dir: %s",
        total - failures,
        failures,
        output_dir,
    )
    return 1 if failures else 0


def validate_config(config: argparse.Namespace) -> None:
    if config.images_per_prompt < 1:
        raise ValueError("--images-per-prompt must be greater than or equal to 1")


def run_file_mode(config: argparse.Namespace) -> int:
    prompts = parse_prompts_file(Path(config.prompts_file))
    client = build_client()
    return process_prompts(prompts, client, config)


def run_interactive_mode(config: argparse.Namespace) -> int:
    logging.info("Entering interactive mode.")
    try:
        client = build_client()
        template_file = choose_template_file()
        words_input = input("Enter keywords, separated by commas: ").strip()
        if not words_input:
            logging.warning("No input provided. Exiting.")
            return 0

        keywords = parse_keywords(words_input)
        prompts = generate_prompts_from_keywords(keywords, client, template_file)
        preview_prompts(prompts)

        confirm = input("Proceed with image generation? (y/n): ").strip().lower()
        if confirm not in ("y", "yes"):
            logging.info("Generation cancelled by user. Exiting.")
            return 0

        return process_prompts(prompts, client, config)
    except KeyboardInterrupt:
        print()
        logging.warning("Operation cancelled by user. Exiting.")
        return 1


def main() -> int:
    from dotenv import load_dotenv

    load_dotenv()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    config = parse_args()

    try:
        validate_config(config)
        if config.interactive:
            return run_interactive_mode(config)
        return run_file_mode(config)
    except PermissionDenied:
        logging.error("=" * 80)
        logging.error("AUTHENTICATION FAILED: Vertex AI rejected the request.")
        logging.error("Verify the following before running again:")
        logging.error("  1. GOOGLE_GENAI_USE_VERTEXAI=true")
        logging.error("  2. GOOGLE_CLOUD_PROJECT is set to the correct project")
        logging.error("  3. GOOGLE_CLOUD_LOCATION is set, or global is acceptable")
        logging.error("  4. Application Default Credentials are available")
        logging.error("  5. Vertex AI API is enabled and billing is active")
        logging.error("=" * 80)
        return 1
    except Exception as exc:
        logging.error("An unexpected error occurred: %s", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
