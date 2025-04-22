#step by step breaking down the chat chain of thought
from dotenv import load_dotenv
import openai
import json

load_dotenv()
client = openai.OpenAI()
system_prompt = """
you are an AI assintant who is expert in breaking down the problem in to steps and solving it step by step.

For the given user Input, analyse the input and breakdown the problem step by step.
Atleast think 5-6 steps on how to solve the problem before solving it down.

The steps are you get a user input, then you think for several time, with explaination 
and finally you validate the output as well before giving final result.

follow the step in sequence  that is "analysise", "think", "output", "validate" and finally "result".

Rules:
1. follow the strict JSON output as per output schema
2. Always perform one step at a time and wait for next input
3. carefully analsye the user query.

output format:
{{ step: "string", content: "string" }}

Example:
Input: what is 2+2.
Output: {{ step:"analyse", content:"Alright! the user is interested in maths query and user is asking a basic arthimetic operation" }}
Output: {{ step: "think", content:"To perform the addition I must go from left to right and add all the operands}}
Output: {{ step: "output", content:"2+2 = 4" }}
Output: {{ step: "validate", content:"I have checked the result and it is correct seems like 4 is correct ans for 2+2" }}
Output: {{ step: "result", content:"2 + 2 = 4 and that is calculated by adding all numbers" }}



"""

result = client.chat.completions.create(
    model="gpt-4o",
    response_format={"type": "json_object"},
    max_tokens=100,
    temperature=0.5,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "what is 3+4*5"},
        {"role": "assistant", "content": json.dumps({
            "step": "analyse",
            "content": "The user is asking for the result of a mathematical expression that involves both addition and multiplication. This requires understanding of the order of operations."
        })},
        {"role": "assistant", "content": json.dumps({
            "step": "think",
            "content": "To solve this expression correctly, I must apply the order of operations, often remembered by the acronym PEMDAS (Parentheses, Exponents, Multiplication and Division (from left to right), Addition and Subtraction (from left to right))."
        })},
         {"role": "assistant", "content": json.dumps({
            "step": "think",
            "content": "According to the order of operations, multiplication should be performed before addition. Therefore, I need to first calculate 4 * 5, and then add the result to 3."
        })},
        {"role": "assistant", "content": json.dumps({
            "step": "output",
            "content": "First, calculate the multiplication: 4 * 5 = 20. Then, add the result to 3: 3 + 20 = 23."
        })},
        {"role": "assistant", "content": json.dumps({
            "step": "validate",
            "content": "I have reviewed the steps: Multiplication was done first (4 * 5 = 20), then addition (3 + 20 = 23). The operations follow the correct order, so the result seems accurate."
        })},
         {"role": "assistant", "content": json.dumps({
            "step": "result",
            "content": "The result of the expression 3 + 4 * 5, following the order of operations, is 23."
        })}
    ]
)

print(result.choices[0].message.content)