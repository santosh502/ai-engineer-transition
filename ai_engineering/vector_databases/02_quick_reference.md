# Vector Databases - Quick Reference

## One-Page Cheat Sheet

### Vector Database Decision Tree

```
Do you already use Postgres?
├─ YES → pgvector
│        (SQL, transactional, simpler ops, join with other tables)
└─ NO
   │
   Do you want fully managed, zero ops?
   ├─ YES → Pinecone
   │        (Easy API, pay per query, cloud-only)
   └─ NO
      │
      How many vectors? (millions or billions?)
      ├─ Millions → Qdrant or Weaviate
      │            (Self-host or managed, feature-rich, HNSW)
      └─ Billions → Milvus
                    (Massive scale, distributed, IVF/HNSW/PQ)
```

---

### Algorithms: When to Use

| Algorithm | Speed vs. Accuracy | Best For | Trade-off |
|---|---|---|---|
| **Flat** | Trade speed for 100% accuracy | <100K vectors, evaluation baseline | Slow for scale |
| **IVF** | ~95% accuracy, faster | 100K–10M vectors, good default | Tuning `nprobe` needed |
| **HNSW** | ~98% accuracy, very fast | 100K–100M vectors, production standard | Memory-hungry |
| **LSH** | ~90% accuracy, super fast | 100M+ vectors, real-time latency critical | Lower accuracy |
| **PQ** | Compression, reduces memory 10x | Billion-scale, memory-constrained | Trades accuracy for space |

---

### Top Vector Databases Compared

| DB | Type | Index | Scale | Metadata Filtering | Hybrid Search | Managed Option | Best For |
|---|---|---|---|---|---|---|---|
| **Qdrant** | Dedicated | HNSW | 1M–1B | Excellent | Built-in | Yes (Qdrant Cloud) | Best all-rounder |
| **pgvector** | Postgres extension | HNSW, IVF | 1M–100M | SQL power | Via SQL + tsvector | Via managed Postgres | Postgres users |
| **Pinecone** | Dedicated managed | Proprietary | 1M–1B | Yes | Built-in | Yes (only option) | Zero-ops teams |
| **Weaviate** | Dedicated | HNSW | 1M–1B | Excellent | Built-in BM25 | Yes | GraphQL users |
| **Milvus** | Dedicated | IVF, HNSW, PQ | 1B+ | Yes | Partial | Yes (Zilliz) | Billion-scale |
| **Chroma** | Embedded | HNSW | <100M | Basic | Basic | Chroma Cloud | Prototyping |
| **FAISS** | Library | Flat, IVF, PQ | Any | Manual | Manual | N/A | Research, control |

---

### Quick Setup Guide

**Qdrant (Docker, 30 seconds):**
```bash
docker run -p 6333:6333 qdrant/qdrant
```

**pgvector (Postgres):**
```bash
# Install extension (once per database)
psql -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

**Pinecone:**
- Sign up at pinecone.io
- Get API key
- Use SDK directly (no infrastructure setup)

---

### Metadata Filtering Examples

**Qdrant:**
```python
Filter(must=[
    FieldCondition(key="category", match=MatchValue(value="royalty"))
])
```

**pgvector (SQL):**
```sql
WHERE metadata->>'category' = 'royalty'
```

**Pinecone:**
```python
filter={"category": "royalty"}
```

---

### Hybrid Search Workflow

```
Query
  ↓
1. Embed query (dense)          → Vector A
2. Tokenize query (sparse)      → Tokens B
  ↓
3a. Vector search (semantic)    → Semantic results + scores
3b. BM25 search (keyword)       → Keyword results + scores
  ↓
4. Merge via RRF or weighting   → Final ranked results
  ↓
Result (re-ranked)
```

**Quick formula (Reciprocal Rank Fusion):**
```python
final_score[doc] = Σ (1 / (k + rank + 1)) for each ranking
# typical k = 60
```

---

### Common Mistakes to Avoid

| Mistake | Impact | Fix |
|---|---|---|
| **Choosing wrong DB for scale** | Expensive or slow | Use decision tree above |
| **Not indexing vectors** | Queries O(n) forever | Create HNSW/IVF index |
| **Metadata filter in Python post-query** | Filter 10K results in code | Filter in DB query |
| **Forgetting to normalize vectors** | Wrong similarity scores | Check embedding model docs |
| **Searching without hybrid** | Misses acronyms, product codes | Add BM25 keyword search |
| **Testing on 1K vectors only** | Doesn't reveal scale issues | Profile at 100K, 1M |
| **Ignoring query latency** | Discovers issue in production | Profile before shipping |

---

### Performance Tuning Checklist

- [ ] Vector DB chosen (Qdrant, pgvector, or Pinecone)
- [ ] Local or cloud setup complete
- [ ] Index created (HNSW or IVF)
- [ ] Metadata filtering tested
- [ ] Hybrid search implemented (Example 8)
- [ ] Query latency profiled at 1K, 10K, 100K, 1M vectors
- [ ] Batch upsert implemented (faster than one-at-a-time)
- [ ] Caching strategy considered (cache query results)

---

### Typical Costs (2024)

| Provider | Model/Option | Cost | Notes |
|---|---|---|---|
| **Pinecone** | Starter pod | $0.40/month + $0.16/compute-hour | Pay per query, managed |
| **Qdrant** | Cloud | $0.40/month + storage | Managed multi-region |
| **pgvector** | Self-hosted (AWS t3.small) | ~$10/month | Just Postgres compute |
| **Self-hosted GPU** | Local or cloud GPU | $1–5/month | Full control, cheap |

**Rule:** For <1M queries/month, Pinecone is fine. Beyond that, self-hosted (Qdrant + pgvector) wins.

---

### Debug: Why Is My Vector DB Search Slow?

1. **Is the index built?** Check HNSW/IVF is created, not Flat
   ```sql
   -- pgvector
   SELECT schemaname, tablename, indexname FROM pg_indexes WHERE tablename='chunks';
   ```

2. **What's the query latency?** Should be <100ms for 1M vectors
   ```python
   import time
   start = time.time()
   results = client.search(...)
   print(f"Query: {(time.time() - start) * 1000:.2f}ms")
   ```

3. **Is metadata filtering happening in DB?** Don't fetch 1M and filter in Python
   ```python
   # WRONG: fetches 1M results
   results = client.search(..., limit=1000000)
   filtered = [r for r in results if r.payload["category"] == "x"]
   
   # RIGHT: filter in query
   results = client.search(..., filter=Filter(...), limit=5)
   ```

4. **Hitting memory limits?** Check if DB has enough RAM
   ```python
   # If latency suddenly increases, you may be swapping to disk
   ```

5. **Network latency?** If remote DB, is it geographically close?
   ```python
   # Local Qdrant: <5ms latency typical
   # Cloud Qdrant: 20-50ms typical
   # If >100ms, investigate network
   ```

---

### Timeline: How Long to Learn This?

| Topic | Time | Resources |
|---|---|---|
| Understanding ANN algorithms | 1–2 hours | Section 12 (Guide) |
| Set up pgvector or Qdrant locally | 30 min | Example 5-6 (Code) |
| Add metadata filtering | 30 min | Guide Section 15, Code |
| Implement hybrid search | 1–2 hours | Section 16, Example 8 |
| **Full Vector DB mastery** | 1 week | Theory + hands-on |

---

### Resources to Bookmark

- **HNSW Paper**: https://arxiv.org/abs/1603.09320 (the algorithm)
- **FAISS Wiki**: https://github.com/facebookresearch/faiss/wiki/Illustrated-Faiss (illustrated algorithms)
- **Qdrant Docs**: https://qdrant.tech/documentation/ (best self-hosted option)
- **pgvector Docs**: https://pgvector.readthedocs.io/ (Postgres extension)
- **Pinecone Guide**: https://www.pinecone.io/learn/vector-search/ (managed option)

---

### One Example: End-to-End with Qdrant

```python
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct, Filter, FieldCondition, MatchValue

# 1. Setup
client = QdrantClient(":memory:")
client.create_collection("docs", vectors_config=VectorParams(size=1536, distance=Distance.COSINE))

# 2. Insert vectors
vectors_to_insert = []
for doc_id, (text, embedding, category) in enumerate(your_documents):
    vectors_to_insert.append(
        PointStruct(id=doc_id, vector=embedding, payload={"text": text, "category": category})
    )
client.upsert("docs", vectors_to_insert)

# 3. Search with filter
query_embedding = embed("royal families")
results = client.search(
    "docs",
    query_vector=query_embedding,
    query_filter=Filter(must=[FieldCondition(key="category", match=MatchValue(value="royalty"))]),
    limit=5,
    with_payload=True,
)

# 4. Print results
for result in results:
    print(f"Similarity: {result.score:.4f}, Text: {result.payload['text'][:50]}...")
```

Done! You have fast vector search at scale.

---

### Next: Hybrid Search

Most production systems combine:
1. **Dense (semantic) search** - catches meaning
2. **BM25 (keyword) search** - catches exact terms/codes
3. **RRF (fusion)** - merges results

See Example 8 in Practical Code Examples for full implementation.

---

### Next: Phase 4 (RAG)

Vector databases are the retrieval engine for RAG. Once you have fast vector search working, move to RAG to:
- Ground LLM answers in your vectors
- Evaluate retrieval quality (recall@k, MRR)
- Handle context window limits
- Add re-ranking for higher precision
