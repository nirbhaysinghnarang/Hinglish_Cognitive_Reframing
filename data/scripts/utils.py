import json

def convert_to_jsonl(input_filepath, output_filepath):
    with open(input_filepath, 'r') as input_file, open(output_filepath, 'w') as output_file:
        for line in input_file:
            try:
                json_object = json.loads(line.replace("'", '"'))
                output_file.write(json.dumps(json_object) + '\n')
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}, in line: {line}")

# Example usage:
convert_to_jsonl('data/gpt-4/thinking_traps_hinglish.txt', 'data/gpt-4/thinking_traps_hinglish_1.jsonl')
