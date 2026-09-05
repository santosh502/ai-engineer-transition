# How It All Fits Together: The Complete RAG Pipeline

If you're learning embeddings, vector databases, and RAG separately, you might miss how they actually work together. This page shows the **full system** and maps concepts to where they're explained.

---

## The Complete RAG Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        OFFLINE PHASE                             │
│           (Run once when you set up your knowledge base)         │
└─────────────────────────────────────────────────────────────────┘

📄 Raw Documents
   │
   ▼
┌─────────────────────────────────────────────────────────────────┐
│ CHUNKING: Split documents into manageable pieces                │
│ Learn here: embeddings/Section 6 OR rag/chunking-strategies.md  │
│                                                                  │
│ Common chunk sizes: 300-800 tokens                              │
│ Common overlap: 10-20%                                          │
│                                                                  │
│ Example: A 10-page doc → 20-30 chunks                           │
└─────────────────────────────────────────────────────────────────┘
   │
   ▼
┌─────────────────────────────────────────────────────────────────┐
│ EMBEDDING: Convert chunks to numerical vectors                  │
│ Learn here: embeddings/Sections 1-5, 8-9                       │
│                                                                  │
│ Models: text-embedding-3-small, all-MiniLM-L6-v2, bge-large    │
│ Output: Each chunk → vector of 384-3072 numbers                │
│                                                                  │
│ ⚠️ CRITICAL: Use the SAME model everywhere                      │
│ If you switch models later, vectors become incomparable         │
└─────────────────────────────────────────────────────────────────┘
   │
   ▼
🗄️  VECTOR DATABASE: Store vectors + metadata for fast retrieval
   │ Learn here: vector_databases/Sections 10-16
   │
   ├─ What gets stored:
   │  • The embedding vector (e.g., [0.12, -0.45, 0.89, ...])
   │  • The original chunk text
   │  • Metadata: source doc, page #, timestamp, etc.
   │
   ├─ Indexing algorithms:
   │  • HNSW (Qdrant, pgvector, Weaviate) - fastest, most popular
   │  • IVF (Milvus, FAISS) - good balance
   │  • Flat (for <10K vectors, full comparison)
   │
   └─ Database choices:
      • pgvector (if already using Postgres)
      • Qdrant (easiest, most feature-rich)
      • Pinecone (managed, most expensive)
      • FAISS (pure Python, no server)


┌─────────────────────────────────────────────────────────────────┐
│                        ONLINE PHASE                              │
│              (Run every time a user asks a question)             │
└─────────────────────────────────────────────────────────────────┘

❓ User Query
   │
   ▼
┌─────────────────────────────────────────────────────────────────┐
│ QUERY ENCODING: Convert query to vector                         │
│ (Using the SAME embedding model from offline phase)             │
│                                                                  │
│ Input: "How does embeddings work?"                              │
│ Output: [0.15, -0.42, 0.88, ...] (same dimensions as chunks)   │
└─────────────────────────────────────────────────────────────────┘
   │
   ▼
┌─────────────────────────────────────────────────────────────────┐
│ RETRIEVAL: Find similar chunks from vector database             │
│ Learn here: vector_databases/Sections 13-16                    │
│                                                                  │
│ How it works:                                                    │
│ 1. Vector DB compares query vector to all stored vectors       │
│ 2. Uses ANN algorithm (HNSW) to find top-K similar chunks      │
│ 3. Returns chunks ranked by similarity score                    │
│                                                                  │
│ Typical: retrieve top 4-5 chunks                                │
│ Similarity score: 0.0 (unrelated) to 1.0 (identical)           │
│                                                                  │
│ Optional: Add BM25 keyword search for exact-term matching      │
│ (useful for product codes, acronyms)                            │
└─────────────────────────────────────────────────────────────────┘
   │
   ▼
📚 Retrieved Context
   │ Top 4-5 most similar chunks from your knowledge base
   │
   ▼
┌─────────────────────────────────────────────────────────────────┐
│ AUGMENTATION: Combine query + retrieved context                 │
│                                                                  │
│ Format it into a prompt:                                        │
│                                                                  │
│ "You are a helpful assistant. Answer based ONLY on the         │
│  context below. If the answer isn't in the context, say         │
│  'I don't know'.                                                │
│                                                                  │
│  Context:                                                        │
│  [Chunk 1: ...]                                                 │
│  [Chunk 2: ...]                                                 │
│  [Chunk 3: ...]                                                 │
│                                                                  │
│  Question: How does embeddings work?"                           │
└─────────────────────────────────────────────────────────────────┘
   │
   ▼
┌─────────────────────────────────────────────────────────────────┐
│ GENERATION: LLM generates grounded answer                       │
│ Learn here: rag/notes.md Section 5                              │
│                                                                  │
│ LLM reads: Question + Context                                   │
│ LLM generates: Answer based only on context                     │
│ Quality depends on: retrieval quality + prompt quality          │
└─────────────────────────────────────────────────────────────────┘
   │
   ▼
✅ Answer (grounded in your data, not hallucinated)
```

---

## Concept Map: Where Each Piece Lives

| Concept | Module | Section | Purpose |
|---------|--------|---------|---------|
| **What are vectors?** | Embeddings | Sections 1-5 | Foundation: geometry of meaning |
| **Cosine similarity** | Embeddings | Section 5 | How to compare vectors |
| **Chunking strategies** | RAG | chunking-strategies.md | How to split documents |
| **Embedding models** | Embeddings | Sections 8-9 | Practical model comparison |
| **Building vector stores** | Embeddings | Sections 7-8 | From scratch, no framework |
| **ANN algorithms** | Vector DBs | Section 12 | How to scale retrieval |
| **Choosing a vector DB** | Vector DBs | Section 13 | pgvector? Qdrant? Pinecone? |
| **Metadata filtering** | Vector DBs | Section 15 | Filter retrieved results |
| **Hybrid search** | Vector DBs | Section 16 | Dense + sparse retrieval |
| **RAG pipeline** | RAG | notes.md | Complete system |
| **Troubleshooting** | RAG | troubleshooting.md | When things break |

---

## Real Example: Building a Question-Answering System Over Your Company Docs

Let's trace through a complete example to show how everything connects.

### Offline: Setting Up the Knowledge Base

```
STEP 1: Load company docs (100 PDF documents)
├─ HR handbook
├─ Engineering best practices
├─ Product documentation
└─ Meeting transcripts

STEP 2: Chunk them
├─ HR handbook: 50 chunks of ~500 tokens each
├─ Engineering guide: 150 chunks
├─ Product docs: 200 chunks
├─ Meeting notes: 80 chunks
└─ Total: 480 chunks

STEP 3: Embed with text-embedding-3-small
├─ For each chunk: call OpenAI API
├─ Get back: 1536-dimensional vector
├─ Cost: 480 chunks × ~250 tokens/chunk ÷ 1M tokens × $0.02 = $0.002 (cheap!)
└─ Time: ~5 minutes

STEP 4: Store in Qdrant
├─ Create collection: "company_docs"
├─ Upsert 480 points:
│  • id: unique chunk ID
│  • vector: [0.12, -0.45, 0.88, ...] (1536 dims)
│  • payload: {
│      "text": "full chunk content",
│      "source": "HR handbook",
│      "page": 3,
│      "section": "Remote Work Policy"
│    }
└─ Build HNSW index (automatic)

✅ Knowledge base ready
```

### Online: Answering a User Question

```
USER QUESTION: "What's our remote work policy?"

STEP 1: Encode query
├─ Input: "What's our remote work policy?"
├─ Embedding model: text-embedding-3-small (SAME as indexing!)
├─ Output: [0.15, -0.43, 0.87, ...] (1536 dims)
└─ Cost: ~5 tokens × $0.02/1M = ~$0.0001

STEP 2: Search Qdrant
├─ Query vector: [0.15, -0.43, 0.87, ...]
├─ Vector DB: Compare against 480 stored vectors using HNSW
├─ Time: ~5ms (fast!)
├─ Returned:
│  1. (score: 0.94) HR handbook chunk: "Remote employees..."
│  2. (score: 0.91) HR handbook chunk: "Work from home benefits..."
│  3. (score: 0.88) HR handbook chunk: "Equipment stipend..."
│  4. (score: 0.85) HR handbook chunk: "Time zone expectations..."
└─ Takes top 4 (k=4)

STEP 3: Build prompt
├─ Combine query + retrieved chunks:
│
│ System: "You are an HR assistant. Answer based ONLY on the
│  provided policy. Do not make up policies."
│
│ Context:
│ [1] Remote employees are required to...
│ [2] Work from home benefits include...
│ [3] Equipment stipend of $500/year for...
│ [4] Time zone expectations: within 2 hours of...
│
│ Question: What's our remote work policy?
│
└─ Total prompt size: ~1200 tokens (well under LLM limit)

STEP 4: Generate answer
├─ LLM (Claude, GPT-4, etc.) reads the prompt
├─ Generates: "Based on company policy, remote employees must
│  be within 2 hours of a core business time zone. You get
│  $500/year equipment stipend and standard benefits for
│  remote work include..."
└─ Time: ~1-2 seconds (depends on LLM)

✅ ANSWER (grounded in company docs, not hallucinated)
```

### What If Something Goes Wrong?

Each step has failure modes. See troubleshooting.md:

| If This Happens | Check These |
|---|---|
| Got wrong policy docs | Verify embedding model consistency |
| Only 1-2 relevant chunks | Increase k (retrieve more) OR tune chunk size |
| Answer hallucinates | Verify prompt includes grounding instruction |
| Queries take 5+ seconds | Check vector DB index exists |
| Cost is very high | Caching embeddings? Re-embedding unchanged docs? |

---

## Design Decisions: Why Each Component

### Why Chunking?

```
❌ Can't embed entire 100-page document as one vector
   - Embedding model has token limit (~8K for most)
   - One vector averages too much (loses specificity)
   - LLM context window fills up with one chunk

✅ Chunk first, then embed
   - Smaller chunks = specific, precise vectors
   - More chunks = more retrieval options
   - Better control over context size to LLM
```

### Why Vector Database?

```
❌ Naive approach: compare query vector to ALL 480 stored vectors
   - Time: O(n) = 480 comparisons per query
   - Speed: ~50ms even for 480 vectors (manageable)
   - But scales terribly: 1M documents = 1M comparisons (~500ms)

✅ Vector database with HNSW index
   - Time: O(log n) ≈ 5-10ms even for 1M vectors (100x faster)
   - Trade-off: <1% accuracy loss (acceptable)
   - Scales to billions of vectors
```

### Why Embedding Model Consistency?

```
Model A trained on: "dog, cat, animal"      Model B trained on: "perro, gato, animale"
Model A: dog    = [0.9, 0.1, 0.5]          Model B: perro = [0.5, 0.8, 0.2]
Model A: cat    = [0.1, 0.9, 0.6]          Model B: gato  = [0.4, 0.9, 0.1]
Model A: animal = [0.8, 0.8, 0.9]          Model B: animal = [0.7, 0.7, 0.8]

Query (Model A): "dog"    = [0.9, 0.1, 0.5]
Similarity to (Model A): dog   = 1.0 ✅
Similarity to (Model B): perro = ??? ❌ (different semantic space)

→ Mixing models breaks geometry.
→ Use same model for indexing + querying.
```

### Why Hybrid Search?

```
Query: "error E402"

Dense search only (semantic):
✅ Finds: "system failures", "application exceptions"
❌ Misses: specific error code "E402"

BM25 keyword search only:
✅ Finds: "error E402", "error E401", "E402 handling"
❌ Misses: "When the system crashes" (related but no E402 token)

Hybrid (dense + BM25):
✅ Finds: "When system crashes with error E402"
✅ Both semantic understanding AND exact term matching
```

---

## Common Mistakes at Each Step

### Chunking Phase
- Chunks too large (>1500 tokens) → vectors lose specificity
- Chunks too small (<100 tokens) → lack context
- Inconsistent chunk sizes → some precise, some vague

### Embedding Phase
- ❌ Using different models at index vs. query time → complete failure
- Not using token-based chunking → multilingual docs silent overflow
- Not normalizing vectors → cosine similarity unreliable

### Vector DB Phase
- No index created → queries slow down
- Wrong database choice → scaling issues or cost explosion
- Metadata not preserved → can't trace where retrieved chunks came from

### Retrieval Phase
- Retrieving too few chunks (k=1) → incomplete context
- Retrieving too many chunks (k=100) → token overflow, hallucinations
- Not filtering by metadata → getting irrelevant docs from different knowledge bases

### Generation Phase
- Prompt doesn't tell LLM to use only context → hallucinations
- Context truncated due to token limits → LLM doesn't see the answer
- Bad query formatting → LLM confused about what it should answer

---

## Learning Path: How to Use All Three Modules

### Path A: Learn Concepts First (Recommended)
1. **Embeddings** (weeks 1-2)
   - Sections 1-5: understand vectors and similarity
   - Section 6: practice chunking by hand
   - Sections 7-9: understand practical trade-offs

2. **Vector Databases** (weeks 3-4)
   - Section 10-13: understand why DBs needed, which to pick
   - Section 14: set up pgvector or Qdrant locally
   - Sections 15-16: metadata filtering + hybrid search

3. **RAG** (weeks 5-6)
   - This architecture overview
   - notes.md: full RAG pipeline
   - implementation-examples.md: build it
   - troubleshooting.md: fix it when broken

### Path B: Learn By Doing (Faster)
1. **Read** this file (architecture-overview.md)
2. **Skim** embeddings README + vector_databases README
3. **Run** rag/implementation-examples.md "Simple RAG Pipeline"
4. **Read** sections in-depth only when curious about "why"

---

## Mental Model: Think of It As Layers

```
┌─────────────────────────────────────────┐
│  Generation Layer                       │ (LLM, prompt engineering)
│  rag/notes.md section 5                 │
└─────────────────────────────────────────┘
         ▲
         │ retrieved context
         │
┌─────────────────────────────────────────┐
│  Retrieval Layer                        │ (vector DB, ANN search)
│  vector_databases/ (all sections)       │
└─────────────────────────────────────────┘
         ▲
         │ stored vectors
         │
┌─────────────────────────────────────────┐
│  Embedding Layer                        │ (semantic representation)
│  embeddings/ (all sections)             │
└─────────────────────────────────────────┘
         ▲
         │ split text
         │
┌─────────────────────────────────────────┐
│  Chunking Layer                         │ (document preparation)
│  rag/chunking-strategies.md             │
└─────────────────────────────────────────┘
         ▲
         │ raw documents
         │
   Raw Knowledge Base
```

Each layer depends on the one below:
- Bad chunking → bad embeddings
- Bad embeddings → bad retrieval
- Bad retrieval → hallucinations in generation
- Good engineering at every layer → accurate, grounded answers

---

## Next Steps

1. **Understand the architecture** (you just did this) ✓
2. **Pick a learning path** (A or B above)
3. **Build locally** using rag/implementation-examples.md
4. **When it breaks** → use rag/troubleshooting.md
5. **When you're ready to scale** → reference quick guides in each module

---

## Quick Reference: What to Read When

| Question | Read This |
|----------|-----------|
| "How do embeddings work?" | embeddings/00_embeddings_guide.md Sections 1-5 |
| "How do I chunk documents?" | rag/chunking-strategies.md (pick 1-2 strategies) |
| "How do I compare vectors?" | embeddings/00_embeddings_guide.md Section 5 |
| "When do I need a vector DB?" | vector_databases/README.md |
| "Which vector DB should I use?" | vector_databases/02_quick_reference.md |
| "How does ANN work?" | vector_databases/00_vector_databases_guide.md Section 12 |
| "How do I build a RAG system?" | rag/README.md → implementation-examples.md |
| "My system is broken" | rag/troubleshooting.md |
| "I want production setup" | vector_databases/01_practical_code_examples.md |
| "I'm confused" | This file (you are here) |
