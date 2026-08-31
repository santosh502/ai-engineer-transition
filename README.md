# AI Engineer Transition

A **practical, 18-week program** for experienced software engineers to master AI engineering-from LLM fundamentals through building production agents.

**Live on GitHub Pages**: [https://santosh502.github.io/ai-engineer-transition/](https://santosh502.github.io/ai-engineer-transition/)

---

## What This Is

This repo combines:
- **Learning materials** - Theory + hands-on code across 5 structured LLM modules
- **Working projects** - Two production-like applications (text-to-JSON extractor, hello-world LLM)
- **Progress tracker** - Interactive 18-week curriculum with tasks, resources, and checkpoints

**Ideal for**: Software engineers with 5+ years experience who want to build real AI systems (not just prompt ChatGPT).

---

## Table of Contents

### Quick Navigation
- [Access This Course](#access-this-course) - How to view
- [Quick Start](#quick-start) - Choose your path
- [Repository Structure](#repository-structure) - What's inside
- [Learning Path](#the-learning-path-at-a-glance) - 18-week curriculum
- [How to Use](#how-to-use-this-repo) - Learning modes

### Learning Materials
- [RAG Materials](#rag-learning-materials) - Complete RAG guide
- [Key Files](#key-files) - Important resources
- [Tools](#tools-youll-use) - Required tools & platforms

### For Forkers
- [Host Your Own Tracker](#host-your-own-tracker) - Use as-is (3 steps)
- [License](#license) - Permissions & attribution

---

## Access This Course

### Online (Recommended)
- **Interactive Tracker** - [https://santosh502.github.io/ai-engineer-transition/tracker.html](https://santosh502.github.io/ai-engineer-transition/tracker.html) (best for progress tracking)
- **GitHub Repository** - [https://github.com/santosh502/ai-engineer-transition](https://github.com/santosh502/ai-engineer-transition)

### Local (Clone & Use Offline)
```bash
git clone https://github.com/santosh502/ai-engineer-transition.git
cd ai-engineer-transition
code .  # View in your editor
```

---

## Quick Start

**Just want to learn?**
- Start: [ai_engineering/llm/01_llm_fundamentals.md](ai_engineering/llm/01_llm_fundamentals.md)
- Then work through: fundamentals → examples → reference → hard problems → prompting
- For RAG: [ai_engineering/rag/README.md](ai_engineering/rag/README.md)
- Time: 1 week basics, 3-4 weeks for depth

**Want to build projects?**
- Open [Interactive Tracker](https://santosh502.github.io/ai-engineer-transition/tracker.html)
- Follow 18-week curriculum or accelerate to 4-6 weeks
- See [projects/](projects/) for working examples

**Prefer to understand structure first?**
- Keep reading below

---

## Repository Structure

```
ai-engineer-transition/
├── README.md                          # Main documentation
├── tracker.html                       # Interactive 18-week curriculum
│
├── ai_engineering/                    # Learning materials
│   ├── README.md                      # Learning path guide
│   ├── llm/                           # Complete LLM course (5 modules)
│   │   ├── 00_attention_is_all_you_need.md
│   │   ├── 01_llm_fundamentals.md
│   │   ├── 02_practical_examples.md
│   │   ├── 03_quick_reference.md
│   │   ├── 04_hard_problems.md
│   │   └── 05_prompt_engineering.md
│   ├── rag/                           # Retrieval-Augmented Generation
│   │   ├── README.md                  # Navigation & overview
│   │   ├── notes.md                   # Comprehensive study guide
│   │   ├── implementation-examples.md # Practical code examples
│   │   └── quick-reference.md         # Quick lookup cheat sheet
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
        │   ├── main.py
        │   ├── config.py
        │   ├── core/
        │   │   ├── extractor.py
        │   │   └── models.py
        │   └── utils/
        │       ├── retry.py
        │       └── exceptions.py
        ├── tests/
        │   └── test_extractor.py
        └── pyproject.toml
```

---

## The Learning Path (At a Glance)

**Phase 0 (Week 1)**: Fast context & setup
- Vocabulary, API access, hello-world tool use

**Phase 1 (Weeks 2-7)**: Core Engineering - RAG from First Principles
- Week 2: Prompting as engineering (JSON extraction)
- Week 3: Embeddings & vector search - See [rag/notes.md - Vector Embeddings](ai_engineering/rag/notes.md#2-vector-embeddings--similarity-search)
- Week 4: Vector databases - See [rag/quick-reference.md - Vector Databases](ai_engineering/rag/quick-reference.md#vector-databases)
- Week 5: RAG done right (retrieval + re-ranking) - See [rag/implementation-examples.md](ai_engineering/rag/implementation-examples.md)
- Week 6: Evaluation frameworks - See [rag/notes.md - Evaluation Metrics](ai_engineering/rag/notes.md#evaluation-metrics)
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

## How to Use This Repo

**Learning mode**
1. Read modules in order (they build on each other)
2. Run code examples - don't just read them
3. Use the tracker to stay on schedule

**Reference mode**
- Jump to [Quick Reference](ai_engineering/llm/03_quick_reference.md) for definitions and decision trees
- Check [tracker.html](https://santosh502.github.io/ai-engineer-transition/tracker.html) for resources and tasks
- See [projects/](projects/) for working code

**Self-challenge mode**
- Complete evaluations to check your understanding
- Build the 18-week capstone project
- Red-team your own systems (Week 15)

---

## RAG Learning Materials

Complete, comprehensive materials for mastering Retrieval-Augmented Generation:

| Resource | Type | Best For | Size |
|----------|------|----------|------|
| [rag/README.md](ai_engineering/rag/README.md) | Overview | Navigation & understanding structure | Quick read |
| [rag/notes.md](ai_engineering/rag/notes.md) | Study Guide | Deep learning (concepts, diagrams, best practices) | 317 lines |
| [rag/implementation-examples.md](ai_engineering/rag/implementation-examples.md) | Code | Building RAG systems (9 working examples) | 345 lines |
| [rag/quick-reference.md](ai_engineering/rag/quick-reference.md) | Reference | Quick lookups during development | 298 lines |

**Start with**: [rag/README.md](ai_engineering/rag/README.md) → Choose your path (depth vs speed)

---

## Key Files

| File | Purpose |
|------|---------|
| [tracker.html](https://santosh502.github.io/ai-engineer-transition/tracker.html) | Interactive progress tracker + 18-week curriculum (open in browser) |
| [ai_engineering/README.md](ai_engineering/README.md) | Learning path guide + key concepts |
| [ai_engineering/llm/01_llm_fundamentals.md](ai_engineering/llm/01_llm_fundamentals.md) | Start here for foundations |
| [ai_engineering/llm/03_quick_reference.md](ai_engineering/llm/03_quick_reference.md) | Lookup table + decision trees |
| [ai_engineering/llm/04_hard_problems.md](ai_engineering/llm/04_hard_problems.md) | What breaks in production |
| [ai_engineering/rag/README.md](ai_engineering/rag/README.md) | RAG learning path + materials |
| [ai_engineering/rag/quick-reference.md](ai_engineering/rag/quick-reference.md) | RAG quick lookup guide |
| [projects/Jsonify/README.md](projects/Jsonify/README.md) | Production-ready project example |

---

## Tools You'll Use

**LLM APIs** - Anthropic Claude, OpenAI GPT, Ollama

**Data & Vectors** - Pydantic, Vector databases (Qdrant, pgvector, Pinecone), Sentence Transformers

**Frameworks** - LangGraph, LangChain, Instructor

**Evaluation** - RAGAS, Langfuse, custom metrics

See [tracker.html](https://santosh502.github.io/ai-engineer-transition/tracker.html) for the complete toolkit per phase.

---

## Host Your Own Tracker

Want to use this 18-week curriculum for yourself or your team? Simply fork and deploy - no customization required.

**3 steps:**
1. Fork the repo on GitHub
2. Enable GitHub Pages in Settings (main branch, root folder)
3. Access your tracker at `https://YOUR_USERNAME.github.io/ai-engineer-transition/tracker.html`

---

## License

This learning path and all materials are open and free to use, modify, and share.

**Ready to start?**
- **Recommended**: [Interactive Tracker](https://santosh502.github.io/ai-engineer-transition/tracker.html)
- **Alternative**: [LLM Fundamentals](ai_engineering/llm/01_llm_fundamentals.md)
- **For RAG**: [RAG Learning Materials](ai_engineering/rag/README.md)

Good luck!
