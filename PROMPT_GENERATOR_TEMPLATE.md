# Prompt generator template

Use this prompt in Gemini, ChatGPT, or another LLM when you want to turn a
list of words or expressions into prompts that match the format in
`PROMPTS.md`.

## Base prompt

```text
You will receive a list of words or expressions.

Your task is to convert each item into one image prompt using exactly the same
output format as this model:

1. **Title:** A detailed visual scene description in English. If needed, add
small contextual details that make the scene richer and more natural. Keep the
scene appropriate for image generation. If there is a brand, school, or text
string I provide, integrate it subtly into an object inside the scene.

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

Optional style constraints:
- Target audience: children learning English.
- Visual style: bright, friendly, colorful, clean.
- If the input is a room, object, or place in a house, create a scene with a
child interacting naturally with that place or object.
- If I provide a text string, include it subtly in the scene, not as the main
focus.

Input items:
[PASTE YOUR WORDS OR EXPRESSIONS HERE]
```

## Example input

```text
living room
bedroom
kitchen
door
window
```

## Example output

```text
1. **Living room:** A cozy living room where a child is building a pillow fort
on the floor during a sunny afternoon, with colorful books, toys, and warm
lighting creating a friendly atmosphere.
2. **Bedroom:** A playful bedroom with a child organizing stuffed animals on a
neatly made bed, surrounded by drawings, bright pillows, and a cheerful rug.
3. **Kitchen:** A bright kitchen where a child is mixing cookie dough with a
parent at the counter, with flour, wooden spoons, and a welcoming family feel.
4. **Door:** A child standing at a colorful bedroom door covered with fun
stickers, reaching for the handle as sunlight spills in from the hallway.
5. **Window:** A child looking out of a large sunny window at a green garden,
with soft curtains moving gently and a calm, bright morning mood.
```
