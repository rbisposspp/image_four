# Project: Image Four (Batch Image Generation)

## Project Overview
This is a Python-based utility project designed to batch-generate images using the Google GenAI SDK (specifically targeting the Imagen 4.0 model). It reads structured image prompts from a Markdown file and outputs the generated images to a designated directory.

The project is currently tailored for generating educational or thematic image sets (e.g., for ESL learners) with consistent branding or text inclusion.

## Key Files
*   **`ai_studio_code.py`**: The main execution script. It handles argument parsing, file reading, calling Vertex AI through the Google GenAI SDK to generate prompts and images, and saving the outputs locally.
*   **`PROMPTS.md`**: The default input file containing a numbered list of image prompts formatted as `1. **Title:** Description`.
*   **`PROMPT_GENERATOR_TEMPLATE.md`**: A system prompt template used by the interactive mode to convert raw keywords into the rich, formatted prompt list required by `PROMPTS.md`.
*   **`generated_images/`**: The default output directory where generated images are saved.
*   **`.venv/`**: A standard Python virtual environment containing the project's dependencies (including `google-genai`).

## Building and Running

### Prerequisites
The project relies on a Python virtual environment.
You **must** configure Vertex AI before running the script.

```bash
export GOOGLE_GENAI_USE_VERTEXAI=true
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_CLOUD_LOCATION="global"
gcloud auth application-default login
```

### Execution
Run the main script using the project virtual environment:

```bash
./.venv/bin/python ai_studio_code.py
```

### Command Line Arguments
The script supports several arguments to customize the generation process:
*   `--prompts-file`: Path to the markdown file with prompts (default: `PROMPTS.md`)
*   `--output-dir`: Directory to save images (default: `generated_images`)
*   `--model`: Image generation model (default: `imagen-4.0-generate-001`)
*   `--aspect-ratio`: Aspect ratio for images (default: `1:1`)
*   `--image-size`: Output size (default: `1K`)
*   `--output-mime-type`: Output format (default: `image/jpeg`)
*   `--images-per-prompt`: Number of variations per prompt (default: `1`)

Example with custom arguments:
```bash
./.venv/bin/python ai_studio_code.py --images-per-prompt 2 --output-dir my_custom_folder
```

## Development Conventions
*   **Prompt Formatting:** The input Markdown file (`PROMPTS.md`) must follow a strict pattern for the script to parse it correctly: `1. **Title:** Prompt description`. 
*   **File Naming:** Generated images are automatically named using the prompt's index, a sanitized version of the title (slug), and the image variation index (e.g., `002_bedroom_01.jpg`).
*   **Style/Theme:** Based on `PROMPT_GENERATOR_TEMPLATE.md`, the intended visual style for the default prompts targets children learning English, emphasizing bright, colorful, friendly, and clean visuals with subtle text integration ("RBS ESL Tech Teach").
