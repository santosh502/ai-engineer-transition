# Phase 2A: Embeddings, Chunking - Semantic Search

**Materials**: [Overview](README.md) - [00: Embeddings Guide](00_embeddings_guide.md) - [01: Code Examples](01_practical_code_examples.md) - [02: Quick Reference](02_quick_reference.md)

Learn what embeddings are, why they matter, and how to build semantic search from first principles.

## Content

### 1. **[00_embeddings_guide.md](00_embeddings_guide.md)** (Main Guide)
Complete walkthrough covering:
- What embeddings are and why we need them (geometric intuition)
- Cosine similarity: the "angle between meanings"
- Dense vs. sparse vectors
- Text chunking strategies (5 approaches with trade-offs)
- Building a semantic search engine from scratch (pure Python, no frameworks)
- Comparing embedding models (OpenAI, Cohere, open-source options)

**Sections:**
1. What Is an Embedding?
2. Why Embeddings Are Needed
3. Best Way of Embedding (Practical Guidelines)
4. Dense Vectors
5. Cosine Similarity
6. Chunking - And Why Size/Overlap Matters
7. Build a Semantic Search Engine from Scratch
8. Basic Vector Store (Local, No Framework)
9. Comparing Embedding Models

---

### 2. **[01_practical_code_examples.md](01_practical_code_examples.md)** (Runnable Code)
4 complete examples you can run right now:
- Example 1: Manual cosine similarity (pure Python)
- Example 2: Text chunking strategies
- Example 3: Simple vector store implementation
- Example 4: Mock embedding API
- **Integration Example:** Complete end-to-end pipeline

All self-contained, no dependencies beyond Python stdlib (or optional numpy).

---

### 3. **[02_quick_reference.md](02_quick_reference.md)** (Cheat Sheet)
Quick lookups:
- Embedding model recommendations
- Chunking sizes by document type
- Cosine similarity vs. other distances
- API quick reference (OpenAI, Cohere, Sentence Transformers)
- Common mistakes & how to fix them
- Cost comparison (2024 pricing)
- Debugging guide

---

## How to Use

### Option 1: Learn Sequentially (First Time)
1. Read **Main Guide** (`00_*`), Sections 1–9
2. After each section, try the corresponding example from `01_*`
3. Keep `02_*` handy while coding

**Time:** 1 week

### Option 2: Learn By Doing (Experienced Learners)
1. Run **Examples 1–4** from `01_*`
2. Read relevant sections in `00_*` when curious about "why"
3. Use `02_*` for quick model/chunking decisions

**Time:** 2–3 days

### Option 3: Reference Only (Experts)
1. Use `02_*` for quick answers
2. Dip into `00_*` for deeper understanding of a specific concept

---

## Quick Start - 15 Minutes

```
1. Read: Section 1 + Section 5 (Main Guide)
   → "What is an embedding" + "How cosine similarity works"

2. Run: Example 1 (Manual cosine similarity)
   → Understand the core math in 10 lines of code

3. Run: Example 3 (Simple vector store)
   → Now you have a working search engine
```

---

## Key Concepts at a Glance

| Concept | In One Sentence |
|---|---|
| **Embedding** | A function mapping text/image/audio to a point in high-dimensional space where similar meaning = nearby points |
| **Dense vector** | A vector where almost every dimension is non-zero (learned latent features) |
| **Cosine similarity** | The angle between two vectors (ignores magnitude, perfect for comparing directions/meanings) |
| **Chunking** | Splitting long documents into smaller pieces before embedding to balance precision vs. context |
| **Overlap** | Repeating some text between chunks to prevent loss of meaning at boundaries |

---

## Learning Path

### Phase 2A: Embeddings Fundamentals (1 week)

**Days 1–3: Concepts**
- [ ] Read Sections 1–5 (embeddings, cosine similarity)
- [ ] Run Examples 1–3 (understand the math)
- [ ] Answer Section 11 practice problems

**Days 4–7: Implementation**
- [ ] Read Sections 6–9 (chunking, comparing models)
- [ ] Run Example 4 and the integration example on real documents
- [ ] Test 2 embedding models on your domain data
- [ ] Benchmark chunking strategies (does 300 vs 500 tokens matter?)

---

## Learning Outcomes

By the end of this phase, you will:
- [ ] **Explain embeddings** to non-technical people using Phase 1 vector geometry
- [ ] **Compute cosine similarity by hand** for 2–3D vectors
- [ ] **Design a chunking strategy** for your document type (size, overlap, reasoning)
- [ ] **Build a semantic search engine** from scratch without frameworks
- [ ] **Choose an embedding model** based on latency/quality/cost
- [ ] **Understand the trade-offs** between dense embeddings and sparse/keyword search

---

## Tech Stack Recommendations

**Embedding Model (Pick One):**
- `text-embedding-3-small` (OpenAI) - best for production
- `all-MiniLM-L6-v2` (Sentence Transformers) - best for free
- Cohere `embed-v3` - if you already use Cohere
- `bge-large` (BAAI) - best self-hosted

**No database needed at this stage** - Example 3's vector store handles everything until you scale to millions of vectors.

---

## Connections to Other Phases

- **Phase 1 (Vector Geometry):** Section 5 uses all Phase 1 concepts (dot product, magnitude, angle)
- **Vector Databases module:** Next step when you need to scale beyond 10K vectors or add metadata filtering
- **Phase 4 (RAG):** These chunks become the context window for your LLM

---

## Why Learn This?

1. **Intuition:** Embeddings feel like magic until you understand cosine similarity. This phase demystifies it.
2. **Foundation:** You can't pick the right embedding model or chunking strategy without understanding trade-offs.
3. **No abstractions:** Building it by hand (Examples 1–3) teaches you what LangChain/Llama Index hide.
4. **Domain-specific:** Your embedding choices are the biggest lever on retrieval quality.

---

## FAQ

**Q: Do I need to read all 9 sections?**
A: Not if you already understand embeddings. Skim Sections 1–4, focus on 5–9 (chunking, chunking strategy, model comparison).

**Q: Is Example 3's vector store good enough for production?**
A: Yes, for <10K vectors. Beyond that, move to Vector Databases module for ANN indexing.

**Q: Can I use different embedding models for indexing vs. querying?**
A: No. Vectors are only comparable if from the same model. Mixing breaks all rankings.

**Q: How do I know if my chunking is right?**
A: Measure recall@5 on queries you care about. If results are missing relevant info, chunks are too large. If too fragmented, they're too small.

**Q: What's the minimal viable setup?**
A: Example 4 + Example 3 = semantic search in ~100 lines of Python. Run it tonight.

---

## Next Steps

1. **Pick a learning path** above (Sequential, By Doing, or Reference)
2. **Start with Examples 1–3** to build intuition
3. **Run the integration example** on your own documents
4. **Compare embedding models** using the API examples
5. **Experiment with chunking** strategies (300 vs. 500 vs. 800 tokens)
6. **Move to Vector Databases module** when ready to scale

---

## File Manifest

```
embeddings/
├── README.md (you are here)
├── 00_embeddings_guide.md (14 sections, ~400 lines)
├── 01_practical_code_examples.md (4 examples + integration, ~300 lines)
└── 02_quick_reference.md (cheat sheet & decision trees, ~200 lines)
```

---

## Success Criteria

You'll know you're ready to move to Vector Databases when you can:
- [ ] Explain why cosine similarity works for embeddings (not Euclidean distance)
- [ ] Design chunking for your specific document type
- [ ] Build and query a simple vector store
- [ ] Compare embedding models on your domain
- [ ] Identify the bottleneck: is it embedding quality or search speed?

If the bottleneck is **search speed** (queries >100ms on 10K vectors), move to **Vector Databases**. If it's **quality**, tune your embedding model or chunking strategy here.

---

**Ready?** Start with [00_embeddings_guide.md](00_embeddings_guide.md), Section 1.

Next: [Vector Databases Module](../vector_databases/README.md) - Learn how to search millions of vectors in milliseconds.
