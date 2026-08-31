# AI Engineer Transition

A **practical, 18-week program** for experienced software engineers to master AI engineering-from LLM fundamentals through building production agents.

**Live on GitHub Pages**: [https://santosh502.github.io/ai-engineer-transition/](https://santosh502.github.io/ai-engineer-transition/)

---

## What This Is

This repo combines:
- **Learning materials** - Theory + hands-on code across 5 structured LLM modules
- **Working projects** - Two production-like applications (text→JSON extractor, hello-world LLM)
- **Progress tracker** - Interactive 18-week curriculum with tasks, resources, and checkpoints

**Ideal for**: Software engineers with 5+ years experience who want to build real AI systems (not just prompt ChatGPT).

---

## Table of Contents

### Quick Navigation
- [Access This Course](#access-this-course) — How to view
- [Quick Start](#quick-start-choose-your-path) — Choose your path
- [Repository Structure](#repository-structure) — What's inside
- [Learning Path](#the-learning-path-at-a-glance) — 18-week curriculum
- [Getting Started](#getting-started-right-now) — 4 options to begin

### Learning Materials
- [RAG Materials](#rag-learning-materials) — Complete RAG guide
- [Key Files](#key-files) — Important resources
- [Tools](#tools-youll-use) — Required tools & platforms

### For Forkers
- [Host Your Own Tracker](#-host-this-tracker-for-your-own-use-no-changes-needed) — Use as-is (3 steps)
- [License](#license) — Permissions & attribution

---

## Access This Course

### Online (Recommended)
- **Interactive Tracker**: [https://santosh502.github.io/ai-engineer-transition/tracker.html](https://santosh502.github.io/ai-engineer-transition/tracker.html) - Best for progress tracking
- **GitHub Repository**: [https://github.com/santosh502/ai-engineer-transition](https://github.com/santosh502/ai-engineer-transition)

### Want Your Own Tracker?
**Two options:**
1. **Use This Tracker As-Is** → [Host for Your Own Use](#-host-this-tracker-for-your-own-use-no-changes-needed) (recommended for most people)
   - Fork & deploy in 3 steps
   - No customization needed
   - Perfect for tracking your own progress

2. **Create Your Own Custom Tracker** → [Fork & Customize](#-fork--customize-advanced-customization)
   - Modify weeks, content, and tasks
   - Full customization guide included
   - Perfect for your class or program

### Local (Offline Access)
```bash
# Clone the repo
git clone https://github.com/santosh502/ai-engineer-transition.git
cd ai-engineer-transition

# View in your editor
code .

# Or serve locally (if you prefer)
# (all markdown links work in your IDE/editor)
```

---

## Quick Start (Choose Your Path)

### Just want to learn?
1. Open [ai_engineering/README.md](ai_engineering/README.md)
2. Start with [ai_engineering/llm/01_llm_fundamentals.md](ai_engineering/llm/01_llm_fundamentals.md)
3. Work through in order: fundamentals → examples → reference → hard problems → prompting
4. **For RAG**: See [ai_engineering/rag/README.md](ai_engineering/rag/README.md) for comprehensive materials

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
- Week 3: Embeddings & vector search → See [rag/notes.md - Vector Embeddings](ai_engineering/rag/notes.md#2-vector-embeddings--similarity-search)
- Week 4: Vector databases → See [rag/quick-reference.md - Vector Databases](ai_engineering/rag/quick-reference.md#vector-databases)
- Week 5: RAG done right (retrieval + re-ranking) → See [rag/implementation-examples.md](ai_engineering/rag/implementation-examples.md)
- Week 6: Evaluation frameworks → See [rag/notes.md - Evaluation Metrics](ai_engineering/rag/notes.md#evaluation-metrics)
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
**On GitHub Pages**: Read from [ai_engineering/README.md](https://santosh502.github.io/ai-engineer-transition/ai_engineering/README.md)

**Locally** (after cloning):
```bash
# Open the learning path
open ai_engineering/README.md

# Then read
ai_engineering/llm/01_llm_fundamentals.md
```

### Option 2: Use the Tracker (Recommended)
**Live Version**: Open [Interactive Tracker](https://santosh502.github.io/ai-engineer-transition/tracker.html) on GitHub Pages (no server needed)

**Locally** (after cloning):
```bash
# Open in your browser
open tracker.html

# Set a start date and begin tracking Week 1 tasks
# For Phase 1 (RAG weeks), cross-reference: ai_engineering/rag/
```

### Option 2b: Deep Dive into RAG
```bash
# Jump directly to comprehensive RAG materials
open ai_engineering/rag/README.md

# Then choose:
# - For theory: ai_engineering/rag/notes.md
# - For code: ai_engineering/rag/implementation-examples.md
# - For quick lookup: ai_engineering/rag/quick-reference.md
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

## Host This Tracker For Your Own Use (No Changes Needed)

Want to use this 18-week AI engineering curriculum for yourself or your team? Simply fork and deploy - no customization required!

### Quick Start (3 Steps)
```bash
# Step 1: Fork the repo (click fork on GitHub)
# Your fork: https://github.com/YOUR_USERNAME/ai-engineer-transition

# Step 2: Enable GitHub Pages in Settings → Pages
# Select: main branch, / (root) folder

# Step 3: Access your tracker
# Your tracker: https://YOUR_USERNAME.github.io/ai-engineer-transition/tracker.html
```

**That's it!** Your own tracker is live and ready to use.

### What You Get
- Personal progress tracker
- All 18 weeks of curriculum
- Interactive checkboxes
- Your own GitHub Pages URL
- No coding/customization needed

---

## License

This learning path and all materials are open and free to use, modify, and share.

**Ready?** 

**Start Here**: [Interactive Tracker on GitHub Pages](https://santosh502.github.io/ai-engineer-transition/tracker.html) (recommended)

**Alternative**: Read [LLM Fundamentals](ai_engineering/llm/01_llm_fundamentals.md) first

**For RAG**: Jump to [RAG Learning Materials](ai_engineering/rag/README.md)

---

Good luck!
