# AI Engineering Learning Path

<div style="float: right; width: 220px; background: #f5f5f5; padding: 15px; border-radius: 5px; margin-left: 20px;">

**Learning Materials**
- **Main Guide** ← You are here
- [LLM Course](llm/README.md)
- [RAG Guide](rag/README.md)
- [Agentic AI](agentic/README.md)

</div>

A practical guide to understanding Large Language Models-how they actually work, how to build with them, and what matters in 2026.

## Directory Structure

```
ai_engineering/
├── llm/                           # How LLMs work
│   ├── 00_attention_is_all_you_need.md    # Transformer deep dive (optional foundation)
│   ├── 01_llm_fundamentals.md             # Core concepts, explained
│   ├── 02_practical_examples.md           # Code you can run
│   ├── 03_quick_reference.md              # Lookup when you need it
│   ├── 04_hard_problems.md                # Production realities
│   ├── 05_prompt_engineering.md           # How to get good behavior
│   ├── assets/                            # Diagrams and supporting materials
│   └── README.md                          # Learning sequence guide
├── rag/                           # Retrieval-Augmented Generation
│   ├── README.md                  # Navigation & overview
│   ├── notes.md                   # Comprehensive study guide
│   ├── implementation-examples.md # Practical code examples
│   └── quick-reference.md         # Quick lookup cheat sheet
├── agentic/                       # AI Agents & Multi-Agent Systems
│   └── README.md                  # WIP - coming soon
├── NIPS-2017-attention-is-all-you-need-Paper.pdf
└── README.md                      # This file
```

## Getting Started

**Just starting out? (Beginner Path - 1 week)**
1. Read [LLM Fundamentals](llm/01_llm_fundamentals.md) first-covers what LLMs actually are, not the hype version
2. Keep the [Quick Reference](llm/03_quick_reference.md) nearby for terms and decision trees
3. Work through [Practical Examples](llm/02_practical_examples.md) to see it in action
4. (Optional) Read [Attention Is All You Need](llm/00_attention_is_all_you_need.md) for deep Transformer understanding

**Already comfortable with the basics? (2-3 weeks)**
1. Work through all 5 LLM files in order (fundamentals → examples → reference → hard problems → prompting)
2. Dig into Transformer architecture and why self-attention works
3. Understand scaling laws and what they predict about future models
4. Read about reasoning models and test-time compute (o1, DeepSeek-R1)

**Ready to build? (Weeks 3+)**
1. Build something real: a RAG system or a simple agent
2. Learn security hardening-prompt injection, jailbreaks, alignment challenges
3. Build multi-agent systems that compose tools together
4. Follow the [18-week curriculum](../tracker.html) for structured progression

## What's Here

### Large Language Models (LLM)
Complete learning path from theory to production. Learn: the architecture, how training actually works, why scaling matters, reasoning models vs standard inference, and how to build reliable systems.

**Files** (read in order):
- [00: Attention Is All You Need](llm/00_attention_is_all_you_need.md) - Transformer deep dive (optional but recommended)
- [01: LLM Fundamentals](llm/01_llm_fundamentals.md) - What LLMs are, architecture, training, scaling
- [02: Practical Examples](llm/02_practical_examples.md) - Code you can run and modify
- [03: Quick Reference](llm/03_quick_reference.md) - Terminology, decision trees, lookups
- [04: Hard Problems](llm/04_hard_problems.md) - What breaks in production
- [05: Prompt Engineering](llm/05_prompt_engineering.md) - How to get good behavior

**Topics covered**:
- What is an LLM really? (it's weights + inference code)
- Transformer architecture and why self-attention changed everything
- Training pipeline: pretraining → fine-tuning → alignment
- Scaling laws and what they tell us about future models
- Reasoning models and test-time compute (o1, DeepSeek-R1)
- Multimodal models (vision, audio, text in one)
- Security challenges (jailbreaks, prompt injection, alignment)
- How to write effective prompts that work in production

### Retrieval-Augmented Generation (RAG)
Complete learning materials for mastering RAG systems.

**Files** (in suggested order):
- [README.md](rag/README.md) - Overview and navigation
- [notes.md](rag/notes.md) - Comprehensive study guide (concepts, diagrams, best practices)
- [implementation-examples.md](rag/implementation-examples.md) - Practical code examples (9 working implementations)
- [quick-reference.md](rag/quick-reference.md) - Quick lookups and cheat sheet during development

**Topics covered**:
- Vector embeddings and similarity search
- Semantic vs keyword search
- RAG pipeline architecture
- Chunking strategies (sliding window, recursive, hierarchical, etc.)
- Vector databases (Qdrant, pgvector, Pinecone, Weaviate, FAISS, Milvus)
- LLM integration with RAG
- Prompt injection attacks in RAG systems
- Evaluating RAG quality (retrieval precision, answer relevance, RAGAS metrics)
- Production deployment patterns

See the [18-week curriculum](../tracker.html) Week 3-7 for hands-on projects and structured progression.

### Agentic AI
**Status**: Placeholder-structure ready, content coming soon.

Planning to cover: agent architecture and loops, tool definitions, ReAct framework, multi-agent coordination, error recovery, security & permissions, human-in-the-loop patterns, agent evaluation.

In the meantime, see the [18-week curriculum](../tracker.html) Week 8-12 for the complete agentic AI learning path with hands-on projects.

## Key Concepts At a Glance

| Concept | Why It Matters | Learn More |
|---------|---|---|
| **Transformers** | The architecture behind every major LLM | [01_llm_fundamentals.md §2](llm/01_llm_fundamentals.md) or [00_attention_is_all_you_need.md](llm/00_attention_is_all_you_need.md) (deep dive) |
| **Self-Attention** | Lets tokens understand context from all positions | [01_llm_fundamentals.md §2](llm/01_llm_fundamentals.md) |
| **Scaling Laws** | Bigger model + more data = predictably better | [01_llm_fundamentals.md §4](llm/01_llm_fundamentals.md) |
| **Fine-tuning** | Customize models for specific domains/tasks | [02_practical_examples.md §4](llm/02_practical_examples.md) |
| **RAG** | Ground LLM answers in real documents | [rag/README.md](rag/README.md) |
| **Agents** | LLMs coordinating tools for autonomous action | [agentic/README.md](agentic/README.md) (coming soon) |
| **Reasoning Models** | "Think longer" for harder problems | [01_llm_fundamentals.md §5](llm/01_llm_fundamentals.md) |
| **Multimodality** | LLMs understanding vision, audio, text | [01_llm_fundamentals.md §7](llm/01_llm_fundamentals.md) |
| **Security** | Jailbreaks, injection, alignment challenges | [04_hard_problems.md](llm/04_hard_problems.md) + [05_prompt_engineering.md](llm/05_prompt_engineering.md) |

## Tools & Platforms

**Running models locally**
- Ollama (easiest way to run Llama, Mistral, etc. on your machine)
- Hugging Face (model hub + inference, lots of community support)
- LM Studio (if you want a GUI)

**Via API**
- Anthropic (Claude)
- OpenAI (GPT)
- Together.ai (if you want to experiment with open-source models at scale)
- Replicate (serverless inference for anything)

**Building with agents**
- LangChain (lots of examples, very popular)
- LlamaIndex (great for RAG specifically)
- Claude SDK (Python/TypeScript, works directly with Anthropic API)

## What You'll Be Able to Do

After working through this, you'll understand:
- How LLMs actually work (not the simplified version)
- Why transformers and attention work, and when alternatives might matter
- What happens during training and why it matters for your use case
- How to pick the right model for a problem (or build your own)
- When to fine-tune vs. RAG vs. just use a bigger model
- How to build systems that use tools and can reason across multiple steps
- What can go wrong in LLM systems and how to defend against it  

## Quick Decision Trees

**Picking a model?**
- Need to run it on your laptop? → Llama 2, Mistral, or DeepSeek (7B-70B) - see [01_llm_fundamentals.md](llm/01_llm_fundamentals.md)
- Running via API is fine? → Claude, GPT, Gemini - see [03_quick_reference.md](llm/03_quick_reference.md) model comparison table
- Need math or hard reasoning? → DeepSeek-R1, o1, or Claude w/ extended thinking - see [05_prompt_engineering.md](llm/05_prompt_engineering.md)
- Need vision? → GPT-4o, Claude 3.5 Sonnet, or Gemini 2.0 - see [01_llm_fundamentals.md §7](llm/01_llm_fundamentals.md)

**Fine-tuning worth it?**
- Have 1K+ examples in your domain? → Probably yes - see [02_practical_examples.md §4](llm/02_practical_examples.md)
- Less than that? → Try RAG first, it's usually cheaper
- Cost per inference is critical? → Fine-tune a smaller model
- Otherwise? → Start with a big model + RAG, fine-tune later if needed

**RAG vs. fine-tuning?**
- Data changes all the time? → RAG (update without retraining)
- Data is stable? → Fine-tuning (faster at inference)
- Need to cite sources? → RAG is natural for that
- Unsure? → RAG first, then fine-tune if it's not working
- **See** [03_quick_reference.md](llm/03_quick_reference.md) for decision tree in detail

## Resources

**Papers that actually matter**
- "Attention Is All You Need" (Vaswani et al., 2017) - [Full PDF included](NIPS-2017-attention-is-all-you-need-Paper.pdf) locally. Read this if you're serious. See [00_attention_is_all_you_need.md](llm/00_attention_is_all_you_need.md) for guided walkthrough.
- "Scaling Laws for Neural Language Models" (Hoffmann et al.) - Understanding scaling. Covered in [01_llm_fundamentals.md §4](llm/01_llm_fundamentals.md)
- "Language Models are Unsupervised Multitask Learners" (Radford et al., GPT-2 paper) - Foundational

**Talks**
- Andrej Karpathy: "Intro to LLMs" (1hr, very clear) - https://www.youtube.com/watch?v=zjkBMFhNj_g
- Jeremy Howard: "A Practical Deep Learning for Coders" (courses)
- 3Blue1Brown: "Attention in Transformers" (visual explanation) - https://www.youtube.com/watch?v=eMlx5aFJsqM

**Communities & Learning**
- Hugging Face (model hub + forums)
- r/MachineLearning (Reddit)
- Anthropic Discord (latest on Claude)
- OpenAI Community Forum
- arXiv.org (read papers from the source)

## What This Course Is & Isn't

**What it IS:**
- A practical, hands-on learning path from theory → code → production
- Focused on **building real systems**, not just understanding concepts
- Rooted in 2024-2026 state of the art (reasoning models, extended thinking, etc.)
- Designed for engineers transitioning to AI (not starting from math degree)

**What it ISN'T:**
- A complete ML theory course (assumes some comfort with matrices, calculus)
- A replacement for papers and original research
- Dogmatic about any one framework or model

## How to Use This Path

1. **Read sequentially** - Each file builds on previous ones. Don't skip ahead.
2. **Run the code** - You learn by doing, not just reading.
3. **Take notes** - Write things in your own words as you go.
4. **Build projects** - Use the [18-week tracker](../tracker.html) for structured project ideas.
5. **Check yourself** - Each section ends with "Check Your Understanding" questions.

## Contributing & Updates

As you work through this, feel free to:
- Document tricks that actually work in production (Flash Attention, GQA, quantization, etc.)
- Share frameworks or tools you've tried (what worked, what didn't)
- Add things that broke and how you fixed them
- Note security surprises or defense strategies
- Link papers or talks that changed how you think

This is a living resource-it gets better as people use it and learn from it.
