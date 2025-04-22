#!/usr/bin/env python3
"""
Persona-based prompting system using OpenAI Chat API, now displaying chain-of-thought alongside final response.
"""
import os
import openai
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI()

class Persona:
    def __init__(self, name, tone, traits, actions, example):
        self.name = name
        self.tone = tone
        self.traits = traits
        self.actions = actions
        self.example = example

    def build_system_prompt(self):
        # Instruction to include chain-of-thought in the output
        return (
            f"You are to role-play as {self.name} with the following characteristics:\n"
            f"- Tone: {self.tone}\n"
            f"- Traits: {', '.join(self.traits)}\n"
            f"- Actions: {', '.join(self.actions)}\n\n"
            f"Example interaction:\n{self.example}\n\n"
            "When responding, first show your chain-of-thought steps, each prefixed with 'Thought:'.\n"
            "After the chain-of-thought, output the final reply prefixed with 'Response:'."
        )


def ask_persona(persona_prompt, user_query):
    messages = [
        {"role": "system", "content": persona_prompt},
        {"role": "user", "content": user_query}
    ]
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.8,
        max_tokens=400
    )
    return response.choices[0].message.content



def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: Set the OPENAI_API_KEY environment variable.")
        return
    openai.api_key = api_key

    # Define the Amitabh Bachchan persona
    amitabh = Persona(
        name="Amitabh Bachchan",
        tone="warm, dignified, and eloquent",
        traits=["wise", "humorous", "empathetic"],
        actions=[
            "open with 'Deviyon aur Sajjanon'",
            "offer respectful greeting",
            "share personal anecdote",
            "provide thoughtful advice"
        ],
        example=(
            "User: Sir, how do I stay motivated during hard times?\n"
            "Amitabh Bachchan (thinking): I recall the early days of my career, the struggles and hopes...\n"
            "Thought: Recall significant personal struggles to empathize.\n"
            "Thought: Structure advice as an inspiring narrative.\n"
            "Response: Deviyon aur Sajjanon, my dear friend, in moments of hardship, remember that every challenge is an opportunity in disguise..."
        )
    )

    system_prompt = amitabh.build_system_prompt()

    print("Persona: Amitabh Bachchan (with chain-of-thought)")
    print("Type your message and press Enter. To end the session, press Ctrl+C.")
    try:
        while True:
            user_input = input("> ")
            if not user_input.strip():
                continue
            try:
                reply = ask_persona(system_prompt, user_input)
                print(reply + "\n")
            except Exception as e:
                print(f"Error communicating with OpenAI: {e}")
    except KeyboardInterrupt:
        print("\nSession ended. Goodbye!")

if __name__ == "__main__":
    main()
