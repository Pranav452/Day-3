# 🧠 Prompt Engineering Pipeline: Multi-Path Reasoning + Automated Optimization

## Objective
Advanced prompt engineering pipeline that combines:
- **Tree-of-Thought (ToT)**: Multiple reasoning paths per problem
- **Self-Consistency**: Aggregating answers through consensus
- **Automated Prompt Optimization**: OPRO/TextGrad-style feedback loops

## Domain: Math Word Problems + Logic Puzzles

### Key Features
- Generates 3-5 reasoning paths per query
- Uses majority voting for final answers
- Automatically improves prompts based on failures
- Tracks performance across prompt versions

## Setup & Usage

### Dependencies
```bash
pip install transformers torch
```

### Run Pipeline
```bash
cd src/
python main_pipeline.py
```

### Project Structure
```
q2/
├── README.md
├── tasks/ (problem definitions)
├── prompts/ (initial + optimized prompts)
├── src/ (pipeline implementation)
├── logs/ (reasoning paths, optimization logs)
└── evaluation/ (metrics + reflection)
```

## Model Used
- **microsoft/DialoGPT-small** via Transformers
- Local model approach (no external APIs required)
- Lightweight but sufficient for demonstrating advanced prompt techniques

## Key Innovations
1. **Multi-path reasoning** catches errors through diversity
2. **Self-consistency** filters out hallucinations
3. **Automated optimization** learns from failures
4. **Performance tracking** shows measurable improvements 