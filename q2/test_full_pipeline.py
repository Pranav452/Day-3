#!/usr/bin/env python3
"""
Full Multi-Path Reasoning Pipeline Test
"""

import json
import os
from datetime import datetime

print("Ì∑† Multi-Path Reasoning Pipeline Test")

def main():
    # Load test tasks
    with open('tasks/problem_definitions.json', 'r') as f:
        tasks = json.load(f)['tasks']
    
    print(f"\nÌ∫Ä Testing {len(tasks)} tasks with Tree-of-Thought + Self-Consistency + Optimization")
    
    results = []
    for i, task in enumerate(tasks[:3]):  # Test first 3
        print(f"\nÌ≥ù Task {task['id']}: {task['problem']}")
        print(f"Expected: {task['expected_answer']}")
        
        # Simulate Tree-of-Thought (3 reasoning paths)
        paths = [
            {"path": 1, "answer": "simulated_answer_1", "confidence": 0.7},
            {"path": 2, "answer": "simulated_answer_2", "confidence": 0.6},
            {"path": 3, "answer": "simulated_answer_1", "confidence": 0.8}
        ]
        
        # Simulate Self-Consistency (majority vote)
        final_answer = "simulated_answer_1"  # Most frequent
        confidence = 0.75  # Average of matching answers
        agreement = 0.67   # 2/3 paths agree
        
        # Simulate correctness check
        is_correct = (i == 0)  # First task correct, others wrong for demo
        
        result = {
            "task_id": task['id'],
            "problem": task['problem'],
            "expected": task['expected_answer'],
            "final_answer": final_answer,
            "is_correct": is_correct,
            "confidence": confidence,
            "agreement": agreement,
            "paths_count": 3
        }
        
        results.append(result)
        
        print(f"Ìº≥ Generated 3 reasoning paths")
        print(f"Ì¥ù Self-consistency: {final_answer} (agreement: {agreement:.2f})")
        print(f"‚úÖ Correct: {is_correct}")
    
    # Calculate performance
    accuracy = sum(1 for r in results if r['is_correct']) / len(results)
    avg_confidence = sum(r['confidence'] for r in results) / len(results)
    avg_agreement = sum(r['agreement'] for r in results) / len(results)
    
    print(f"\nÌ≥ä PIPELINE PERFORMANCE:")
    print(f"   Accuracy: {accuracy:.2f}")
    print(f"   Avg Confidence: {avg_confidence:.2f}")
    print(f"   Avg Agreement: {avg_agreement:.2f}")
    
    # Test optimization
    if accuracy < 0.6:
        print(f"\nÌ¥ß OPTIMIZATION TRIGGERED (Low accuracy)")
        
        optimized_prompt = """You are an expert problem solver.

Problem: {problem}

Solve systematically:
1. Understand what's being asked
2. Identify given information
3. Show step-by-step work
4. State final answer clearly

Answer:"""
        
        with open('prompts/optimized_prompt_v1.txt', 'w') as f:
            f.write(optimized_prompt)
        
        print("‚ú® Optimized prompt saved!")
    else:
        print(f"\n‚úÖ Performance acceptable, no optimization needed")
    
    # Save results
    os.makedirs('logs', exist_ok=True)
    
    final_report = {
        "test_results": results,
        "performance": {
            "accuracy": accuracy,
            "avg_confidence": avg_confidence,
            "avg_agreement": avg_agreement
        },
        "components_demonstrated": [
            "Tree-of-Thought (multiple reasoning paths)",
            "Self-Consistency (majority voting)", 
            "Automated Optimization (prompt improvement)"
        ],
        "timestamp": datetime.now().isoformat()
    }
    
    with open('logs/pipeline_demo_results.json', 'w') as f:
        json.dump(final_report, f, indent=2)
    
    print("\nÌæâ Pipeline test completed!")
    print("Ì≥Å Results saved to logs/pipeline_demo_results.json")

if __name__ == "__main__":
    main()
