# Prompt generator template - Halloween / scary

Use this prompt in Gemini, ChatGPT, or another LLM when you want to turn a
list of words or expressions into darker image prompts that still match the
format in `PROMPTS.md`.

## Base prompt

```text
You will receive a list of words or expressions.

Your task is to convert each item into one image prompt using exactly the same
output format as this model:

1. **Title:** A detailed visual scene description in English. If needed, add
small contextual details that make the scene richer and more cinematic. Keep
the scene appropriate for image generation. If there is a brand, school, or
text string I provide, integrate it subtly into an object inside the scene.

Rules:
- Output only the final list.
- Keep the numbering sequential.
- Use exactly this structure for each line:
  1. **Title:** Prompt text
- Write all prompts in English.
- Make each prompt specific, visual, and image-generation friendly.
- Keep one prompt per line.
- Do not add explanations, headings, notes, or code fences.
- Preserve the original order of the input items.
- Convert short words or expressions into natural scene titles.
- The title must be short and end before the colon.
- The prompt text must be one complete sentence or two concise sentences.

Style constraints:
- Target mood: spooky, eerie, unsettling, Halloween-like.
- Visual style: dark, cinematic, atmospheric, dramatic lighting.
- Use moonlight, fog, candlelight, storm clouds, haunted interiors, twisted
trees, glowing magic, eerie shadows, or other horror-friendly details when
appropriate.
- Do not soften scary themes into child-friendly scenes unless the input
explicitly asks for that.
- Avoid gore or graphic violence.

Input items:
[PASTE YOUR WORDS OR EXPRESSIONS HERE]
```

## Example input

```text
witch house
haunted broom
frog curse
```

## Example output

```text
1. **Witch house:** A crooked witch house made of cracked candy walls and dark
icing stands deep in a foggy forest at night, with dim lantern light, glowing
windows, and an eerie trail leading to the door.
2. **Haunted broom:** An old enchanted broom hovers inside a candlelit attic,
surrounded by floating dust, torn curtains, and long shadows that create a
tense Halloween atmosphere.
3. **Frog curse:** A psychedelic frog sits on a wet stone in a haunted swamp as
green cursed smoke spirals around it, with twisted trees, violet moonlight,
and sinister magic reflecting in the water.
```
