import json
import pandas as pd
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from load_dotenv import load_dotenv
import os

load_dotenv()

def do(last_processed=0):
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
    
    df = pd.read_csv("./data/reframing_dataset.csv")
    output_filepath = "./data/output.jsonl"

    with open(output_filepath, 'a') as file:
        for ind in df.index:
            if ind < last_processed:
                continue
            else:
                situation = df['situation'][ind]
                thought = df['thought'][ind]
                reframe = df['reframe'][ind]
                
                new_obj = {}
                new_obj["prompt"] = f"Here is a situation {to_hinglish(situation)}. Here is what the situation made me think. {to_hinglish(thought)} How can I reframe this thought?"
                new_obj["completion"] = to_hinglish(reframe)
                json_line = json.dumps(new_obj)
                file.write(json_line + '\n')

#do()


def to_assistant_format(jsonl_path, jsonl_write_path):
    def transform(json_obj):
        return (
            {"messages": [
                {  
                 "role": "system", 
                 "content": "You will be provided with a negative thought had by a user in Hinglish. Your goal is to output the appropriate negative thought pattern, also in Hinglish."}, 
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
        
to_assistant_format('./data/gpt-4/thinking_traps_hinglish_1.jsonl', './data/gpt-4/thinking_traps_hinglish_pairs_assistant_format.jsonl')