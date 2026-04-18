You need to debug and fix a specific regression in the current Python project.

Project context:
- Main file: `ai_studio_code.py`
- Stack: Python + `google-genai`
- The script now has an `--interactive` mode
- Existing non-interactive / file-based generation must keep working exactly as before

Bug to fix:
When I run:

`./.venv/bin/python ai_studio_code.py --interactive`

and enter keywords like:

`witch house, broom, wand, troll, prince, princess, castle`

the script says prompts were generated, but the preview shows the entire raw template file content instead of actual generated prompts.

Current wrong behavior:
- `INFO: 7 prompts were generated based on your keywords.`
- `INFO: --- Prompt Preview ---`
- then it prints the full contents of the prompt template file
- generation preview is therefore wrong

Expected behavior:
- the interactive flow must transform the entered keywords into actual final prompts
- the preview must show one real generated prompt, not the raw template
- if 7 keywords are entered, the system should produce 7 actual prompts
- those prompts must be the same kind of final prompts the normal generation pipeline expects
- after confirmation, image generation must use those real prompts

Your task:
1. Inspect the current codebase first
2. Find the root cause of why the preview is showing the raw template instead of rendered prompts
3. Fix the bug with the smallest clean architectural change
4. Preserve the existing non-interactive behavior
5. Do not introduce hacks or duplicate logic

Implementation requirements:
- Do not hardcode fake prompt output
- Do not just hide the preview bug
- Fix the actual prompt-generation pipeline
- Ensure interactive mode produces a true `List[str]` of final prompts
- Ensure preview reads from that real generated list
- Ensure downstream image generation uses the same real prompt list
- Handle empty input and cancellation cleanly
- Keep the code modular and maintainable

What I want from you:
Phase 1:
- Inspect `ai_studio_code.py` and related files
- Explain briefly what the current interactive flow is doing
- Identify the exact bug source

Phase 2:
- Implement the fix
- Keep the architecture clean
- Reuse existing generation logic where appropriate

Phase 3:
- Validate the result
- Show:
  - which files changed
  - the root cause
  - what was fixed
  - how to test the fix

Important:
Before editing, confirm in your analysis whether the bug is caused by one of these:
- the template file is being returned directly instead of rendered
- the code is confusing “template text” with “final prompts”
- the interactive mode is skipping the LLM/template-rendering step
- the preview is reading the wrong variable

After fixing, test with this exact example:
`witch house, broom, wand, troll, prince, princess, castle`

The preview should show one actual generated prompt, not the template contents.


_______________________ERROR_____________________

catbo300684@DESKTOP-C4PFUSH:~/projects/image_four$ python ai_studio_code.py --interactive
Traceback (most recent call last):
  File "/home/catbo300684/projects/image_four/ai_studio_code.py", line 8, in <module>
    from google import genai
ModuleNotFoundError: No module named 'google'
catbo300684@DESKTOP-C4PFUSH:~/projects/image_four$ ./.venv/bin/python ai_studio_code.py --interactive
INFO: Entering interactive mode.
Enter keywords, separated by commas: witch house, broom, wand, troll, prince, princess, castle
INFO: 7 prompts were generated based on your keywords.
INFO: --- Prompt Preview ---
INFO: # Prompt generator template

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
- witch house
- broom
- wand
- troll
- prince
- princess
- castle
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

INFO: ----------------------
Proceed with image generation? (y/n): y
INFO: Generating 1/7 -> 1 image(s) for witch_house
INFO: HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict "HTTP/1.1 403 Forbidden"
ERROR: Failed on prompt 1 (witch_house): 403 PERMISSION_DENIED. {'error': {'code': 403, 'message': 'Requests to this API generativelanguage.googleapis.com method google.ai.generativelanguage.v1beta.PredictionService.Predict are blocked.', 'status': 'PERMISSION_DENIED', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_SERVICE_BLOCKED', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com', 'consumer': 'projects/891558245394', 'methodName': 'google.ai.generativelanguage.v1beta.PredictionService.Predict', 'apiName': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'Requests to this API generativelanguage.googleapis.com method google.ai.generativelanguage.v1beta.PredictionService.Predict are blocked.'}]}}
INFO: Generating 2/7 -> 1 image(s) for broom
INFO: HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict "HTTP/1.1 403 Forbidden"
ERROR: Failed on prompt 2 (broom): 403 PERMISSION_DENIED. {'error': {'code': 403, 'message': 'Requests to this API generativelanguage.googleapis.com method google.ai.generativelanguage.v1beta.PredictionService.Predict are blocked.', 'status': 'PERMISSION_DENIED', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_SERVICE_BLOCKED', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com', 'consumer': 'projects/891558245394', 'methodName': 'google.ai.generativelanguage.v1beta.PredictionService.Predict', 'apiName': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'Requests to this API generativelanguage.googleapis.com method google.ai.generativelanguage.v1beta.PredictionService.Predict are blocked.'}]}}
INFO: Generating 3/7 -> 1 image(s) for wand
INFO: HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict "HTTP/1.1 403 Forbidden"
ERROR: Failed on prompt 3 (wand): 403 PERMISSION_DENIED. {'error': {'code': 403, 'message': 'Requests to this API generativelanguage.googleapis.com method google.ai.generativelanguage.v1beta.PredictionService.Predict are blocked.', 'status': 'PERMISSION_DENIED', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_SERVICE_BLOCKED', 'domain': 'googleapis.com', 'metadata': {'service': 'generativelanguage.googleapis.com', 'methodName': 'google.ai.generativelanguage.v1beta.PredictionService.Predict', 'consumer': 'projects/891558245394', 'apiName': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'Requests to this API generativelanguage.googleapis.com method google.ai.generativelanguage.v1beta.PredictionService.Predict are blocked.'}]}}
INFO: Generating 4/7 -> 1 image(s) for troll
INFO: HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict "HTTP/1.1 403 Forbidden"
ERROR: Failed on prompt 4 (troll): 403 PERMISSION_DENIED. {'error': {'code': 403, 'message': 'Requests to this API generativelanguage.googleapis.com method google.ai.generativelanguage.v1beta.PredictionService.Predict are blocked.', 'status': 'PERMISSION_DENIED', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_SERVICE_BLOCKED', 'domain': 'googleapis.com', 'metadata': {'methodName': 'google.ai.generativelanguage.v1beta.PredictionService.Predict', 'service': 'generativelanguage.googleapis.com', 'apiName': 'generativelanguage.googleapis.com', 'consumer': 'projects/891558245394'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'Requests to this API generativelanguage.googleapis.com method google.ai.generativelanguage.v1beta.PredictionService.Predict are blocked.'}]}}
INFO: Generating 5/7 -> 1 image(s) for prince
INFO: HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict "HTTP/1.1 403 Forbidden"
ERROR: Failed on prompt 5 (prince): 403 PERMISSION_DENIED. {'error': {'code': 403, 'message': 'Requests to this API generativelanguage.googleapis.com method google.ai.generativelanguage.v1beta.PredictionService.Predict are blocked.', 'status': 'PERMISSION_DENIED', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_SERVICE_BLOCKED', 'domain': 'googleapis.com', 'metadata': {'methodName': 'google.ai.generativelanguage.v1beta.PredictionService.Predict', 'service': 'generativelanguage.googleapis.com', 'apiName': 'generativelanguage.googleapis.com', 'consumer': 'projects/891558245394'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'Requests to this API generativelanguage.googleapis.com method google.ai.generativelanguage.v1beta.PredictionService.Predict are blocked.'}]}}
INFO: Generating 6/7 -> 1 image(s) for princess
INFO: HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict "HTTP/1.1 403 Forbidden"
ERROR: Failed on prompt 6 (princess): 403 PERMISSION_DENIED. {'error': {'code': 403, 'message': 'Requests to this API generativelanguage.googleapis.com method google.ai.generativelanguage.v1beta.PredictionService.Predict are blocked.', 'status': 'PERMISSION_DENIED', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_SERVICE_BLOCKED', 'domain': 'googleapis.com', 'metadata': {'consumer': 'projects/891558245394', 'apiName': 'generativelanguage.googleapis.com', 'service': 'generativelanguage.googleapis.com', 'methodName': 'google.ai.generativelanguage.v1beta.PredictionService.Predict'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'Requests to this API generativelanguage.googleapis.com method google.ai.generativelanguage.v1beta.PredictionService.Predict are blocked.'}]}}
INFO: Generating 7/7 -> 1 image(s) for castle
INFO: HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict "HTTP/1.1 403 Forbidden"
ERROR: Failed on prompt 7 (castle): 403 PERMISSION_DENIED. {'error': {'code': 403, 'message': 'Requests to this API generativelanguage.googleapis.com method google.ai.generativelanguage.v1beta.PredictionService.Predict are blocked.', 'status': 'PERMISSION_DENIED', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_SERVICE_BLOCKED', 'domain': 'googleapis.com', 'metadata': {'methodName': 'google.ai.generativelanguage.v1beta.PredictionService.Predict', 'service': 'generativelanguage.googleapis.com', 'consumer': 'projects/891558245394', 'apiName': 'generativelanguage.googleapis.com'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'Requests to this API generativelanguage.googleapis.com method google.ai.generativelanguage.v1beta.PredictionService.Predict are blocked.'}]}}
INFO: Finished. Success: 0, Failures: 7, Output dir: generated_images
catbo300684@DESKTOP-C4PFUSH:~/projects/image_four$


_______________________ERROR-2_____________________



4@DESKTOP-C4PFUSH:~/projects/image_four$ ./.venv/bin/python ai_studio_code.py --interactive
INFO: Entering interactive mode.
Enter keywords, separated by commas: bee bite by an apple, psicodelic boy bedroom, witch house made by candy
INFO: 3 prompts were generated based on your keywords.
INFO: --- Prompt Preview ---
INFO: # Prompt generator template

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
- bee bite by an apple
- psicodelic boy bedroom
- witch house made by candy
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

INFO: ----------------------
Proceed with image generation? (y/n): y
INFO: Generating 1/3 -> 1 image(s) for bee_bite_by_an_apple
INFO: HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict "HTTP/1.1 200 OK"
INFO: Generating 2/3 -> 1 image(s) for psicodelic_boy_bedroom
INFO: HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict "HTTP/1.1 200 OK"
INFO: Generating 3/3 -> 1 image(s) for witch_house_made_by_candy
INFO: HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict "HTTP/1.1 200 OK"
INFO: Finished. Success: 3, Failures: 0, Output dir: generated_images
catbo300684@DESKTOP-C4PFUSH:~/projects/image_four$ cd ..
catbo300684@DESKTOP-C4PFUSH:~/projects$ cd image_four
catbo300684@DESKTOP-C4PFUSH:~/projects/image_four$ ./.venv/bin/python ai_studio_code.py
Traceback (most recent call last):
  File "/home/catbo300684/projects/image_four/ai_studio_code.py", line 325, in <module>
    sys.exit(main())
             ^^^^^^
  File "/home/catbo300684/projects/image_four/ai_studio_code.py", line 321, in main
    return run_file_mode(config, api_key)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/catbo300684/projects/image_four/ai_studio_code.py", line 263, in run_file_mode
    prompts = parse_prompts_file(prompts_file)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/catbo300684/projects/image_four/ai_studio_code.py", line 74, in parse_prompts_file
    raise FileNotFoundError(f"Prompts file not found: {prompts_file}")
FileNotFoundError: Prompts file not found: PROMPTS.md
catbo300684@DESKTOP-C4PFUSH:~/projects/image_four$ ./.venv/bin/python ai_studio_code.py --interactive
INFO: Entering interactive mode.
Enter keywords, separated by commas: bee bite by an apple, psicodelic boy bedroom, witch house made by candy
ERROR: An unexpected error occurred in interactive mode: 'Client' object has no attribute 'GenerativeModel'
catbo300684@DESKTOP-C4PFUSH:~/projects/image_four$





_______________________ERROR-3________________________



File "/home/catbo300684/projects/image_four/ai_studio_code.py", line 327, in <module>
    sys.exit(main())
             ^^^^^^
  File "/home/catbo300684/projects/image_four/ai_studio_code.py", line 318, in main
    genai.configure(api_key=api_key)
    ^^^^^^^^^^^^^^^
AttributeError: module 'google.genai' has no attribute 'configure'
catbo300684@DESKTOP-C4PFUSH:~/projects/image_four$ ./.venv/bin/python ai_studio_code.py --interactive
INFO: Entering interactive mode.
WARNING: Both GOOGLE_API_KEY and GEMINI_API_KEY are set. Using GOOGLE_API_KEY.
Enter keywords, separated by commas: bee bite by an apple, psicodelic boy bedroom, witch house made by candy
INFO: Generating rich prompt for 'bee bite by an apple' using gemini-3-flash-preview...
INFO: AFC is enabled with max remote calls: 10.
INFO: HTTP Request: POST https://aiplatform.googleapis.com/v1beta1/publishers/google/models/gemini-3-flash-preview:generateContent "HTTP/1.1 403 Forbidden"
ERROR: LLM generation or parsing failed for 'bee bite by an apple': 403 PERMISSION_DENIED. {'error': {'code': 403, 'message': 'Requests to this API aiplatform.googleapis.com method google.cloud.aiplatform.v1beta1.PredictionService.GenerateContent are blocked.', 'status': 'PERMISSION_DENIED', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_SERVICE_BLOCKED', 'domain': 'googleapis.com', 'metadata': {'apiName': 'aiplatform.googleapis.com', 'consumer': 'projects/891558245394', 'service': 'aiplatform.googleapis.com', 'methodName': 'google.cloud.aiplatform.v1beta1.PredictionService.GenerateContent'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'Requests to this API aiplatform.googleapis.com method google.cloud.aiplatform.v1beta1.PredictionService.GenerateContent are blocked.'}]}}. Falling back to simple prompt.
INFO: Generating rich prompt for 'psicodelic boy bedroom' using gemini-3-flash-preview...
INFO: AFC is enabled with max remote calls: 10.
INFO: HTTP Request: POST https://aiplatform.googleapis.com/v1beta1/publishers/google/models/gemini-3-flash-preview:generateContent "HTTP/1.1 403 Forbidden"
ERROR: LLM generation or parsing failed for 'psicodelic boy bedroom': 403 PERMISSION_DENIED. {'error': {'code': 403, 'message': 'Requests to this API aiplatform.googleapis.com method google.cloud.aiplatform.v1beta1.PredictionService.GenerateContent are blocked.', 'status': 'PERMISSION_DENIED', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_SERVICE_BLOCKED', 'domain': 'googleapis.com', 'metadata': {'service': 'aiplatform.googleapis.com', 'apiName': 'aiplatform.googleapis.com', 'consumer': 'projects/891558245394', 'methodName': 'google.cloud.aiplatform.v1beta1.PredictionService.GenerateContent'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'Requests to this API aiplatform.googleapis.com method google.cloud.aiplatform.v1beta1.PredictionService.GenerateContent are blocked.'}]}}. Falling back to simple prompt.
INFO: Generating rich prompt for 'witch house made by candy' using gemini-3-flash-preview...
INFO: AFC is enabled with max remote calls: 10.
INFO: HTTP Request: POST https://aiplatform.googleapis.com/v1beta1/publishers/google/models/gemini-3-flash-preview:generateContent "HTTP/1.1 403 Forbidden"
ERROR: LLM generation or parsing failed for 'witch house made by candy': 403 PERMISSION_DENIED. {'error': {'code': 403, 'message': 'Requests to this API aiplatform.googleapis.com method google.cloud.aiplatform.v1beta1.PredictionService.GenerateContent are blocked.', 'status': 'PERMISSION_DENIED', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_SERVICE_BLOCKED', 'domain': 'googleapis.com', 'metadata': {'methodName': 'google.cloud.aiplatform.v1beta1.PredictionService.GenerateContent', 'apiName': 'aiplatform.googleapis.com', 'service': 'aiplatform.googleapis.com', 'consumer': 'projects/891558245394'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'Requests to this API aiplatform.googleapis.com method google.cloud.aiplatform.v1beta1.PredictionService.GenerateContent are blocked.'}]}}. Falling back to simple prompt.
INFO: 3 prompts were generated based on your keywords.
INFO: --- Prompt Preview ---
INFO: A vivid image of bee bite by an apple for children.
INFO: ----------------------
Proceed with image generation? (y/n): y
INFO: Generating 1/3 -> 1 image(s) for bee_bite_by_an_apple
INFO: HTTP Request: POST https://aiplatform.googleapis.com/v1beta1/publishers/google/models/imagen-4.0-generate-001:predict "HTTP/1.1 403 Forbidden"
ERROR: Failed on prompt 1 (bee_bite_by_an_apple): 403 PERMISSION_DENIED. {'error': {'code': 403, 'message': 'Requests to this API aiplatform.googleapis.com method google.cloud.aiplatform.v1beta1.PredictionService.Predict are blocked.', 'status': 'PERMISSION_DENIED', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_SERVICE_BLOCKED', 'domain': 'googleapis.com', 'metadata': {'service': 'aiplatform.googleapis.com', 'apiName': 'aiplatform.googleapis.com', 'methodName': 'google.cloud.aiplatform.v1beta1.PredictionService.Predict', 'consumer': 'projects/891558245394'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'Requests to this API aiplatform.googleapis.com method google.cloud.aiplatform.v1beta1.PredictionService.Predict are blocked.'}]}}
INFO: Generating 2/3 -> 1 image(s) for psicodelic_boy_bedroom
INFO: HTTP Request: POST https://aiplatform.googleapis.com/v1beta1/publishers/google/models/imagen-4.0-generate-001:predict "HTTP/1.1 403 Forbidden"
ERROR: Failed on prompt 2 (psicodelic_boy_bedroom): 403 PERMISSION_DENIED. {'error': {'code': 403, 'message': 'Requests to this API aiplatform.googleapis.com method google.cloud.aiplatform.v1beta1.PredictionService.Predict are blocked.', 'status': 'PERMISSION_DENIED', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_SERVICE_BLOCKED', 'domain': 'googleapis.com', 'metadata': {'service': 'aiplatform.googleapis.com', 'apiName': 'aiplatform.googleapis.com', 'methodName': 'google.cloud.aiplatform.v1beta1.PredictionService.Predict', 'consumer': 'projects/891558245394'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'Requests to this API aiplatform.googleapis.com method google.cloud.aiplatform.v1beta1.PredictionService.Predict are blocked.'}]}}
INFO: Generating 3/3 -> 1 image(s) for witch_house_made_by_candy
INFO: HTTP Request: POST https://aiplatform.googleapis.com/v1beta1/publishers/google/models/imagen-4.0-generate-001:predict "HTTP/1.1 403 Forbidden"
ERROR: Failed on prompt 3 (witch_house_made_by_candy): 403 PERMISSION_DENIED. {'error': {'code': 403, 'message': 'Requests to this API aiplatform.googleapis.com method google.cloud.aiplatform.v1beta1.PredictionService.Predict are blocked.', 'status': 'PERMISSION_DENIED', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_SERVICE_BLOCKED', 'domain': 'googleapis.com', 'metadata': {'apiName': 'aiplatform.googleapis.com', 'methodName': 'google.cloud.aiplatform.v1beta1.PredictionService.Predict', 'service': 'aiplatform.googleapis.com', 'consumer': 'projects/891558245394'}}, {'@type': 'type.googleapis.com/google.rpc.LocalizedMessage', 'locale': 'en-US', 'message': 'Requests to this API aiplatform.googleapis.com method google.cloud.aiplatform.v1beta1.PredictionService.Predict are blocked.'}]}}
INFO: Finished. Success: 0, Failures: 3, Output dir: generated_images
catbo300684@DESKTOP-C4PFUSH:~/projects/image_four$