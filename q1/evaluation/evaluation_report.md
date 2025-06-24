# Prompt Evaluation Report

## EdTech Math Tutor - Local Model Performance Analysis

### Test Queries Used:
1. Solve 3x + 5 = 14
2. What is the area of a triangle with base 8cm and height 6cm?
3. Calculate 25% of 160
4. If a rectangle has length 12cm and width 7cm, what is its perimeter?
5. Solve for y: 2y - 8 = 10

### Evaluation Metrics:

#### 1. Accuracy (Expected vs Actual Output)
- **Zero-Shot**: 4.0/10
- **Few-Shot**: 4.0/10
- **Chain-Of-Thought**: 2.0/10
- **Self-Ask**: 0.0/10

#### 2. Reasoning Clarity (for CoT)
- Clear step-by-step explanation: Variable quality
- Easy to follow for students: Limited due to model constraints

#### 3. Hallucination Score (Manual Judgment)
- **Zero-Shot**: 3 factual errors
- **Few-Shot**: 3 factual errors
- **Chain-Of-Thought**: 4 factual errors
- **Self-Ask**: 5 factual errors

#### 4. Consistency
- Similar queries produce consistent outputs: Variable (6/10)

### Observations:
- **Best performing strategy**: Few-shot (provides examples)
- **Most reliable for math problems**: Few-shot with mathematical examples
- **Recommended for Class 6-10**: Few-shot or Chain-of-thought

### Key Findings:
1. **Model Limitations**: Local model struggles with precise mathematical calculations
2. **Prompt Strategy Impact**: Few-shot examples help guide the model better
3. **Chain-of-thought**: Shows reasoning process but accuracy varies
4. **Zero-shot**: Quick responses but often lacks mathematical precision

### Strategies to Reduce Hallucination:
1. Add "If unsure, say you don't know" to prompts
2. Use more constrained, specific prompts
3. Include validation steps in CoT prompts
4. Provide more mathematical examples in few-shot prompts