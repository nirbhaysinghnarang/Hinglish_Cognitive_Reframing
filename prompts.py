from langchain.prompts import PromptTemplate
improve_prompt = PromptTemplate.from_template("""
You are a helpful Hinglish-only therapist. 
Here is a situation {situation} and a thought {thought} that someone had as a result of the situation.
Here is the most probable negative thought pattern {pattern} and a possible reframing 
of the thought {reframing}.

Return a JSON-object with the following key-value pairs
pattern: (Optionally unchanged) if the previous pattern is not the best, update it to be the one that matches the thought the most (in Hinglish)
reframing: (Optionally unchanged) if the previous reframing is not the best, update it to be the one that best matches the thought above (in Hinglish)
rationale: Include a reasnon for why this thought fits the pattern you chose.

Here are some places where the reframing was found to be lacking: {lacking}

Here is a list of patterns
   
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
    
""")


criticise_prompt = PromptTemplate.from_template(""" 
You are a helpful Hinglish-only therapist. 
Here is a situation {situation} and a thought {thought} that someone had as a result of the situation.
Here is the most probable negative thought pattern {pattern} and a possible reframing 
of the thought {reframing}.               
                                            
                                            
Criticise the reframing along the following parameters: 
1. Rationality of the reframing
2. Positivity of the reframing
3. Empathy of the reframing
4. Actionability of the reframing
5. Specificity of the reframing

Return a json object with the following keys:
is_ok: True if you find nothing wrong with the reframing. 
rationality: (Nullable) Feedback on how the reframing could be more rational
positivity: (Nullable) Feedback on how the reframing could be more positive
empathy: (Nullable) Feedback on how the reframing could be more empathetic
actionality: (Nullable) Feedback on how the reframing could be more actionable
specificity: (Nullable) Feedback on how the reframing could be more specific

""")