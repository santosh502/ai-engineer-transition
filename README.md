# AI Engineer Transition

A **practical, 18-week program** for experienced software engineers to master AI engineering-from LLM fundamentals through building production agents.

---

## What This Is

This repo combines:
- **Learning materials** - Theory + hands-on code across 5 structured LLM modules
- **Working projects** - Two production-like applications (text→JSON extractor, hello-world LLM)
- **Progress tracker** - Interactive 18-week curriculum with tasks, resources, and checkpoints

**Ideal for**: Software engineers with 5+ years experience who want to build real AI systems (not just prompt ChatGPT).

---

## Quick Start (Choose Your Path)

### Just want to learn?
1. Open [ai_engineering/README.md](ai_engineering/README.md)
2. Start with [ai_engineering/llm/01_llm_fundamentals.md](ai_engineering/llm/01_llm_fundamentals.md)
3. Work through in order: fundamentals → examples → reference → hard problems → prompting

**Time**: 1 week to understand the basics. 3-4 weeks to go deep.

### Want to build projects?
1. Open [tracker.html](https://santosh502.github.io/ai-engineer-transition/tracker.html) in your browser (no server needed)
2. Start Week 1 tasks to set up environment
3. Follow Weeks 2-7 (RAG from scratch) + Weeks 8-12 (Agents) + Weeks 13-18 (Capstone)
4. See [projects/](projects/) for working examples

**Time**: 18 weeks full commitment. Scales down to 4-6 weeks if you accelerate.

### Want to understand the structure first?
Keep reading this file.

---

## Repository Structure

```
ai-engineer-transition/
├── README.md                          # You are here
├── tracker.html                       # Interactive 18-week curriculum
│
├── ai_engineering/                    # Learning materials
│   ├── README.md                      # Learning path guide
│   ├── llm/                           # Complete LLM course (5 modules)
│   │   ├── 00_attention_is_all_you_need.md     # Transformer deep dive (optional)
│   │   ├── 01_llm_fundamentals.md              # Start here
│   │   ├── 02_practical_examples.md            # Code to run
│   │   ├── 03_quick_reference.md               # Lookup + decision trees
│   │   ├── 04_hard_problems.md                 # Production realities
│   │   └── 05_prompt_engineering.md            # How to prompt well
│   ├── rag/                           # Retrieval-Augmented Generation (WIP)
│   ├── agentic/                       # AI Agents & Multi-Agent Systems (WIP)
│   └── NIPS-2017-attention-is-all-you-need-Paper.pdf
│
└── projects/                          # Hands-on implementations
    ├── hello_world/                   # Simple Ollama + streaming example
    │   ├── main.py
    │   └── pyproject.toml
    └── Jsonify/                       # Production-ready JSON extractor
        ├── README.md
        ├── src/
        │   ├── main.py                # CLI entry point
        │   ├── config.py              # Configuration
        │   ├── core/                  # Core logic
        │   │   ├── extractor.py       # LLM + retry logic
        │   │   └── models.py          # Pydantic schemas
        │   └── utils/                 # Utilities
        │       ├── retry.py           # Exponential backoff
        │       └── exceptions.py      # Error types
        ├── tests/
        │   └── test_extractor.py      # Comprehensive test suite
        └── pyproject.toml

```

---

## The Learning Path (At a Glance)

**Phase 0 (Week 1)**: Fast context & setup
- Vocabulary, API access, hello-world tool use

**Phase 1 (Weeks 2-7)**: Core Engineering - RAG from First Principles
- Week 2: Prompting as engineering (JSON extraction)
- Week 3: Embeddings & vector search
- Week 4: Vector databases
- Week 5: RAG done right (retrieval + re-ranking)
- Week 6: Evaluation frameworks
- Week 7: LLMOps & observability

**Phase 2 (Weeks 8-12)**: Agentic AI
- Week 8: Tool use from first principles
- Week 9: Agent frameworks (LangGraph)
- Week 10: Memory & multi-turn
- Week 11: Multi-agent & human-in-the-loop
- Week 12: Evaluation & safety

**Phase 3 (Weeks 13-18)**: Production & Capstone
- Week 13: Model serving & economics
- Week 14: Fine-tuning & customization
- Week 15: Security for AI systems
- Weeks 16-18: Build, polish, ship capstone project

---

## Getting Started Right Now

### Option 1: Learn Theory First
```bash
# Open the learning path
open ai_engineering/README.md

# Then read
ai_engineering/llm/01_llm_fundamentals.md
```

### Option 2: Use the Tracker
```bash
# Open in any browser (no server required)
open tracker.html

# Set a start date and begin tracking Week 1 tasks
```

### Option 3: Run Existing Projects
```bash
# hello_world - basic Ollama integration
cd projects/hello_world
python main.py

# Jsonify - production JSON extractor with tests
cd projects/Jsonify
python -m pytest tests/ -v      # Run tests
python -m src.main "your text here"  # Use the CLI
```

---

## How to Use This Repo

**As a learner:**
1. Read modules in order (they build on each other)
2. Run the code examples - don't just read them
3. Use the tracker to stay on schedule
4. Build projects from the curriculum

**As a reference:**
- Jump to [ai_engineering/llm/03_quick_reference.md](ai_engineering/llm/03_quick_reference.md) for definitions and decision trees
- Check [tracker.html](https://santosh502.github.io/ai-engineer-transition/tracker.html) for Week X resources and tasks
- See [projects/](projects/) for working code examples

**As a self-challenge:**
- Use the tracker's evaluations to check your understanding
- Complete the 18-week capstone project
- Red-team your own systems (Week 15)

---

## Key Files

| File | Purpose |
|------|---------|
| [tracker.html](https://santosh502.github.io/ai-engineer-transition/tracker.html) | Interactive progress tracker + 18-week curriculum (open in browser) |
| [ai_engineering/README.md](ai_engineering/README.md) | Learning path guide + key concepts |
| [ai_engineering/llm/01_llm_fundamentals.md](ai_engineering/llm/01_llm_fundamentals.md) | Start here for foundations |
| [ai_engineering/llm/03_quick_reference.md](ai_engineering/llm/03_quick_reference.md) | Lookup table + decision trees |
| [ai_engineering/llm/04_hard_problems.md](ai_engineering/llm/04_hard_problems.md) | What breaks in production |
| [projects/Jsonify/README.md](projects/Jsonify/README.md) | Production-ready project example |

---

## Tools You'll Use

**LLM APIs & Platforms**
- Anthropic Claude (primary)
- OpenAI GPT (comparison)
- Ollama (local models)

**Data & Vectors**
- Pydantic (validation)
- Vector databases (Qdrant, pgvector, Pinecone)
- Sentence Transformers (embeddings)

**Building & Frameworks**
- LangGraph (agent workflows)
- LangChain (composing with LLMs)
- Instructor (structured outputs)

**Evaluation & Observability**
- RAGAS (RAG evaluation)
- Langfuse (observability)
- Custom metrics

See each week's resources in [tracker.html](https://santosh502.github.io/ai-engineer-transition/tracker.html) for the complete toolkit per phase.

---
## License

This learning path and all materials are open and free to use, modify, and share.

---

**Ready?** → Open [tracker.html](https://santosh502.github.io/ai-engineer-transition/tracker.html) or read [ai_engineering/llm/01_llm_fundamentals.md](ai_engineering/llm/01_llm_fundamentals.md)

Good luck!
