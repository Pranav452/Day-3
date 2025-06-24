# 🧠 Prompt Engineering Lab: EdTech Math Tutor

## Domain: Educational Technology (Class 6-10 Math)

A mini-agent using TinyLlama for solving and explaining math problems for middle school students.

### Representative User Tasks:
1. Solve linear equations step-by-step
2. Explain geometric formulas with examples  
3. Generate practice problems for specific topics

### Prompt Strategies Implemented:
- **Zero-shot**: Direct instruction with no examples
- **Few-shot**: Instruction + 2-3 examples
- **Chain-of-thought (CoT)**: Step-by-step reasoning
- **Self-ask**: Model asks sub-questions to reach answer

### Usage:
```bash
python main.py
```

### Model: TinyLlama (1.1B parameters)
- Lightweight for low-resource systems
- Good for educational content generation
- Requires careful prompt engineering due to size limitations 