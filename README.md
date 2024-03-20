# Nonty
Nonty is a QA-bot fine-tuned on 1k+ situation-thought-trap-pattern tuples in the Hinglish language.
The original dataset is sourced from the paper **Cognitive Reframing of Negative Thoughts through Human-Language Model Interaction.**

This dataset was translated into Hinglish multiple times using different methods, including but not limited to Machine-Translation, an Open-Hathi model
fine-tuned on Hinglish-English translation pairs, and GPT-4 with low-context prompting.

After this translation process, we transform the data into Assistant format to enable fine-tuning on GPT-3.5-Turbo, which gives us two models:

1. One takes in a negative thought (in Hinglish) and outputs the closest negative-thought-pattern present in that thought.
2. The other takes in a situation, a thought, and outputs a reframed thought - accounting for any cognitive dissonances present in the initial thought.


The user inputs a thought and a situation. We run our models above on these inputs to give us starting points.
I found that the fine-tuned models are able to pick up on thought patterns accurately but are largely unable
to articulate their reframings properly in Hinglish, possibly due to a low frequency of Hindi/Hinglish data 
in their pre-training data.

As such, in order to improve upon the reframed thought outputted by Nonty, I decided to 
employ a critic-respondent approach where one LLM critiques the initial thought trap identified 
and the reframed thought based on attributes defined in the paper above, and another LLM modifies 
the answers to better meet the critic's criteria, allowing for an iterative convergence.






