from transformers import pipeline
import json
import warnings

warnings.filterwarnings("ignore")

class EdTechMathTutor:
    def __init__(self):
        print("Loading TinyLlama model (this may take a moment)...")
        self.model = pipeline("text-generation", model="microsoft/DialoGPT-small", pad_token_id=50256)
        print("Model loaded successfully!")
        
    def zero_shot_prompt(self, question):
        """Direct instruction with no examples"""
        prompt = f"""You are a helpful math tutor for students in class 6-10. 
Solve this math problem clearly and accurately:

{question}

Answer:"""
        return self._query_model(prompt)
    
    def few_shot_prompt(self, question):
        """Instruction with 2-3 examples"""
        prompt = f"""You are a helpful math tutor for students in class 6-10. Here are some examples:

Q: Solve 2x + 3 = 7
A: Subtract 3 from both sides: 2x = 4. Divide by 2: x = 2

Q: Find area of rectangle with length 5cm and width 3cm
A: Area = length × width = 5 × 3 = 15 cm²

Q: What is 15% of 80?
A: 15% = 15/100 = 0.15. So 0.15 × 80 = 12

Now solve this problem:
Q: {question}
A:"""
        return self._query_model(prompt)
    
    def chain_of_thought_prompt(self, question):
        """Step-by-step reasoning"""
        prompt = f"""You are a math tutor. Think step by step to solve this problem.

Problem: {question}

Let me think through this step by step:
1. First, I need to understand what the problem is asking
2. Then identify the relevant formula or method
3. Apply the method step by step
4. Check my answer

Step-by-step solution:"""
        return self._query_model(prompt)
    
    def self_ask_prompt(self, question):
        """Model asks sub-questions"""
        prompt = f"""You are a math tutor. Before solving, ask yourself helpful sub-questions.

Problem: {question}

Let me ask myself some questions to solve this:
- What type of problem is this?
- What information do I have?
- What formula or method should I use?
- What are the steps needed?

Self-questioning approach:"""
        return self._query_model(prompt)
    
    def _query_model(self, prompt):
        """Send prompt to local model"""
        try:
            response = self.model(prompt, max_new_tokens=50, do_sample=True, temperature=0.7, pad_token_id=50256)
            full_text = response[0]['generated_text']
            answer = full_text[len(prompt):].strip()
            # Take first meaningful line
            answer = answer.split('\n')[0].strip()
            return answer if answer else "Model could not generate a response"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def run_interactive(self):
        """Interactive CLI for testing different prompt strategies"""
        print("🧠 EdTech Math Tutor - Prompt Engineering Lab")
        print("Choose a prompt strategy:")
        print("1. Zero-shot")
        print("2. Few-shot") 
        print("3. Chain-of-thought")
        print("4. Self-ask")
        print("5. Exit")
        
        while True:
            choice = input("\nEnter choice (1-5): ")
            
            if choice == "5":
                break
                
            if choice in ["1", "2", "3", "4"]:
                question = input("Enter your math question: ")
                print("\n" + "="*50)
                
                if choice == "1":
                    print("ZERO-SHOT RESPONSE:")
                    response = self.zero_shot_prompt(question)
                elif choice == "2":
                    print("FEW-SHOT RESPONSE:")
                    response = self.few_shot_prompt(question)
                elif choice == "3":
                    print("CHAIN-OF-THOUGHT RESPONSE:")
                    response = self.chain_of_thought_prompt(question)
                elif choice == "4":
                    print("SELF-ASK RESPONSE:")
                    response = self.self_ask_prompt(question)
                
                print(response)
                print("="*50)
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    tutor = EdTechMathTutor()
    tutor.run_interactive() 