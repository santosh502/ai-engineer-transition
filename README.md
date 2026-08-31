# AI Engineer Transition

A **practical, 18-week program** for experienced software engineers to master AI engineering—from LLM fundamentals through building production agents.

📍 **Live on GitHub Pages**: [https://santosh502.github.io/ai-engineer-transition/](https://santosh502.github.io/ai-engineer-transition/)

---

## Overview

This repo combines:
- **Learning materials** — Theory + hands-on code across 5 structured LLM modules
- **Working projects** — Two production-like applications (text-to-JSON extractor, hello-world LLM)
- **Progress tracker** — Interactive 18-week curriculum with tasks, resources, and checkpoints

> **Ideal for**: Software engineers with 5+ years experience who want to build real AI systems (not just prompt ChatGPT).

---

## Navigation

| Section | Purpose |
|---------|---------|
| [Quick Start](#quick-start) | Choose your learning path |
| [Repository Structure](#repository-structure) | Understand what's inside |
| [Learning Path](#the-learning-path-at-a-glance) | 18-week curriculum overview |
| [Access Options](#access-this-course) | Online, local, or hosted |
| [Resources](#rag-learning-materials) | Learning materials & tools |

---

## Access This Course

**Online (Recommended)**

- **[Interactive Tracker](https://santosh502.github.io/ai-engineer-transition/tracker.html)** — Best for progress tracking and structured learning
- **[GitHub Repository](https://github.com/santosh502/ai-engineer-transition)** — Source code and materials

**Local (Clone & Use Offline)**

```bash
git clone https://github.com/santosh502/ai-engineer-transition.git
cd ai-engineer-transition
code .  # Open in your editor
```

---

## Quick Start

Choose your path below:

### Path 1: Learning Only
**Goal**: Master AI engineering concepts  
**Time**: 1 week basics, 3-4 weeks for depth

1. Start: [LLM Fundamentals](ai_engineering/llm/01_llm_fundamentals.md)
2. Progress: fundamentals → examples → reference → hard problems → prompting
3. Deepen: [RAG Materials](ai_engineering/rag/README.md)

### Path 2: Build Projects
**Goal**: Apply concepts to real applications  
**Time**: 4-6 weeks (or 18-week full path)

1. Open [Interactive Tracker](https://santosh502.github.io/ai-engineer-transition/tracker.html)
2. Follow structured curriculum with projects and checkpoints
3. Reference: [Working Examples](projects/)

### Path 3: Understand Structure First
Keep reading the sections below

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
│   │   ├── 00_attention_is_all_you_need.md     # Deep dive: Transformer architecture
│   │   ├── 01_llm_fundamentals.md              # Start here: Core concepts
│   │   ├── 02_practical_examples.md            # Code examples to run
│   │   ├── 03_quick_reference.md               # Lookup table & decision trees
│   │   ├── 04_hard_problems.md                 # Production challenges
│   │   └── 05_prompt_engineering.md            # Getting good results
│   │
│   ├── rag/                           # Retrieval-Augmented Generation
│   │   ├── README.md                  # Navigation & overview
│   │   ├── notes.md                   # Comprehensive study guide
│   │   ├── implementation-examples.md # Practical code examples
│   │   └── quick-reference.md         # Quick lookup cheat sheet
│   │
│   ├── agentic/                       # AI Agents & Multi-Agent Systems (coming soon)
│   └── NIPS-2017-attention-is-all-you-need-Paper.pdf
│
└── projects/                          # Hands-on implementations
    ├── hello_world/                   # Simple Ollama + streaming example
    │   ├── main.py
    │   └── pyproject.toml
    │
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

## The Learning Path

### Phase 0 — Week 1: Fast Context & Setup
Vocabulary, API access, hello-world tool use

### Phase 1 — Weeks 2-7: Core Engineering (RAG from First Principles)

| Week | Topic | Resources |
|------|-------|-----------|
| 2 | Prompting as engineering (JSON extraction) | [Implementation examples](ai_engineering/rag/implementation-examples.md) |
| 3 | Embeddings & vector search | [RAG notes: Vector Embeddings](ai_engineering/rag/notes.md#2-vector-embeddings--similarity-search) |
| 4 | Vector databases | [RAG quick ref: Vector Databases](ai_engineering/rag/quick-reference.md#vector-databases) |
| 5 | RAG done right (retrieval + re-ranking) | [Implementation examples](ai_engineering/rag/implementation-examples.md) |
| 6 | Evaluation frameworks | [RAG notes: Evaluation Metrics](ai_engineering/rag/notes.md#evaluation-metrics) |
| 7 | LLMOps & observability | [Tracker resources](https://santosh502.github.io/ai-engineer-transition/tracker.html) |

### Phase 2 — Weeks 8-12: Agentic AI
- Week 8: Tool use from first principles
- Week 9: Agent frameworks (LangGraph)
- Week 10: Memory & multi-turn
- Week 11: Multi-agent & human-in-the-loop
- Week 12: Evaluation & safety

### Phase 3 — Weeks 13-18: Production & Capstone
- Week 13: Model serving & economics
- Week 14: Fine-tuning & customization
- Week 15: Security for AI systems
- Weeks 16-18: Build, polish, ship capstone project

---

## How to Use This Repo

**Learning Mode**
1. Read modules in order (they build on each other)
2. Run code examples—don't just read them
3. Use the tracker to stay on schedule

**Reference Mode**
- Jump to [Quick Reference](ai_engineering/llm/03_quick_reference.md) for definitions and decision trees
- Check [tracker.html](https://santosh502.github.io/ai-engineer-transition/tracker.html) for resources and tasks
- See [projects/](projects/) for working code

**Self-Challenge Mode**
- Complete evaluations to check your understanding
- Build the 18-week capstone project
- Red-team your own systems (Week 15)

---

## Learning Materials

### Retrieval-Augmented Generation (RAG)

Complete materials for mastering RAG systems:

| Resource | Type | Best For | Length |
|----------|------|----------|--------|
| [rag/README.md](ai_engineering/rag/README.md) | Overview | Navigation & structure | Quick read |
| [rag/notes.md](ai_engineering/rag/notes.md) | Study Guide | Deep learning & concepts | 317 lines |
| [rag/implementation-examples.md](ai_engineering/rag/implementation-examples.md) | Code | Building systems | 9 examples |
| [rag/quick-reference.md](ai_engineering/rag/quick-reference.md) | Reference | Quick lookups | 298 lines |

**Start with**: [rag/README.md](ai_engineering/rag/README.md) — Choose your path (depth vs speed)

---

## Key Resources

### Essential Files

| File | Purpose |
|------|---------|
| [tracker.html](https://santosh502.github.io/ai-engineer-transition/tracker.html) | Interactive progress tracker & 18-week curriculum |
| [ai_engineering/README.md](ai_engineering/README.md) | Learning path guide & key concepts |
| [ai_engineering/llm/01_llm_fundamentals.md](ai_engineering/llm/01_llm_fundamentals.md) | Foundations—start here |
| [ai_engineering/llm/03_quick_reference.md](ai_engineering/llm/03_quick_reference.md) | Lookup table & decision trees |
| [ai_engineering/llm/04_hard_problems.md](ai_engineering/llm/04_hard_problems.md) | What breaks in production |
| [ai_engineering/rag/README.md](ai_engineering/rag/README.md) | RAG learning path & materials |
| [projects/Jsonify/README.md](projects/Jsonify/README.md) | Production-ready project example |

### Tools & Platforms

**LLM APIs**: Anthropic Claude, OpenAI GPT, Ollama

**Data & Vectors**: Pydantic, Vector databases (Qdrant, pgvector, Pinecone), Sentence Transformers

**Frameworks**: LangGraph, LangChain, Instructor

**Evaluation**: RAGAS, Langfuse, custom metrics

See [tracker.html](https://santosh502.github.io/ai-engineer-transition/tracker.html) for the complete toolkit per phase.

---

## Deploy Your Own Tracker

Want to use this 18-week curriculum for yourself or your team?

> **No customization required**—simply fork and deploy.

**3-step setup**:
1. Fork the repo on GitHub
2. Enable GitHub Pages in Settings (main branch, root folder)
3. Access your tracker: `https://YOUR_USERNAME.github.io/ai-engineer-transition/tracker.html`

---

## License

This learning path and all materials are open and free to use, modify, and share.

---

## Ready to Start?

- **Recommended**: [Interactive Tracker](https://santosh502.github.io/ai-engineer-transition/tracker.html)
- **Alternative**: [LLM Fundamentals](ai_engineering/llm/01_llm_fundamentals.md)
- **For RAG**: [RAG Learning Materials](ai_engineering/rag/README.md)
