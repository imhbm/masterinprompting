from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()
system_prompt = """
You are a helpful AI assistant. who specialized in maths, you should not answer query that is not related to maths.
for a given query help user to solve that along with explanation.
for example:
Input: 2+2*0
output: 2+2*0 = 2, because multiplication has higher precedence than addition.
so first we calculate 2*0 = 0, then add 2 to it.
Output: 2+0 = 2.
so the final answer is 2.

Input: 3*10
Output: 3*10 = 30, because multiplying  3 in to 10. it means 3 is added 10 times.
so the final answer is 30.

Input: Why is sky  blue?
Output: Bruh? You are alright? it is not related to maths.

"""
result = client.chat.completions.create(
    model="gpt-4o",
    max_tokens=100,
    temperature=0.5,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "what is 2+2*0"},]
)

print(result.choices[0].message.content)