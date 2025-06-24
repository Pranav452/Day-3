import json
import random
from transformers import pipeline
import warnings

warnings.filterwarnings("ignore")

class ReasoningTree:
    def __init__(self):
        print("Loading model for Tree-of-Thought reasoning...")
        self.model = pipeline("text-generation", model="microsoft/DialoGPT-small", pad_token_id=50256)
        print("Model loaded successfully!")
        
    def generate_reasoning_paths(self, problem, prompt_template, num_paths=3):
        """Generate multiple reasoning paths for a single problem"""
        paths = []
        
        # Load prompt template
        with open(prompt_template, 'r') as f:
            template = f.read()
        
        for path_id in range(num_paths):
            # Vary the approach slightly for each path
            variations = [
                "Think through this step by step:",
                "Let me solve this carefully:",
                "Breaking this down systematically:",
                "Analyzing this problem:"
            ]
            
            # Create varied prompt
            prompt = template.format(problem=problem)
            prompt = prompt.replace("Think through this carefully:", variations[path_id % len(variations)])
            
            try:
                # Generate response with different seeds for diversity
                response = self.model(
                    prompt, 
                    max_new_tokens=100, 
                    do_sample=True, 
                    temperature=0.8,
                    top_p=0.9,
                    pad_token_id=50256
                )
                
                full_text = response[0]['generated_text']
                reasoning = full_text[len(prompt):].strip()
                
                # Extract final answer
                final_answer = self._extract_final_answer(reasoning)
                
                path_data = {
                    "path_id": path_id + 1,
                    "prompt_variation": variations[path_id % len(variations)],
                    "full_reasoning": reasoning,
                    "final_answer": final_answer,
                    "confidence": self._estimate_confidence(reasoning)
                }
                
                paths.append(path_data)
                
            except Exception as e:
                paths.append({
                    "path_id": path_id + 1,
                    "prompt_variation": variations[path_id % len(variations)],
                    "full_reasoning": f"Error: {str(e)}",
                    "final_answer": "Error",
                    "confidence": 0.0
                })
        
        return paths
    
    def _extract_final_answer(self, reasoning):
        """Extract the final answer from reasoning text"""
        # Look for common answer patterns
        lines = reasoning.split('\n')
        for line in lines:
            line = line.strip().lower()
            if any(keyword in line for keyword in ['answer:', 'final answer:', 'result:', 'solution:']):
                # Extract the part after the keyword
                for keyword in ['answer:', 'final answer:', 'result:', 'solution:']:
                    if keyword in line:
                        answer = line.split(keyword)[1].strip()
                        return answer if answer else "No clear answer"
        
        # If no explicit answer found, try to get the last meaningful sentence
        meaningful_lines = [line for line in lines if line.strip() and not line.strip().startswith(('Step', 'First', 'Next'))]
        if meaningful_lines:
            return meaningful_lines[-1].strip()
        
        return "No clear answer found"
    
    def _estimate_confidence(self, reasoning):
        """Estimate confidence based on reasoning quality"""
        if not reasoning or "error" in reasoning.lower():
            return 0.0
        
        confidence_indicators = [
            "step by step", "therefore", "because", "so", "thus",
            "final answer", "result", "solution"
        ]
        
        score = 0
        for indicator in confidence_indicators:
            if indicator in reasoning.lower():
                score += 1
        
        # Normalize to 0-1 range
        return min(score / len(confidence_indicators), 1.0)
    
    def evaluate_tree_quality(self, paths):
        """Evaluate the overall quality of the reasoning tree"""
        if not paths:
            return {"diversity": 0, "avg_confidence": 0, "error_rate": 1}
        
        # Calculate diversity (unique answers)
        answers = [path["final_answer"] for path in paths if path["final_answer"] != "Error"]
        unique_answers = len(set(answers))
        diversity = unique_answers / len(paths) if paths else 0
        
        # Calculate average confidence
        confidences = [path["confidence"] for path in paths]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        
        # Calculate error rate
        errors = sum(1 for path in paths if path["final_answer"] == "Error")
        error_rate = errors / len(paths)
        
        return {
            "diversity": diversity,
            "avg_confidence": avg_confidence,
            "error_rate": error_rate,
            "total_paths": len(paths)
        } 