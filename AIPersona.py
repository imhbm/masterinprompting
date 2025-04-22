import os
from openai import OpenAI
import google.generativeai as genai
from typing import Dict, List, Optional
import re
from dotenv import load_dotenv

load_dotenv()

class AIPersona:
    def __init__(self, config: Dict):
        """Initialize an AI persona with configurable traits and behaviors"""
        self.name = config.get("name", "Assistant")
        self.tone = config.get("tone", "helpful")
        self.traits = config.get("traits", [])
        self.role = config.get("role", "general assistant")
        self.actions = config.get("actions", [])
        self.signature_phrases = config.get("signature_phrases", [])
        self.knowledge_domains = config.get("knowledge_domains", [])
        self.examples = config.get("examples", [])
        
    def get_prompt_prefix(self) -> str:
        """Generate the persona-specific instruction part of the prompt"""
        traits_str = ", ".join(self.traits)
        
        prefix = f"""
You are embodying {self.name}, who is known for a {self.tone} communication style.
Your key traits include: {traits_str}.
You serve as a {self.role} and should maintain this expertise in your responses.

Follow these specific actions in your response:
"""
        for action in self.actions:
            prefix += f"- {action}\n"
            
        if self.signature_phrases:
            phrases = ", ".join([f'"{phrase}"' for phrase in self.signature_phrases])
            prefix += f"\nIncorporate phrases like {phrases} naturally in your response.\n"
            
        return prefix

class AIModelManager:
    def __init__(self):
        """Initialize API configurations for multiple AI models"""
        # Load environment variables for API keys
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.google_api_key = os.getenv("GEMINI_API_KEY")
        
        # Configure APIs
        if self.openai_api_key:
            self.openai_client = OpenAI(api_key=self.openai_api_key)
        else:
            self.openai_client = None
            print("Warning: OpenAI API key not found")
        
        if self.google_api_key:
            genai.configure(api_key=self.google_api_key)
        else:
            print("Warning: Google API key not found")
            
        # Model configurations - updated to newer models
        self.default_openai_model = "gpt-4o"
        self.default_gemini_model = "gemini-1.5-flash-001"
    
    def ask_openai(self, prompt: str, model: Optional[str] = None) -> str:
        """Query OpenAI's text models using the latest client"""
        if not self.openai_client:
            return "Error: OpenAI API key not configured"
            
        model = model or self.default_openai_model
        
        try:
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error with OpenAI API: {str(e)}"
    
    def ask_gemini(self, prompt: str, model: Optional[str] = None) -> str:
        """Query Google's Gemini text models"""
        model_name = model or self.default_gemini_model
        
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error with Gemini API: {str(e)}"

class ChainOfThoughtProcessor:
    @staticmethod
    def build_cot_prompt(query: str, persona_prefix: str) -> str:
        """Build a chain-of-thought prompt with persona instructions"""
        cot_instructions = """
Let's solve this step by step:
1. First, understand what's being asked
2. Consider the relevant context and background
3. Explore possible approaches to address the question
4. Analyze the pros and cons of each approach
5. Formulate a thoughtful, comprehensive response that reflects your persona
"""
        
        combined_prompt = f"{persona_prefix}\n\n{cot_instructions}\n\nQuestion: {query}\n\nThinking process:"
        return combined_prompt
    
    @staticmethod
    def format_final_response(cot_response: str) -> str:
        """Extract the final answer without showing the reasoning process"""
        # This is simplified - you might want to use regex or more sophisticated parsing
        if "Final Answer:" in cot_response:
            parts = cot_response.split("Final Answer:")
            if len(parts) > 1:
                return parts[1].strip()
        
        # If no specific final answer section, return the last paragraph
        paragraphs = cot_response.split("\n\n")
        return paragraphs[-1].strip()

class AIResponseEvaluator:
    def __init__(self, model_manager: AIModelManager):
        self.model_manager = model_manager
    
    def evaluate_responses(self, query: str, responses: List[str]) -> int:
        """Evaluate multiple responses and return the index of the best one"""
        if len(responses) == 1:
            return 0
            
        response_text = "\n\n".join([f"Response {i+1}: {resp}" for i, resp in enumerate(responses)])
        
        eval_prompt = f"""
As an objective evaluator, compare these responses to the following query:
"{query}"

{response_text}

Consider:
1. Accuracy and factual correctness
2. Completeness in addressing the query
3. Clarity and coherence
4. Helpfulness and actionability
5. Appropriate tone and style

Analyze each response based on these criteria, then identify which response number (1, 2, etc.) is the best overall.
Return ONLY the number of the best response.
"""
        
        result = self.model_manager.ask_openai(eval_prompt, "gpt-4o")
        
        # Extract just the number from the response
        numbers = re.findall(r'\d+', result)
        if numbers:
            best_index = int(numbers[0]) - 1  # Convert to zero-indexed
            return min(best_index, len(responses) - 1)  # Ensure we don't exceed array bounds
        
        return 0  # Default to first response if parsing fails

class AIPersonaSystem:
    def __init__(self):
        self.model_manager = AIModelManager()
        self.evaluator = AIResponseEvaluator(self.model_manager)
        self.cot_processor = ChainOfThoughtProcessor()
        self.personas = {}
        
    def register_persona(self, persona_id: str, config: Dict) -> None:
        """Register a new persona with the system"""
        self.personas[persona_id] = AIPersona(config)
        
    def get_response(self, 
                    persona_id: str, 
                    query: str,
                    use_cot: bool = True,
                    compare_models: bool = True) -> str:
        """Generate a persona-based response to a query"""
        
        # Get the persona or use a default if not found
        persona = self.personas.get(persona_id)
        if not persona:
            # Create a basic default persona
            persona = AIPersona({"name": "Assistant"})
        
        # Get persona-specific prompt prefix
        persona_prefix = persona.get_prompt_prefix()
        
        # Build the full prompt
        if use_cot:
            prompt = self.cot_processor.build_cot_prompt(query, persona_prefix)
        else:
            prompt = f"{persona_prefix}\n\nQuestion: {query}"
        
        responses = []
        
        # Get responses from different models - text only
        openai_response = self.model_manager.ask_openai(prompt)
        responses.append(openai_response)
        
        if compare_models:
            gemini_response = self.model_manager.ask_gemini(prompt)
            responses.append(gemini_response)
        
        # Evaluate responses if we have multiple
        if len(responses) > 1:
            best_index = self.evaluator.evaluate_responses(query, responses)
            best_response = responses[best_index]
        else:
            best_response = responses[0]
        
        # Format the response if using chain-of-thought
        if use_cot:
            return self.cot_processor.format_final_response(best_response)
        
        return best_response

# Example usage
if __name__ == "__main__":
   
    # Check for API keys first
    if not os.getenv("OPENAI_API_KEY"):
        print("WARNING: OPENAI_API_KEY environment variable not set.")
        print("Please set your OpenAI API key as an environment variable:")
        print("  On Windows: set OPENAI_API_KEY=your_api_key_here")
        print("  On Mac/Linux: export OPENAI_API_KEY=your_api_key_here")
    
    if not os.getenv("GEMINI_API_KEY"):
        print("WARNING: GEMINI_API_KEY environment variable not set.")
        print("Please set your GEMINI_API_KEY as an environment variable:")
        print("  On Windows: set GEMINI_API_KEY=your_api_key_here")
        print("  On Mac/Linux: export GEMINI_API_KEY=your_api_key_here")
    
    # Initialize the AI persona system
    ai_system = AIPersonaSystem()
    
    # Create and register the Amitabh Bachchan persona
    amitabh_persona = {
        "name": "Amitabh Bachchan",
        "tone": "warm and dignified",
        "traits": ["wise", "humorous", "empathetic"],
        "role": "life mentor",
        "actions": [
            "begin with a thoughtful greeting",
            "share a relevant personal anecdote",
            "provide insightful advice with compassion",
            "conclude with an uplifting message"
        ],
        "signature_phrases": [
            "Deviyon aur Sajjanon",
            "Bahut khoob",
            "Zindagi ek sangharsh hai"
        ],
        "knowledge_domains": ["life philosophy", "personal growth", "Indian culture", "resilience"],
        "examples": [
            "Life is a game of challenges, but every challenge brings an opportunity to rise higher."
        ]
    }
    
    ai_system.register_persona("amitabh", amitabh_persona)
    
    # Example text query
    user_query = "what is love?"
    print("\n=== Text-Only Query ===")
    response = ai_system.get_response(
        persona_id="amitabh",
        query=user_query,
        use_cot=True,
        compare_models=True
    )
    print(response)