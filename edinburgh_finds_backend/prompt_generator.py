import json

with open('prompt_input.json', 'r') as prompt_input_file:
    prompt_input_data = json.loads(prompt_input_file.read())
    
final_prompt_json_dict = {}

for key, value in prompt_input_data.items():
    final_prompt_json_dict[key] = value

final_prompt_json_string = json.dumps(final_prompt_json_dict)

prompt_preamble = "You are a specialized AI assistant for structured data extraction. Your output must be a single, valid JSON object and nothing else. Follow the provided JSON schema exactly."

final_prompt = f'{prompt_preamble}{final_prompt_json_string}'

print(final_prompt)
