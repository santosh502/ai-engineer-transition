# Phase 2B: Vector Databases - Approximate Nearest Neighbor Search

**Materials**: [Overview](README.md) - [00: Vector Databases Guide](00_vector_databases_guide.md) - [01: Code Examples](01_practical_code_examples.md) - [02: Quick Reference](02_quick_reference.md)

Learn how to scale semantic search to millions of vectors using ANN algorithms and production vector databases.

## Content

### 1. **[00_vector_databases_guide.md](00_vector_databases_guide.md)** (Main Guide)
Complete walkthrough covering:
- What a vector database is and what it solves
- Approximate Nearest Neighbor (ANN) algorithms in depth
  - Flat/Brute-force
  - IVF (Inverted File Index)
  - HNSW (Hierarchical Navigable Small World) - the modern default
  - LSH (Locality-Sensitive Hashing)
  - Product Quantization (PQ) - compression for billion-scale
- Detailed comparison of top vector databases
- pgvector (Postgres) and Qdrant setup
- Metadata filtering and hybrid search
- BM25 keyword search for exact-term matching

**Sections:**
10. What Is a Vector Database?
11. Types of Vector Databases
12. ANN Algorithms (Flat, IVF, HNSW, LSH, PQ)
13. Comparing Top Vector Databases
14. pgvector and Qdrant Setup
15. Metadata Filtering
16. Hybrid Search (Semantic + Keyword)

---

### 2. **[01_practical_code_examples.md](01_practical_code_examples.md)** (Runnable Code)
6 complete examples you can run right now:
- Example 5: pgvector SQL setup
- Example 6: Qdrant Python client setup
- Example 7: Docker quick start for Qdrant
- Example 8: Reciprocal Rank Fusion (RRF) for merging search results
- Example 9: BM25 scoring from scratch
- **Integration Example:** Complete end-to-end pipeline with real vector DB

All self-contained, progressively building toward production setup.

---

### 3. **[02_quick_reference.md](02_quick_reference.md)** (Cheat Sheet)
Quick lookups:
- Vector database decision tree (choose your DB)
- Algorithm comparison and when to use each
- Top vector databases compared in one table
- Metadata filtering examples for each DB
- Hybrid search workflow
- Common mistakes & how to fix them
- Performance tuning checklist
- Cost comparison (2024 pricing)
- Debugging guide (why is search slow?)

---

## How to Use

### Option 1: Learn Sequentially (First Time)
1. Read **Main Guide** (`00_*`), Sections 10–16
2. Run **Examples 5–9** from `01_*` (setup + algorithms)
3. Run the **Integration Example** on your documents
4. Keep `02_*` handy for DB selection

**Time:** 1 week (includes hands-on setup)

### Option 2: Learn By Doing (Experienced Learners)
1. Use decision tree in `02_*` to choose a DB
2. Run Example 5 or 6 (pgvector or Qdrant setup)
3. Run the Integration Example on your docs
4. Read relevant sections in `00_*` when curious about "why"

**Time:** 2–3 days

### Option 3: Reference Only (Experts)
1. Use `02_*` quick reference for DB/algorithm decisions
2. Copy Example 5 or 6 for your DB of choice
3. Dip into `00_*` only for deep algorithm understanding

---

## Quick Start - 1 Hour

```
1. Read: Vector DB decision tree in quick reference (02_*)
   → Choose: Qdrant (easiest), pgvector (if using Postgres), or Pinecone

2. Run: Example 6 (Qdrant Docker)
   → docker run -p 6333:6333 qdrant/qdrant

3. Run: Integration example on your documents
   → Full end-to-end search in <50 lines

4. Add: Hybrid search (Example 8)
   → Combine semantic + keyword search
```

You now have production-ready vector search.

---

## Key Concepts at a Glance

| Concept | In One Sentence |
|---|---|
| **Vector DB** | A database that answers "find K vectors most similar to query" fast using ANN indexing |
| **ANN** | Approximate Nearest Neighbor - trades <1% accuracy loss for 100x speed gain |
| **HNSW** | Layered graph index, modern default, used by Qdrant/Weaviate/pgvector |
| **IVF** | Cluster-then-search, ~95% accuracy, good middle ground between speed and accuracy |
| **Metadata filtering** | Restrict search to subset of vectors (e.g., "only docs from 2024") |
| **Hybrid search** | Combine semantic (dense embeddings) + keyword (BM25) for best of both |

---

## Learning Path

### Phase 2B: Vector Database Mastery (1 week)

**Days 1–2: Concepts**
- [ ] Read Sections 10–13 (what vector DBs solve, ANN algorithms, DB comparison)
- [ ] Run Examples 5–7 (setup pgvector or Qdrant)
- [ ] Understand decision tree in quick reference

**Days 3–5: Implementation**
- [ ] Read Sections 14–16 (metadata filtering, hybrid search)
- [ ] Run Examples 8–9 (RRF, BM25)
- [ ] Run integration example on real documents
- [ ] Profile latency at 1K, 10K, 100K vectors

**Days 6–7: Production**
- [ ] Implement hybrid search on your dataset
- [ ] Add metadata filtering
- [ ] Profile and optimize
- [ ] Document your chunking + DB choice

---

## Learning Outcomes

By the end of this phase, you will:
- [ ] **Understand ANN algorithms** and trade-offs between speed/accuracy
- [ ] **Choose the right vector DB** for your scale (millions vs. billions)
- [ ] **Set up pgvector or Qdrant** locally and in production
- [ ] **Implement metadata filtering** to restrict search scope
- [ ] **Build hybrid search** combining semantic + keyword retrieval
- [ ] **Profile and optimize** vector database queries
- [ ] **Evaluate retrieval quality** at different scales

---

## Tech Stack Recommendations

**Choose One Vector DB:**
- **pgvector** - if already using Postgres
- **Qdrant** - easiest standalone option
- **Pinecone** - managed (zero ops) but most expensive
- **Milvus** - if needing billion-scale distributed

**For Hybrid Search:**
- Built-in (Qdrant, Weaviate, Pinecone)
- Or combine with `rank_bm25` library (Python)

**For Local Development:**
- Qdrant Docker: `docker run -p 6333:6333 qdrant/qdrant`
- pgvector: `docker run -e POSTGRES_PASSWORD=postgres postgres:15`

---

## Connections to Other Phases

- **Embeddings module** (Phase 2A): These chunks are your embedded documents
- **Phase 4 (RAG):** Vector DBs provide the retrieval engine for LLM grounding
- **Phase 5 (Agents):** Can use vector search to retrieve tool documentation

---

## Why Learn This?

1. **Scale:** Understand how to go from "thousands" to "millions" of vectors without sacrificing speed
2. **Production:** Real vector DBs handle metadata, filtering, persistence, caching - not just similarity search
3. **Algorithms:** HNSW is used by Qdrant, Weaviate, pgvector - understanding it helps you pick DB parameters
4. **Hybrid search:** Semantic search alone misses exact terms (product codes, names) - BM25 catches them
5. **Cost:** Wrong DB choice can cost 10x more; right choice saves money at scale

---

## FAQ

**Q: When do I need a vector DB vs. simple vector store?**
A: When you hit >10K vectors OR need <100ms query latency OR want metadata filtering. Before that, Embeddings module's simple store works fine.

**Q: Should I use pgvector or Qdrant?**
A: Qdrant if starting fresh (easier, faster). pgvector if already on Postgres (one less infrastructure).

**Q: How much faster is ANN than brute-force?**
A: At 1M vectors: brute-force = ~500ms, HNSW = ~5ms. That's 100x faster with <1% accuracy loss.

**Q: Do I need hybrid search?**
A: If your queries include product codes, names, acronyms (E402, SKU-1234) → yes. If purely semantic → maybe not.

**Q: Can I migrate from one DB to another later?**
A: Yes, but plan for it. Start with what fits your current scale; migrate if you outgrow it.

**Q: What's the cost at scale?**
A: Pinecone: expensive ($0.40/month + per-query). Self-hosted Qdrant: cheap (~$10/month for millions of vectors).

---

## Next Steps

1. **Choose a vector DB** using decision tree in quick reference
2. **Set up locally** (Example 5 for pgvector, Example 6 for Qdrant)
3. **Migrate your Embeddings module pipeline** to use real vector DB
4. **Add metadata filtering** (Section 15)
5. **Implement hybrid search** (Section 16, Example 8)
6. **Profile latency** at 1K, 10K, 100K, 1M vectors
7. **Move to Phase 4: Retrieval-Augmented Generation (RAG)** - using these vectors to ground LLM answers

---

## File Manifest

```
vector_databases/
├── README.md (you are here)
├── 00_vector_databases_guide.md (Sections 10-16, ~400 lines)
├── 01_practical_code_examples.md (6 examples + integration, ~400 lines)
└── 02_quick_reference.md (cheat sheet & decision trees, ~300 lines)
```

---

## Success Criteria

You'll know you're ready to move to Phase 4 (RAG) when you can:
- [ ] Explain why HNSW is faster than flat brute-force search
- [ ] Choose the right vector DB for your scale
- [ ] Set up and query pgvector or Qdrant
- [ ] Add metadata filtering to restrict search scope
- [ ] Implement hybrid search (semantic + BM25)
- [ ] Profile query latency and identify bottlenecks
- [ ] Know when to optimize vs. when to move to RAG

---

**Ready?** Start with [00_vector_databases_guide.md](00_vector_databases_guide.md), Section 10.

**Next:** [Phase 4: Retrieval-Augmented Generation (RAG)](../rag/README.md) - Ground LLM answers in your vectors.
