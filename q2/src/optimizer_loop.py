import json
import os
from datetime import datetime
from transformers import pipeline
import warnings

warnings.filterwarnings("ignore")

class PromptOptimizer:
    def __init__(self):
        print("Loading optimizer model...")
        self.model = pipeline("text-generation", model="microsoft/DialoGPT-small", pad_token_id=50256)
        print("Optimizer ready!")
        
        self.optimization_history = []
        self.performance_tracking = []
        
    def optimize_prompt(self, current_prompt_path, failure_analysis, failed_cases, iteration=1):
        """Optimize a prompt based on failure analysis - OPRO/TextGrad style"""
        
        # Load current prompt
        with open(current_prompt_path, 'r') as f:
            current_prompt = f.read()
        
        # Load optimizer prompt template
        with open('../prompts/optimizer_prompt.txt', 'r') as f:
            optimizer_template = f.read()
        
        # Format the optimizer prompt
        optimizer_prompt = optimizer_template.format(
            current_prompt=current_prompt,
            failure_analysis=self._format_failure_analysis(failure_analysis),
            failed_cases=self._format_failed_cases(failed_cases)
        )
        
        try:
            # Generate improved prompt
            response = self.model(
                optimizer_prompt,
                max_new_tokens=200,
                do_sample=True,
                temperature=0.7,
                pad_token_id=50256
            )
            
            full_text = response[0]['generated_text']
            improved_prompt = full_text[len(optimizer_prompt):].strip()
            
            # Clean up the improved prompt
            improved_prompt = self._clean_generated_prompt(improved_prompt)
            
            # Save optimized prompt
            optimized_path = f"../prompts/optimized_prompt_v{iteration}.txt"
            with open(optimized_path, 'w') as f:
                f.write(improved_prompt)
            
            # Log the optimization
            optimization_log = {
                "iteration": iteration,
                "timestamp": datetime.now().isoformat(),
                "original_prompt": current_prompt,
                "improved_prompt": improved_prompt,
                "failure_analysis": failure_analysis,
                "failed_cases": failed_cases,
                "optimization_strategy": self._identify_optimization_strategy(current_prompt, improved_prompt)
            }
            
            self.optimization_history.append(optimization_log)
            
            return optimized_path, improved_prompt
            
        except Exception as e:
            print(f"Optimization failed: {e}")
            return current_prompt_path, current_prompt
    
    def _format_failure_analysis(self, failure_analysis):
        """Format failure analysis for the optimizer prompt"""
        if isinstance(failure_analysis, dict):
            formatted = []
            for key, value in failure_analysis.items():
                formatted.append(f"- {key}: {value}")
            return "\n".join(formatted)
        return str(failure_analysis)
    
    def _format_failed_cases(self, failed_cases):
        """Format failed cases for the optimizer prompt"""
        if not failed_cases:
            return "No specific failed cases provided"
        
        formatted = []
        for i, case in enumerate(failed_cases[:3]):  # Limit to 3 examples
            if isinstance(case, dict):
                problem = case.get('problem', 'Unknown problem')
                expected = case.get('expected_answer', 'Unknown')
                actual = case.get('actual_answer', 'Unknown')
                formatted.append(f"{i+1}. Problem: {problem}\n   Expected: {expected}\n   Got: {actual}")
            else:
                formatted.append(f"{i+1}. {case}")
        
        return "\n".join(formatted)
    
    def _clean_generated_prompt(self, generated_prompt):
        """Clean and improve the generated prompt"""
        # Remove any meta-commentary
        lines = generated_prompt.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            # Skip meta-commentary lines
            if any(skip_phrase in line.lower() for skip_phrase in [
                'here is', 'here\'s', 'improved prompt:', 'new prompt:', 
                'better version:', 'revised prompt:'
            ]):
                continue
            if line and not line.startswith('#'):  # Keep content, skip comments
                cleaned_lines.append(line)
        
        cleaned = '\n'.join(cleaned_lines)
        
        # If the cleaned version is too short, use a fallback improvement
        if len(cleaned) < 50:
            cleaned = self._generate_fallback_prompt()
        
        return cleaned
    
    def _generate_fallback_prompt(self):
        """Generate a fallback improved prompt when optimization fails"""
        return """You are an expert problem solver with strong analytical skills.

Problem: {problem}

Solve this systematically:
1. Read the problem carefully and identify what is being asked
2. List the given information and constraints
3. Determine the appropriate method or formula to use
4. Show your work step by step with clear calculations
5. State your final answer in the requested format
6. Double-check your answer makes logical sense

Final Answer:"""
    
    def _identify_optimization_strategy(self, original, improved):
        """Identify what optimization strategy was applied"""
        strategies = []
        
        if "step by step" in improved.lower() and "step by step" not in original.lower():
            strategies.append("Added step-by-step guidance")
        
        if "final answer" in improved.lower() and "final answer" not in original.lower():
            strategies.append("Added explicit answer formatting")
        
        if len(improved) > len(original) * 1.2:
            strategies.append("Expanded instructions")
        elif len(improved) < len(original) * 0.8:
            strategies.append("Simplified instructions")
        
        if "example" in improved.lower() and "example" not in original.lower():
            strategies.append("Added examples")
        
        return strategies if strategies else ["General refinement"]
    
    def track_performance(self, prompt_version, task_results):
        """Track performance of different prompt versions"""
        performance_data = {
            "prompt_version": prompt_version,
            "timestamp": datetime.now().isoformat(),
            "task_results": task_results,
            "metrics": self._calculate_metrics(task_results)
        }
        
        self.performance_tracking.append(performance_data)
        return performance_data
    
    def _calculate_metrics(self, task_results):
        """Calculate performance metrics from task results"""
        if not task_results:
            return {"accuracy": 0, "avg_confidence": 0, "consistency": 0}
        
        # Calculate accuracy
        correct_count = sum(1 for result in task_results if result.get('is_correct', False))
        accuracy = correct_count / len(task_results)
        
        # Calculate average confidence
        confidences = [result.get('confidence', 0) for result in task_results]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        
        # Calculate consistency (how often paths agree)
        consistency_scores = [result.get('consistency_score', 0) for result in task_results]
        avg_consistency = sum(consistency_scores) / len(consistency_scores) if consistency_scores else 0
        
        return {
            "accuracy": accuracy,
            "avg_confidence": avg_confidence,
            "consistency": avg_consistency,
            "total_tasks": len(task_results)
        }
    
    def should_optimize(self, performance_metrics, threshold=0.6):
        """Determine if prompt optimization is needed"""
        accuracy = performance_metrics.get('accuracy', 0)
        consistency = performance_metrics.get('consistency', 0)
        
        # Trigger optimization if accuracy or consistency is below threshold
        if accuracy < threshold or consistency < threshold:
            return True, f"Performance below threshold - Accuracy: {accuracy:.2f}, Consistency: {consistency:.2f}"
        
        return False, "Performance acceptable"
    
    def generate_optimization_report(self):
        """Generate a report of all optimizations performed"""
        if not self.optimization_history:
            return "No optimizations performed yet."
        
        report = "# Prompt Optimization Report\n\n"
        
        for i, opt in enumerate(self.optimization_history):
            report += f"## Optimization {i+1} (v{opt['iteration']})\n"
            report += f"**Timestamp:** {opt['timestamp']}\n"
            report += f"**Strategy:** {', '.join(opt['optimization_strategy'])}\n"
            report += f"**Issues Addressed:** {self._format_failure_analysis(opt['failure_analysis'])}\n\n"
        
        # Add performance comparison
        if len(self.performance_tracking) > 1:
            report += "## Performance Comparison\n"
            for perf in self.performance_tracking:
                version = perf['prompt_version']
                metrics = perf['metrics']
                report += f"**{version}:** Accuracy: {metrics['accuracy']:.2f}, "
                report += f"Confidence: {metrics['avg_confidence']:.2f}, "
                report += f"Consistency: {metrics['consistency']:.2f}\n"
        
        return report
    
    def save_optimization_logs(self, log_path="../logs/optimization_logs.json"):
        """Save all optimization data to logs"""
        log_data = {
            "optimization_history": self.optimization_history,
            "performance_tracking": self.performance_tracking,
            "summary": {
                "total_optimizations": len(self.optimization_history),
                "best_performance": max(self.performance_tracking, key=lambda x: x['metrics']['accuracy']) if self.performance_tracking else None
            }
        }
        
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        print(f"Optimization logs saved to {log_path}") 