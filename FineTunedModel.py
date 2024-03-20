import os
from load_dotenv import load_dotenv
load_dotenv()
class FineTunedModel:
    def __init__(self, model_id:str, system_prompt:str):
        self.model_id = model_id
        self.system_prompt = system_prompt
        
        
        
        
traps_model = FineTunedModel(
   os.environ.get("TRAPS_FINE_TUNED_MODEL_ID"),
   """You will be provided with a negative thought had by a user in Hinglish.
   Your goal is to output the appropriate negative thought pattern, also in Hinglish.
   Here are the valid thought patterns
   {
    "Bhavnatmak tarkikta":"Emotional reasoning"
    "Mann ki padhna":"Mind reading"
    "Sakaratmak ko nirakaran karna":"Disqualifying the positive"
    "Negativ bhavna ya emotion":"Negative feeling or emotion"
    "Personalizing":"Personalizing"
    "Bhavishya batana":"Fortune telling"
    "Overgeneralization":"Overgeneralization"
    "Labeling":"Labeling"
    "Sab-kuch-ya-kuch-nahi soch":"All-or-nothing thinking"
    "Katastrophizing":"Catastrophizing"
    "Personalization":"Personalization"
    "Doshee dena":"Blaming"
    "Nahi vikrit":"Not distorted"
    "Sakaratmak ko disqualify karna":"Disqualifying the Positive"
    "Chahiye bayanein":"Should statements"
    "Tulna":"Comparing"
    "Tulna aur Nirasha":"Comparing and Despairing"
    }
   """
)

reframe_model = FineTunedModel(
  "ft:gpt-3.5-turbo-0125:cornell-university::94X3VtYC",
   """
   You will be provided with a situation and a corresponding negative 
   thought had by a user in Hinglish. 
   Your goal is to reframe the negative thought,as if you were the user, 
   also in Hinglish.
   You are not to include any directives in your answer. Speak as if you were the user."""
  
)