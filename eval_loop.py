from prompts import improve_prompt, criticise_prompt
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from load_dotenv import load_dotenv
import json


load_dotenv()

def eval_loop(situation, thought, reframed, trap, max_iter=1):
    llm = ChatOpenAI(model='gpt-4')
    improve_chain = LLMChain(llm=llm, prompt=improve_prompt)
    critique_chain = LLMChain(llm=llm, prompt=criticise_prompt)
    critique_results = critique_chain.run(situation=situation, thought=thought, pattern=trap, reframing=reframed)
    critique_results = json.loads(critique_results)
    is_ok = critique_results.get("is_ok", False)
    iterations = 0
    while not is_ok:
        if iterations>=max_iter:
            break
        del critique_results["is_ok"]
        lacking = "\n".join([critique_results[key] for key in critique_results.keys() if critique_results[key] is not None])
        improve_results = improve_chain.run(situation=situation, thought=thought, pattern=trap, reframing=reframed, lacking=lacking)
        improve_results = json.loads(improve_results)
        pattern, framing, rationale = improve_results["pattern"], improve_results["reframing"], improve_results["rationale"]
        critique_results = critique_chain.run(situation=situation, thought=thought, pattern=pattern, reframing=framing)
        print(critique_results)
        critique_results = json.loads(critique_results)
        is_ok = critique_results.get("is_ok", False)
        
    return pattern, framing, rationale
    
