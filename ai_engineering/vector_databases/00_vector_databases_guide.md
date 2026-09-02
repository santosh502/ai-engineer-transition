# Phase 2B: Vector Databases & Approximate Nearest Neighbor Search

> Builds on: **Embeddings module** - understanding what embeddings are and how to compare them with cosine similarity.

## Learning Objectives

By the end of this phase, you will understand:
- What a vector database is and what it solves (scaling similarity search)
- Approximate Nearest Neighbor (ANN) algorithms and their trade-offs
- The major ANN algorithms: HNSW, IVF, LSH, Product Quantization
- How to choose the right vector database for your scale
- How to set up pgvector or Qdrant locally
- How to implement hybrid search combining dense embeddings + BM25 keyword search

---

# PART B - VECTOR DATABASES & ANN

## 10. What Is a Vector Database?

**Definition**: A database purpose-built to store vectors and answer "find me the K vectors most similar to this query vector" **fast**, even across millions/billions of vectors - using **approximate nearest neighbor (ANN)** search instead of brute-force comparison.

```
Brute force (Embeddings module):    Vector database:
compare query to EVERY vector       compare query to a SMART SUBSET
O(n) per query                      O(log n) or better, via an index
Fine for <100K vectors              Needed for millions/billions
```

It also typically bundles: metadata storage & filtering, persistence, horizontal scaling, hybrid (vector + keyword) search, and CRUD operations - everything the simple vector store doesn't have.

---

## 11. Types of Vector Databases

| Type | Examples | Notes |
|---|---|---|
| **Dedicated vector DB** | Pinecone, Qdrant, Weaviate, Milvus, Vespa | Built vector-first; strongest ANN performance & features |
| **Vector search library** (not a full DB) | FAISS, ScaNN, Annoy, hnswlib | You embed them in your own app; no persistence/server/metadata layer built-in |
| **Extension on existing DB** | pgvector (Postgres), Redis (RediSearch), Elasticsearch/OpenSearch (kNN) | Adds vector search to a DB you may already run - good for existing infra |
| **Embedded/local vector DB** | Chroma, LanceDB, SQLite-vss | Runs in-process, easy for prototyping, small-to-medium scale |

---

## 12. Algorithms Behind ANN Search

The core problem: exact nearest-neighbor search is O(n). ANN algorithms trade a *tiny* amount of accuracy for *massive* speed gains.

### 12.1 Flat / Brute-force
Compare the query to every vector. 100% accurate, doesn't scale. This is what the Embeddings module's simple vector store built.

### 12.2 IVF (Inverted File Index)
```
Step 1: Cluster all vectors into N "buckets" (via k-means)
Step 2: At query time, find the nearest few bucket centers
Step 3: Only search inside those buckets

      ●●●          ●●
     ●●●●●   ●●●   ●●●●
      ●●●          ●●●
    (bucket A)   (bucket B)

Query lands near bucket A's center →
only compare against bucket A's vectors, skip the rest.
```
Trade-off: `nprobe` (how many buckets to check) controls speed vs. accuracy.

**Visual reference:** https://github.com/facebookresearch/faiss/wiki/Illustrated-Faiss (Facebook FAISS interactive guide)

### 12.3 HNSW (Hierarchical Navigable Small World)
The most widely used ANN algorithm today (Qdrant, Weaviate, pgvector's default option).
```
Layer 2:  ●───────────●              (few nodes, long "highway" links)
Layer 1:  ●───●───●───●───●          (more nodes, medium links)
Layer 0:  ●─●─●─●─●─●─●─●─●─●─●─●    (every vector, short links)

Search starts at the top sparse layer, "zooms in" through
denser layers - like using highways then local roads to
reach an exact address. Very fast, very accurate, memory-hungry.
```

**Paper & visual:** 
- Original HNSW paper: https://arxiv.org/abs/1603.09320
- Interactive visualization: https://github.com/nmslib/hnswlib

### 12.4 LSH (Locality-Sensitive Hashing)
Hashes similar vectors into the same "bucket" with high probability, dissimilar ones into different buckets - search only within matching hash buckets. Older technique, largely superseded by HNSW for text embeddings but still used in some large-scale systems.

### 12.5 Product Quantization (PQ)
A **compression** technique, often combined with IVF or HNSW: splits each vector into sub-vectors and replaces each with a small learned "code," shrinking memory footprint (e.g. Milvus/FAISS's `IVF+PQ`). Trades a little accuracy for a large reduction in RAM usage - critical at billion-scale.

### 12.6 Quick comparison
| Algorithm | Speed | Accuracy | Memory | Good for |
|---|---|---|---|---|
| Flat | Slow at scale | 100% (exact) | Low | Small datasets, ground-truth eval |
| IVF | Fast | High (tunable) | Medium | Medium-large datasets |
| HNSW | Very fast | Very high | High | Most production use cases |
| LSH | Fast | Medium | Low | Very large scale, memory-constrained |
| IVF+PQ | Fast | Medium-high | Very low | Billion-scale, memory-constrained |

---

## 13. Comparing Top Vector Databases

| DB | Type | Index | Metadata filtering | Hybrid search | Managed cloud option | Best for |
|---|---|---|---|---|---|---|
| **Pinecone** | Dedicated, managed-only | Proprietary (HNSW-like) | Yes | Yes (sparse+dense) | Yes (only option) | Teams wanting zero ops |
| **Qdrant** | Dedicated | HNSW | Yes, very strong | Yes | Yes + self-host | Best balance of power & simplicity |
| **Weaviate** | Dedicated | HNSW | Yes | Yes (built-in BM25) | Yes + self-host | GraphQL-style APIs, modules ecosystem |
| **Milvus** | Dedicated | IVF, HNSW, PQ, many | Yes | Partial | Yes (Zilliz) + self-host | Massive scale (billions of vectors) |
| **pgvector** | Postgres extension | IVFFlat, HNSW | Full SQL power | Via SQL + `tsvector` | Via managed Postgres (Supabase, RDS, Neon) | Teams already on Postgres, transactional data + vectors together |
| **Chroma** | Embedded/local | HNSW | Basic | Basic | Chroma Cloud | Prototyping, small apps, notebooks |
| **FAISS** | Library, not a DB | Flat, IVF, HNSW, PQ | Manual (you build it) | Manual | N/A | Research, custom pipelines, max control |

**Practical picks:**
- Already using Postgres, want simplicity + SQL joins with vectors → **pgvector**
- Want a dedicated, easy-to-run, feature-rich DB → **Qdrant**
- Need billion-scale, distributed → **Milvus**
- Want fully managed with no ops at all → **Pinecone**

---

## 14. Choose & Setup: pgvector or Qdrant

### 14.1 pgvector (Postgres)
```sql
-- Enable extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Table with a vector column
CREATE TABLE chunks (
    id SERIAL PRIMARY KEY,
    content TEXT,
    metadata JSONB,
    embedding VECTOR(1536)
);

-- HNSW index for fast approximate search
CREATE INDEX ON chunks USING hnsw (embedding vector_cosine_ops);

-- Query: top 5 most similar, with metadata filter
SELECT content, metadata, 1 - (embedding <=> $1) AS similarity
FROM chunks
WHERE metadata->>'category' = 'chapter_3'
ORDER BY embedding <=> $1
LIMIT 5;
-- <=> is pgvector's cosine distance operator
```

### 14.2 Qdrant (Python client, local Docker)
```bash
docker run -p 6333:6333 qdrant/qdrant
```
```python
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct, Filter, FieldCondition, MatchValue

client = QdrantClient(url="http://localhost:6333")

client.create_collection(
    collection_name="docs",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
)

client.upsert(
    collection_name="docs",
    points=[
        PointStruct(id=1, vector=embed("chunk text here"),
                    payload={"category": "chapter_3", "text": "chunk text here"})
    ],
)

results = client.search(
    collection_name="docs",
    query_vector=embed("my query"),
    query_filter=Filter(must=[FieldCondition(key="category", match=MatchValue(value="chapter_3"))]),
    limit=5,
)
```

---

## 15. Rebuild: Real Vector DB + Metadata Filtering

Take the pipeline from the Embeddings module and swap the simple vector store for pgvector or Qdrant:

```
Before (Embeddings module):         After (This module):
Python list of (vector, text)   →    pgvector table / Qdrant collection
Linear scan cosine similarity   →    HNSW-indexed ANN search
No filtering                    →    WHERE category = 'x' / payload filter
Loses state on restart          →    Persisted to disk
```

**Metadata filtering example use cases:**
- Only search within a specific book/chapter/user's documents
- Filter by date range ("only docs from last 30 days")
- Combine access control with search ("only docs this user is allowed to see")

---

## 16. Implement: BM25 / Keyword Search (For Hybrid Retrieval)

### 16.1 Why add keyword search back in?
Dense embeddings are great at *semantic* similarity but sometimes miss **exact terms** that matter a lot - product codes, names, acronyms, numbers ("error E402", "ISO 9001"). BM25 (a refinement of TF-IDF) excels at exactly that.

### 16.2 BM25 formula (conceptually)
```
score(query, doc) = Σ over query terms of:
    IDF(term) × ( TF(term, doc) × (k1 + 1) )
                ─────────────────────────────────────────
                TF(term, doc) + k1 × (1 - b + b × |doc|/avgdl)

IDF = rarer terms score higher (inverse document frequency)
TF  = more occurrences of the term in this doc score higher,
      but with diminishing returns (saturation via k1)
b, k1 = tuning constants (length normalization, saturation)
```
You don't need to memorize the formula - the intuition is: **rare, frequent-in-this-doc terms win**, with a penalty for very long documents so they don't win purely from having more words.

**Reference:**
- BM25 explained: https://en.wikipedia.org/wiki/Okapi_BM25
- Python implementation: https://github.com/dorianbrown/rank_bm25

### 16.3 Hybrid search pattern
```
Query
  │
  ├──► Dense embedding search (semantic)  → results A (ranked)
  │
  └──► BM25 keyword search (lexical)      → results B (ranked)
                │
                ▼
      Combine via Reciprocal Rank Fusion (RRF)
      or a weighted score blend
                │
                ▼
         Final re-ranked result list
```

**Reciprocal Rank Fusion (RRF)** - simple, framework-free way to merge two ranked lists:
```python
def reciprocal_rank_fusion(rank_lists, k=60):
    scores = {}
    for ranked_ids in rank_lists:          # e.g. [semantic_ids, bm25_ids]
        for rank, doc_id in enumerate(ranked_ids):
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1)
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)
```

Most production vector DBs (Weaviate, Qdrant, Pinecone) now have hybrid search built in - but implementing RRF by hand once (like the manual cosine similarity in Embeddings module) is the fastest way to *understand* what's happening under the hood.

---

## 17. Summary Tables

### Vector Databases
| Concept | Meaning |
|---|---|
| Vector DB | Stores vectors + metadata, answers similarity search fast at scale |
| ANN | Approximate Nearest Neighbor - trades tiny accuracy loss for huge speed gains |
| HNSW | Layered graph index; the modern default algorithm |
| IVF | Cluster-then-search index |
| PQ | Vector compression for memory efficiency |
| Hybrid search | Combines dense (semantic) + sparse/BM25 (keyword) search |

---

## 18. Practice Problems

1. Explain, in your own words, why HNSW is faster than brute-force flat search - what is it skipping, and why is that usually safe?
2. Your search returns semantically relevant but wrong-product results because your product codes ("SKU-4471") aren't matching. What retrieval change fixes this?
3. You have 50,000 documents. Would you reach for FAISS, pgvector, or Pinecone first? Justify based on your team's existing stack and ops appetite.
4. At what scale does a vector DB become necessary? (Hint: depends on latency tolerance and infrastructure)
5. Design a hybrid search: you have 1M documents, each scored by both semantic similarity and BM25. How do you combine the scores?

---

## 19. Key Takeaways

✓ **Vector databases** exist purely to make "find nearest vectors" fast at scale via ANN algorithms like HNSW

✓ **ANN trades accuracy for speed** - but the accuracy loss is tiny (<1%) for huge speed gains (100x+)

✓ **No single best vector DB** - pick based on scale, existing infra (Postgres? → pgvector), and ops appetite

✓ **HNSW is the modern default** - fast, accurate, used by Qdrant/Weaviate/pgvector

✓ **Hybrid search** (dense + BM25) beats pure semantic search whenever exact terms/codes/names matter

✓ **Start with pgvector or Qdrant** - both are solid for most use cases up to billions of vectors

---

## 20. Recommended Next Steps

1. Choose pgvector or Qdrant (see decision tree in Quick Reference)
2. Stand up locally (Section 14) and migrate your Embeddings module pipeline
3. Add metadata filtering + BM25 hybrid search (Sections 15–16)
4. Benchmark: what's your query latency at 1K, 10K, 100K vectors?
5. Move to **Phase 4: Retrieval-Augmented Generation (RAG)** - using retrieved chunks to ground an LLM's answers

---

## 21. Online Resources & Visualizations

### Interactive Tools
- **FAISS Wiki with Illustrations**: https://github.com/facebookresearch/faiss/wiki/Illustrated-Faiss - visual guide to vector search algorithms
- **Qdrant Documentation & Examples**: https://qdrant.tech/documentation/ - live interactive examples

### Papers & References
- **HNSW Paper (Arxiv)**: https://arxiv.org/abs/1603.09320 - foundational algorithm
- **FAISS Repo**: https://github.com/facebookresearch/faiss - industry-standard vector search library
- **Pinecone's Vector Search Guide**: https://www.pinecone.io/learn/vector-search/ - comprehensive, industry-friendly

### Articles
- **Weaviate vs Qdrant**: https://weaviate.io/blog/qdrant-vs-weaviate - detailed product comparison
