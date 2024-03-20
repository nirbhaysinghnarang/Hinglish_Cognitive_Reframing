import streamlit as st
import os
from load_dotenv import load_dotenv
from openai import OpenAI
import json
from streamlit_extras.colored_header import colored_header
from eval_loop import eval_loop
from FineTunedModel import FineTunedModel, traps_model, reframe_model



mapping = {}
with open('data/gpt-4/mapping.json') as f:
  mapping = json.loads(f.read())

load_dotenv()

client = OpenAI()





def get_query_for_situation_thought_pair(sit, thought):
  return f"Situation:{sit}\nThought:{thought}. How can I reframe this thought?"

def get_finetuned_outputs(model:FineTunedModel, query:str):
  completion = client.chat.completions.create(
    model=model.model_id,
    messages=[
      {"role": "system", "content": model.system_prompt},
      {"role": "user", "content": query}
    ]
  )
  
  return completion.choices[0].message.content


colored_header(label="Nonty", description="Think Negative, Think Nonty! 🧠🚫")
st.markdown("Enter a negative thought in Hinglish and let Nonty help you reframe it!")
situation, thought = st.text_input("Yaha ek situation likhein."), st.text_input("Aapko is situation ke baare me kya vichaar aaye?")

btn = st.button("Submit")

if situation and thought and btn:
  print(get_query_for_situation_thought_pair(situation, thought))
  output_trap, output_reframed = get_finetuned_outputs(traps_model, thought), get_finetuned_outputs(reframe_model, get_query_for_situation_thought_pair(situation, thought))
  pattern, framing, rationale = eval_loop(situation, thought, output_reframed, output_trap)

  st.markdown(f"### **Nonty kehta hai tumhara vichar trap hai 👉🏻**")
  st.info(pattern)
  st.markdown(f"### Try thinking this instead 👉🏻")
  st.info(framing)
  st.markdown(f"### Kyu? 👉🏻")
  st.info(rationale)


  
  
st.link_button("Dataset", url="https://huggingface.co/datasets/nirbhaysinghnarang/HinglishCognitiveReframing")