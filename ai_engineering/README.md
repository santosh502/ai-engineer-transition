# AI Engineering Learning Path

**Quick Navigation**: [LLM Course](llm/README.md) · [Embeddings](embeddings/README.md) · [Vector Databases](vector_databases/README.md) · [RAG Guide](rag/README.md) · [Agentic AI](agentic/README.md)

A practical guide to understanding Large Language Models - how they actually work, how to build with them, and what matters in 2026.

---

## Directory Structure

```
ai_engineering/
├── llm/                                 # How LLMs work
│   ├── 00_attention_is_all_you_need.md  # Transformer deep dive
│   ├── 01_llm_fundamentals.md           # Core concepts (START HERE)
│   ├── 02_practical_examples.md         # Code you can run
│   ├── 03_quick_reference.md            # Lookup table & decision trees
│   ├── 04_hard_problems.md              # Production challenges
│   ├── 05_prompt_engineering.md         # Getting good behavior
│   └── README.md                        # Learning sequence
│
├── embeddings/                          # Phase 2A: Embeddings & Semantic Search
│   ├── 00_embeddings_guide.md           # Fundamentals & from-scratch implementation
│   ├── 01_practical_code_examples.md    # 4 runnable code examples
│   ├── 02_quick_reference.md            # Cheat sheet for models & chunking
│   └── README.md                        # Learning paths & navigation
│
├── vector_databases/                    # Phase 2B: Vector DBs & ANN
│   ├── 00_vector_databases_guide.md     # ANN algorithms & DB comparison
│   ├── 01_practical_code_examples.md    # 6 runnable code examples
│   ├── 02_quick_reference.md            # DB decision tree & tuning guide
│   └── README.md                        # Learning paths & navigation
│
├── rag/                                 # Retrieval-Augmented Generation
│   ├── README.md                        # Navigation & overview
│   ├── notes.md                         # Comprehensive study guide
│   ├── implementation-examples.md       # Practical code examples
│   └── quick-reference.md               # Quick lookup cheat sheet
│
├── agentic/                             # AI Agents & Multi-Agent Systems
│   └── README.md                        # Coming soon
│
└── NIPS-2017-attention-is-all-you-need-Paper.pdf
```

---

## Getting Started

### Beginner Path (1 week)

1. Read [LLM Fundamentals](llm/01_llm_fundamentals.md)—covers what LLMs actually are, not the hype version
2. Keep [Quick Reference](llm/03_quick_reference.md) nearby for terms and decision trees
3. Work through [Practical Examples](llm/02_practical_examples.md)—see it in action
4. *(Optional)* Read [Attention Is All You Need](llm/00_attention_is_all_you_need.md) for deep Transformer understanding

### Intermediate Path (2-3 weeks)

1. Work through all 5 LLM files in order: fundamentals → examples → reference → hard problems → prompting
2. Dig into Transformer architecture and why self-attention works
3. Understand scaling laws and what they predict about future models
4. Read about reasoning models and test-time compute (o1, DeepSeek-R1)

### Builder Path (3+ weeks)

1. Build something real: a RAG system or a simple agent
2. Learn security hardening—prompt injection, jailbreaks, alignment challenges
3. Build multi-agent systems that compose tools together
4. Follow the [18-week curriculum](../tracker.html) for structured progression

---

## Learning Modules

### Large Language Models (LLM)

Complete learning path from theory to production.

**Files** (read in order):

| File | Focus | Level |
|------|-------|-------|
| [00: Attention Is All You Need](llm/00_attention_is_all_you_need.md) | Transformer deep dive | Advanced (optional) |
| [01: LLM Fundamentals](llm/01_llm_fundamentals.md) | Architecture, training, scaling | Beginner |
| [02: Practical Examples](llm/02_practical_examples.md) | Code you can run | Intermediate |
| [03: Quick Reference](llm/03_quick_reference.md) | Terminology, decision trees | All levels |
| [04: Hard Problems](llm/04_hard_problems.md) | Production challenges | Intermediate+ |
| [05: Prompt Engineering](llm/05_prompt_engineering.md) | Getting good behavior | Beginner+ |

**Topics covered**:
- What is an LLM really? (weights + inference code)
- Transformer architecture and why self-attention changed everything
- Training pipeline: pretraining → fine-tuning → alignment
- Scaling laws and what they tell us about future models
- Reasoning models and test-time compute (o1, DeepSeek-R1)
- Multimodal models (vision, audio, text in one)
- Security challenges (jailbreaks, prompt injection, alignment)
- Writing effective prompts that work in production

---

### Embeddings (Phase 2A)

Learn what embeddings are and how to build semantic search from first principles.

**Files** (in suggested order):

| File | Focus | Level |
|------|-------|-------|
| [README.md](embeddings/README.md) | Navigation & learning paths | All levels |
| [00: Embeddings Guide](embeddings/00_embeddings_guide.md) | What embeddings are, cosine similarity, chunking (Sections 1–9) | Beginner |
| [01: Practical Code](embeddings/01_practical_code_examples.md) | 4 runnable examples + integration | Intermediate |
| [02: Quick Reference](embeddings/02_quick_reference.md) | Model recommendations, chunking sizes, API reference | All levels |

**Topics covered**:
- What embeddings are and why we need them (Phase 1 vector geometry extended to N dimensions)
- Cosine similarity: the "angle between meanings"
- Dense vs. sparse vectors
- Text chunking strategies (5 approaches with trade-offs)
- Building a semantic search engine from scratch in pure Python (no frameworks)
- Comparing embedding models (OpenAI, Cohere, Sentence Transformers, BAAI, etc.)
- Practical model selection and cost analysis

**Learning outcomes**: Deep intuition for embeddings, ability to design chunking strategies, implement semantic search without frameworks, compare models.

---

### Vector Databases (Phase 2B)

Learn how to scale semantic search to millions/billions of vectors using ANN algorithms.

**Files** (in suggested order):

| File | Focus | Level |
|------|-------|-------|
| [README.md](vector_databases/README.md) | Navigation & learning paths | All levels |
| [00: Vector DB Guide](vector_databases/00_vector_databases_guide.md) | ANN algorithms, DB comparison, hybrid search (Sections 10–16) | Intermediate |
| [01: Practical Code](vector_databases/01_practical_code_examples.md) | 6 runnable examples (pgvector, Qdrant, hybrid search) | Intermediate |
| [02: Quick Reference](vector_databases/02_quick_reference.md) | DB decision tree, algorithm comparison, performance tuning | All levels |

**Topics covered**:
- What vector databases solve (scaling similarity search from O(n) to O(log n))
- ANN algorithms in depth: HNSW, IVF, LSH, Product Quantization
- Top vector databases compared (Pinecone, Qdrant, pgvector, Weaviate, Milvus, FAISS)
- Choosing the right vector DB for your scale
- Setting up pgvector (Postgres) and Qdrant locally
- Metadata filtering and access control
- Hybrid search: combining dense embeddings + BM25 keyword search
- Performance tuning and latency optimization

**Learning outcomes**: Understand ANN algorithms and their trade-offs, choose the right vector DB, implement hybrid search, optimize for production.

---

### Retrieval-Augmented Generation (RAG)

Complete learning materials for mastering RAG systems.

**Files** (in suggested order):

| File | Focus | Best For |
|------|-------|----------|
| [README.md](rag/README.md) | Overview | Getting oriented |
| [notes.md](rag/notes.md) | Deep concepts | Understanding theory |
| [implementation-examples.md](rag/implementation-examples.md) | 9 working examples | Building systems |
| [quick-reference.md](rag/quick-reference.md) | Quick lookups | Development reference |

**Topics covered**:
- Vector embeddings and similarity search
- Semantic vs keyword search
- RAG pipeline architecture
- Chunking strategies (sliding window, recursive, hierarchical)
- Vector databases (Qdrant, pgvector, Pinecone, Weaviate, FAISS, Milvus)
- LLM integration with RAG
- Prompt injection attacks in RAG systems
- Evaluating RAG quality (RAGAS metrics)
- Production deployment patterns

> See the [18-week curriculum](../tracker.html) Weeks 3-7 for hands-on projects.

---

### Agentic AI

**Status**: Structure ready, content coming soon.

**Will cover**: Agent architecture and loops, tool definitions, ReAct framework, multi-agent coordination, error recovery, security & permissions, human-in-the-loop patterns, agent evaluation.

> For now, see the [18-week curriculum](../tracker.html) Weeks 8-12 for the complete agentic AI learning path with hands-on projects.

---

## Key Concepts at a Glance

| Concept | Why It Matters | Learn More |
|---------|---|---|
| **Transformers** | The architecture behind every major LLM | [01_llm_fundamentals.md §2](llm/01_llm_fundamentals.md) or [00_attention_is_all_you_need.md](llm/00_attention_is_all_you_need.md) |
| **Self-Attention** | Lets tokens understand context from all positions | [01_llm_fundamentals.md §2](llm/01_llm_fundamentals.md) |
| **Scaling Laws** | Bigger model + more data = predictably better | [01_llm_fundamentals.md §4](llm/01_llm_fundamentals.md) |
| **Fine-tuning** | Customize models for specific domains/tasks | [02_practical_examples.md §4](llm/02_practical_examples.md) |
| **Embeddings** | Text → vectors, similar meaning = nearby vectors | [embeddings/README.md](embeddings/README.md) |
| **Cosine Similarity** | The angle between vectors (ignores magnitude, perfect for semantic comparison) | [embeddings/00_embeddings_guide.md](embeddings/00_embeddings_guide.md) §5 |
| **Chunking** | Splitting documents for optimal embedding + retrieval (balances precision vs. context) | [embeddings/00_embeddings_guide.md](embeddings/00_embeddings_guide.md) §6 |
| **ANN (Approximate Nearest Neighbor)** | Algorithms that trade <1% accuracy for 100x speed gains (HNSW, IVF, etc.) | [vector_databases/00_vector_databases_guide.md](vector_databases/00_vector_databases_guide.md) §12 |
| **Vector Databases** | Fast similarity search at scale (Qdrant, pgvector, Pinecone) | [vector_databases/README.md](vector_databases/README.md) |
| **RAG** | Ground LLM answers in real documents | [rag/README.md](rag/README.md) |
| **Agents** | LLMs coordinating tools for autonomous action | [agentic/README.md](agentic/README.md) |
| **Reasoning Models** | "Think longer" for harder problems | [01_llm_fundamentals.md §5](llm/01_llm_fundamentals.md) |
| **Multimodality** | LLMs understanding vision, audio, text | [01_llm_fundamentals.md §7](llm/01_llm_fundamentals.md) |
| **Security** | Jailbreaks, injection, alignment challenges | [04_hard_problems.md](llm/04_hard_problems.md) |

---

## Tools & Platforms

**Running Models Locally**
- Ollama — Easiest way to run Llama, Mistral, etc. on your machine
- Hugging Face — Model hub + inference, lots of community support
- LM Studio — GUI-based local inference

**Via API**
- Anthropic — Claude
- OpenAI — GPT
- Together.ai — Open-source models at scale
- Replicate — Serverless inference for anything

**Building with LLMs**
- LangChain — General framework, lots of examples
- LlamaIndex — Optimized for RAG
- Claude SDK — Python/TypeScript, works directly with Anthropic API

---

## Learning Outcomes

After working through this, you'll understand:
- How LLMs actually work (not the simplified version)
- Why transformers and attention work, and when alternatives might matter
- What happens during training and why it matters for your use case
- How to pick the right model for a problem (or build your own)
- When to fine-tune vs. RAG vs. just use a bigger model
- How to build systems that use tools and can reason across multiple steps
- What can go wrong in LLM systems and how to defend against it  

---

## Decision Trees

### Picking a Model

| Question | Answer | Recommendation |
|----------|--------|-----------------|
| Need to run on your laptop? | Yes | Llama 2, Mistral, or DeepSeek (7B-70B) → [01_llm_fundamentals.md](llm/01_llm_fundamentals.md) |
| Running via API is fine? | Yes | Claude, GPT, Gemini → [03_quick_reference.md](llm/03_quick_reference.md) |
| Need math or hard reasoning? | Yes | DeepSeek-R1, o1, Claude (extended thinking) → [05_prompt_engineering.md](llm/05_prompt_engineering.md) |
| Need vision? | Yes | GPT-4o, Claude 3.5, Gemini 2.0 → [01_llm_fundamentals.md](llm/01_llm_fundamentals.md) |

### Fine-tuning Worth It?

| Your Situation | Decision | Why |
|---|---|---|
| Have 1K+ domain examples | Yes, fine-tune | See [02_practical_examples.md §4](llm/02_practical_examples.md) |
| Less than 1K examples | Try RAG first | Cheaper and simpler |
| Cost per inference critical | Fine-tune smaller model | Inference is fast but cheap |
| Unsure | Start with big model + RAG | Fine-tune later if needed |

### RAG vs. Fine-tuning

> See [03_quick_reference.md](llm/03_quick_reference.md) for detailed decision tree.

| Situation | Choice | Reason |
|---|---|---|
| Data changes frequently | RAG | Update without retraining |
| Data is stable | Fine-tuning | Faster inference |
| Need to cite sources | RAG | Natural for attribution |
| Unsure | RAG first | Lower risk, easier to iterate |

---

## Resources

### Essential Papers

- **"Attention Is All You Need"** (Vaswani et al., 2017)
  - [Full PDF](NIPS-2017-attention-is-all-you-need-Paper.pdf) included locally
  - [Guided walkthrough](llm/00_attention_is_all_you_need.md) available

- **"Scaling Laws for Neural Language Models"** (Hoffmann et al.)
  - Covered in [01_llm_fundamentals.md §4](llm/01_llm_fundamentals.md)

- **"Language Models are Unsupervised Multitask Learners"** (Radford et al., GPT-2 paper)
  - Foundational for understanding LLM training

### Talks & Videos

- [Andrej Karpathy: "Intro to LLMs"](https://www.youtube.com/watch?v=zjkBMFhNj_g) — Clear 1-hour intro
- Jeremy Howard: "A Practical Deep Learning for Coders" — Applied focus
- [3Blue1Brown: "Attention in Transformers"](https://www.youtube.com/watch?v=eMlx5aFJsqM) — Visual explanation

### Communities

- Hugging Face — Model hub + forums
- r/MachineLearning — Reddit community
- Anthropic Discord — Latest on Claude
- OpenAI Community Forum
- arXiv.org — Original research papers

---

## What This Course Is & Isn't

**What it IS:**
- Practical, hands-on learning: theory → code → production
- Focused on **building real systems**, not just concepts
- Rooted in 2024-2026 state of the art (reasoning models, extended thinking)
- Designed for engineers transitioning to AI

**What it ISN'T:**
- Complete ML theory course (assumes some comfort with matrices, calculus)
- Replacement for papers and original research
- Dogmatic about any one framework or model

---

## How to Use This Learning Path

1. **Read sequentially** — Each file builds on previous ones
2. **Run the code** — You learn by doing, not just reading
3. **Take notes** — Write things in your own words
4. **Build projects** — Use the [18-week tracker](../tracker.html) for ideas
5. **Check yourself** — Each section ends with "Check Your Understanding" questions

---

## Contributing & Updates

This is a living resource. Feel free to contribute:
- Production tricks that work (Flash Attention, GQA, quantization, etc.)
- Frameworks or tools you've tried (what worked, what didn't)
- Things that broke and how you fixed them
- Security surprises or defense strategies
- Papers or talks that changed how you think

It gets better as people use it and learn from it.
