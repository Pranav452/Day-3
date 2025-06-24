import json
from collections import Counter
import re

class SelfConsistency:
    def __init__(self):
        pass
    
    def aggregate_answers(self, reasoning_paths):
        """Aggregate multiple reasoning paths using self-consistency"""
        if not reasoning_paths:
            return {"final_answer": "No paths provided", "confidence": 0.0, "method": "none"}
        
        # Extract answers and filter out errors
        valid_paths = [path for path in reasoning_paths if path["final_answer"] != "Error"]
        
        if not valid_paths:
            return {"final_answer": "All paths failed", "confidence": 0.0, "method": "error"}
        
        # Try different aggregation methods
        majority_result = self._majority_vote(valid_paths)
        confidence_result = self._confidence_weighted(valid_paths)
        similarity_result = self._semantic_similarity(valid_paths)
        
        # Choose the best method based on confidence
        methods = [
            ("majority_vote", majority_result),
            ("confidence_weighted", confidence_result), 
            ("semantic_similarity", similarity_result)
        ]
        
        best_method, best_result = max(methods, key=lambda x: x[1]["confidence"])
        best_result["method"] = best_method
        best_result["all_answers"] = [path["final_answer"] for path in valid_paths]
        best_result["path_count"] = len(valid_paths)
        
        return best_result
    
    def _majority_vote(self, paths):
        """Simple majority voting"""
        answers = [path["final_answer"] for path in paths]
        answer_counts = Counter(answers)
        
        if not answer_counts:
            return {"final_answer": "No valid answers", "confidence": 0.0}
        
        most_common_answer, count = answer_counts.most_common(1)[0]
        confidence = count / len(answers)
        
        return {
            "final_answer": most_common_answer,
            "confidence": confidence,
            "vote_distribution": dict(answer_counts)
        }
    
    def _confidence_weighted(self, paths):
        """Weight answers by path confidence scores"""
        if not paths:
            return {"final_answer": "No paths", "confidence": 0.0}
        
        # Group by answer and sum confidences
        answer_weights = {}
        for path in paths:
            answer = path["final_answer"]
            confidence = path["confidence"]
            
            if answer in answer_weights:
                answer_weights[answer] += confidence
            else:
                answer_weights[answer] = confidence
        
        if not answer_weights:
            return {"final_answer": "No weighted answers", "confidence": 0.0}
        
        # Choose answer with highest total confidence
        best_answer = max(answer_weights, key=answer_weights.get)
        total_weight = sum(answer_weights.values())
        confidence = answer_weights[best_answer] / total_weight if total_weight > 0 else 0
        
        return {
            "final_answer": best_answer,
            "confidence": confidence,
            "weight_distribution": answer_weights
        }
    
    def _semantic_similarity(self, paths):
        """Group similar answers together"""
        if not paths:
            return {"final_answer": "No paths", "confidence": 0.0}
        
        # Simple similarity: normalize answers and group
        normalized_answers = {}
        for path in paths:
            answer = path["final_answer"]
            normalized = self._normalize_answer(answer)
            
            if normalized in normalized_answers:
                normalized_answers[normalized].append(path)
            else:
                normalized_answers[normalized] = [path]
        
        if not normalized_answers:
            return {"final_answer": "No similar answers", "confidence": 0.0}
        
        # Choose the group with most paths
        best_group = max(normalized_answers.values(), key=len)
        best_answer = best_group[0]["final_answer"]  # Take first answer from best group
        confidence = len(best_group) / len(paths)
        
        return {
            "final_answer": best_answer,
            "confidence": confidence,
            "similar_groups": {k: len(v) for k, v in normalized_answers.items()}
        }
    
    def _normalize_answer(self, answer):
        """Normalize answer for similarity comparison"""
        if not answer:
            return ""
        
        # Convert to lowercase and remove extra whitespace
        normalized = answer.lower().strip()
        
        # Extract numbers if present
        numbers = re.findall(r'\d+\.?\d*', normalized)
        if numbers:
            return f"number_{numbers[0]}"
        
        # Handle common answer patterns
        if any(word in normalized for word in ['yes', 'true', 'correct']):
            return "affirmative"
        elif any(word in normalized for word in ['no', 'false', 'incorrect']):
            return "negative"
        
        # Return first meaningful word
        words = normalized.split()
        meaningful_words = [w for w in words if len(w) > 2 and not w.isdigit()]
        return meaningful_words[0] if meaningful_words else normalized
    
    def evaluate_consistency(self, reasoning_paths):
        """Evaluate how consistent the reasoning paths are"""
        if not reasoning_paths:
            return {"consistency_score": 0, "analysis": "No paths to evaluate"}
        
        valid_paths = [path for path in reasoning_paths if path["final_answer"] != "Error"]
        
        if len(valid_paths) < 2:
            return {"consistency_score": 0, "analysis": "Not enough valid paths for consistency check"}
        
        # Check answer consistency
        answers = [path["final_answer"] for path in valid_paths]
        unique_answers = set(answers)
        answer_consistency = 1 - (len(unique_answers) - 1) / len(valid_paths)
        
        # Check reasoning quality consistency
        confidences = [path["confidence"] for path in valid_paths]
        avg_confidence = sum(confidences) / len(confidences)
        confidence_variance = sum((c - avg_confidence) ** 2 for c in confidences) / len(confidences)
        confidence_consistency = max(0, 1 - confidence_variance)
        
        overall_consistency = (answer_consistency + confidence_consistency) / 2
        
        analysis = {
            "total_paths": len(reasoning_paths),
            "valid_paths": len(valid_paths),
            "unique_answers": len(unique_answers),
            "answer_consistency": answer_consistency,
            "confidence_consistency": confidence_consistency,
            "avg_confidence": avg_confidence
        }
        
        return {
            "consistency_score": overall_consistency,
            "analysis": analysis
        } 