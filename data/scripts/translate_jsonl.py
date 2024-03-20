import json
from collections import defaultdict
import os
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from load_dotenv import load_dotenv
import json

load_dotenv()

def do():
    translate_prompt = PromptTemplate.from_template(""" 
        Return ONLY the following sentence/word
        converted to Hinglish.
        Include no directives in your answer.
        {to_translate}                                             
    """)
    model = ChatOpenAI(model="gpt-4")
    translate_chain = LLMChain(llm=model, prompt=translate_prompt)
    def to_hinglish(query):
        return translate_chain.run(query)
            
    def get_traps(filepath):
        data = []
        traps = set()
        with open(filepath, 'r', encoding='utf-8') as file:  # Ensure UTF-8 encoding
            for line in file:
                json_object = json.loads(line.strip())
                data.append(json_object)
                traps.add(json_object["completion"])
        return data, traps
    
    
    def write_jsonl_file(data, filepath):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        try:
            with open(filepath, 'w+', encoding='utf-8') as file:  # Ensure UTF-8 encoding
                for entry in data:
                    json_line = json.dumps(entry, ensure_ascii=False)  # Keep Unicode characters
                    file.write(json_line + '\n')
        except IOError as e:
            print(f"IO error: {e}")
        
        
    
    def translate_traps(traps):
        mapping = defaultdict(str)
        return {trap: to_hinglish(trap) for trap in traps}
            
    def translate_jsonl(data, mapping):
        translated = []
        for i in data:
            k,v = i.items()
            new_obj = {}
            new_obj["prompt"] = to_hinglish(k[1])
            new_obj["completion"] = mapping[v[1]]
            translated.append(new_obj)
            print(new_obj)
        write_jsonl_file(translated, f"data/hinglish/thinking_traps.jsonl")
        
        
    data, traps = get_traps('../original/thinking_traps.jsonl') 
    mapping = translate_traps(traps)
    print(mapping)
    # translate_jsonl(data, mapping)
     
    
do()
        
        
    
def to_assistant_format(jsonl_path, jsonl_write_path):
    def transform(json_obj):
        return (
            {"messages": [
                {  
                 "role": "system", 
                 "content": "You will be provided with a situation and a corresponding negative thought had by a user in Hinglish. Your goal is to reframe the negative thought,as if you were the user, also in Hinglish with a focus on empathy and providing actionable insights. You are not to include any directives in your answer. Speak as if you were the user."}, 
                {"role": "user", 
                 "content": json_obj["prompt"]}, 
                {"role": "assistant", 
                 "content": json_obj["completion"]
                 }
                ]
             }
            )
        
    with open(jsonl_write_path, 'a') as file_out:
        with open(jsonl_path, 'r') as file_in:
            for line in file_in:
                json_object = dict(json.loads(line.strip()))
                json_line_transformed = json.dumps(transform(json_object))
                file_out.write(json_line_transformed + '\n')
        
def improve_prompts_and_convert_to_assistant_format(file_path, output_file_path):
    with open(file_path, 'r', encoding='utf-8') as infile, open(output_file_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            data = json.loads(line)
            prompt = data.get('prompt', '')
            situation_start = prompt.find('Here is a situation') + len('Here is a situation ')
            situation_end = prompt.find('. Here is what the situation made me think.')
            situation = prompt[situation_start:situation_end].strip()
            thought = prompt[situation_end + len('. Here is what the situation made me think. '):].strip()
            data['prompt'] = f"Situation:{situation}\nThought:{thought}"
            data["completion"]
            # Write the modified JSON object back to the file
            json.dump(data, outfile)
            outfile.write('\n')
            
    to_assistant_format(output_file_path, "./data/gpt-4/improved_prompts.jsonl")

# Replace 'input.jsonl' with your input file path and 'output.jsonl' with your desired output file path
# input_file_path = './data/gpt-4/output.jsonl'
# output_file_path = './data/gpt-4/output_refined.jsonl'
# improve_prompts_and_convert_to_assistant_format(input_file_path, output_file_path)
