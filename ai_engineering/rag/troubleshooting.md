# RAG Troubleshooting Guide

When your RAG system isn't working as expected, use this guide to diagnose and fix the issue.

---

## Problem: Retrieved Docs Are Irrelevant

**Symptom:** Your RAG returns documents that don't match the query at all.

### Check these in order:

1. **Same embedding model for indexing + querying?** ⚠️ CRITICAL
   ```
   ❌ WRONG: Index docs with OpenAI, query with Cohere
   ✅ RIGHT: Use the same model everywhere
   
   How to verify:
   - Document: embedding model used at index time?
   - Query: what model are you using now?
   - If different: rebuild entire index with correct model
   ```

2. **Chunk size too big or too small?**
   ```
   Too small (< 100 tokens):
   - Each chunk lacks context
   - Vector embeddings too narrow in meaning
   - Try increasing to 300-500 tokens
   
   Too large (> 1500 tokens):
   - Multiple unrelated topics per chunk
   - Vector is "averaging" conflicting meanings
   - Try reducing to 500-800 tokens
   ```

3. **Have you reindexed after changing embedding model?**
   ```
   Common mistake:
   1. Build index with model A
   2. Switch to model B
   3. Query still uses old vectors from model A
   
   Fix: Completely rebuild index with new model
   ```

4. **Does hybrid search help?**
   ```
   Problem: Searching for "error E402" but getting semantic results
   Solution: Add BM25 keyword search
   
   Example:
   - Dense (semantic): finds "application failure"
   - BM25 (keyword): finds "error E402"
   - Combined: both precision + semantic understanding
   ```

5. **Is your query itself ambiguous?**
   ```
   Try query expansion:
   - Original: "how to configure"
   - Expanded: ["how to configure", "setup steps", "installation guide", ...]
   - Search with all versions, combine results
   ```

**Debug checklist:**
- [ ] Same embedding model used everywhere?
- [ ] Chunk sizes in 300-800 token range?
- [ ] Index rebuilt after model change?
- [ ] Tried hybrid search?
- [ ] Query too vague? Try rephrasing

---

## Problem: Hallucinations Even With Good Retrieval

**Symptom:** Retrieved context is correct, but LLM still generates false information.

### Check these in order:

1. **Is context actually being passed to the LLM?**
   ```python
   # Debug: Print what's being sent
   retrieved = retriever.get_relevant_documents(query)
   print(f"Retrieved {len(retrieved)} docs")
   print(f"Total tokens: {sum(len(d.page_content.split()) for d in retrieved)}")
   
   # Make sure prompt template includes {context}
   ```

2. **Is your prompt forcing the LLM to stay grounded?**
   ```
   ❌ BAD: "Answer the question: {question}"
   ✅ GOOD: "Answer ONLY using the context below. If the answer isn't 
            in the context, say 'I don't know'.
            
            Context:
            {context}
            
            Question: {question}"
   ```

3. **Are chunks overlapping too much?**
   ```
   Problem: Same information repeated in multiple chunks
   Result: LLM sees info multiple times, thinks it's authoritative
   
   Fix: Reduce overlap from 50% to 10-20%
   ```

4. **Token limit exceeded?**
   ```python
   # Count actual tokens, not just words
   from tiktoken import encoding_for_model
   
   enc = encoding_for_model("gpt-4")
   context_tokens = len(enc.encode(context))
   question_tokens = len(enc.encode(question))
   available = 4000  # leave room for response
   
   if context_tokens + question_tokens > available:
       # Context being silently truncated!
       # Solution: fewer retrieved chunks or smaller chunks
   ```

5. **Is your context actually relevant?**
   ```
   The retrieval might rank results highly but not actually answer the query.
   
   Measure: Retrieve top-5 docs, manually check:
   - Do they mention the query topic? (yes/no)
   - Do they actually answer the question? (yes/no)
   - If high precision but low recall: increase number of retrieved docs
   ```

**Debug checklist:**
- [ ] Context in prompt template?
- [ ] Prompt includes "only use context" instruction?
- [ ] Overlap reasonable (10-20%)?
- [ ] Not exceeding token limit?
- [ ] Retrieved docs manually verified as relevant?

---

## Problem: Slow Queries

**Symptom:** Each query takes 5+ seconds, but you expected milliseconds.

### Check these in order:

1. **Is the vector DB index actually built?**
   ```python
   # Qdrant
   collection_info = client.get_collection("my_collection")
   print(collection_info.points_count)
   print(collection_info.indexes)  # should show HNSW index
   
   # pgvector
   SELECT * FROM pg_indexes WHERE tablename = 'documents';
   # should show idx_embedding_hnsw or similar
   ```

2. **Are you batching embedding API calls?**
   ```python
   # ❌ SLOW: Embed one query at a time
   for doc in docs:
       embedding = openai_client.embeddings.create(
           model="text-embedding-3-small",
           input=doc
       )
   
   # ✅ FAST: Batch 50 documents
   embeddings = openai_client.embeddings.create(
       model="text-embedding-3-small",
       input=docs  # pass list
   )
   ```

3. **At what scale is this happening?**
   ```
   < 10K vectors:
   - Likely problem: no index or flat search
   - Solution: create index (Qdrant/pgvector adds index automatically)
   
   10K - 1M vectors:
   - Likely problem: HNSW not tuned
   - Solution: increase ef_construction parameter
   
   > 1M vectors:
   - Likely problem: wrong DB choice
   - Consider Milvus or Pinecone (distributed)
   ```

4. **Are you doing full-text search on every query?**
   ```python
   # ❌ SLOW: Full text search every time
   bm25_results = bm25.get_top_k(query, k=100)  # searches ALL docs
   
   # ✅ FAST: Use vector search to filter first
   dense_results = vector_db.search(query_vec, k=20)
   # Then re-rank with BM25 if needed
   ```

5. **Is your network the bottleneck?**
   ```python
   # Measure latency
   import time
   
   start = time.time()
   results = client.search(...)
   latency = time.time() - start
   
   # Break it down:
   # - Embedding query: ~100ms (API)
   # - Vector search: ~5-50ms (depends on DB)
   # - Reranking: ~100-500ms
   # - LLM generation: 1-5s
   
   If > 500ms on vector search alone → DB config issue
   ```

**Debug checklist:**
- [ ] Vector DB index created?
- [ ] Embedding API calls batched?
- [ ] Appropriate scale (10K vs 1M)?
- [ ] Not doing full-text search on query?
- [ ] Measured each component's latency?

---

## Problem: Cost Exploding

**Symptom:** Your embedding API bill is way higher than expected.

### Check these in order:

1. **Are you re-embedding unchanged documents?**
   ```python
   # ❌ EXPENSIVE: Re-embed every day
   for doc in docs:
       embedding = embed(doc)
   
   # ✅ CHEAP: Cache embeddings by content hash
   import hashlib
   
   doc_hash = hashlib.md5(doc.encode()).hexdigest()
   if doc_hash in cache:
       embedding = cache[doc_hash]
   else:
       embedding = embed(doc)
       cache[doc_hash] = embedding
   ```

2. **Are you querying too often without caching results?**
   ```python
   # ❌ EXPENSIVE: Every identical query embeds separately
   for user in users:
       results = rag.query("What is LangChain?")  # same query N times!
   
   # ✅ CHEAP: Cache query results
   query_cache = {}
   query_hash = hashlib.md5("What is LangChain?".encode()).hexdigest()
   if query_hash in query_cache:
       results = query_cache[query_hash]
   else:
       results = rag.query("What is LangChain?")
       query_cache[query_hash] = results
   ```

3. **Wrong embedding model for your budget?**
   ```
   Cost comparison (per 1M tokens):
   - text-embedding-3-small: $0.02 (fastest, cheapest)
   - text-embedding-3-large: $0.13 (slower, higher quality)
   - Cohere embed-v3: $0.10
   - All-MiniLM (self-hosted): ~$0 (only GPU cost)
   
   For prototyping: use small model or self-hosted
   For production: measure if quality improvement justifies 5-10x cost
   ```

4. **Chunk size bloat?**
   ```
   Cost is roughly proportional to chunk size:
   
   Chunk size: 300 tokens
   100K chunks = 30M tokens = $0.60 (with text-embedding-3-small)
   
   Chunk size: 2000 tokens
   100K chunks = 200M tokens = $4.00 (same data, 6.7x more expensive!)
   
   Audit: what's your median/max chunk size?
   ```

5. **Are you embedding queries that should be cached?**
   ```python
   # ❌ EXPENSIVE: Common queries re-embedded
   # User: "What is embeddings?" (common)
   # User: "How to tune chunking?" (common)
   # User: "What's RAG?" (common)
   
   # ✅ CHEAP: Pre-compute common queries
   common_queries = [
       "What is embeddings?",
       "How to use RAG?",
       ...
   ]
   common_embeddings = {q: embed(q) for q in common_queries}
   ```

**Debug checklist:**
- [ ] Caching embeddings by content hash?
- [ ] Caching query results?
- [ ] Right model for budget?
- [ ] Chunk sizes reasonable (<1000 tokens)?
- [ ] Common queries pre-computed?

---

## Problem: Embedding Model Changed, Now Everything Broken

**Symptom:** You switched embedding models and now similarity scores are all wrong.

### This is a critical gotcha. Here's why:

```
Model A (text-embedding-3-small):
doc1 = [0.123, 0.456, 0.789, ...]  (1536 dimensions)
doc2 = [0.111, 0.444, 0.777, ...]
similarity(doc1, doc2) = 0.95

Switch to Model B (all-MiniLM-L6-v2):
doc1 = [0.999, 0.111, 0.555]  (384 dimensions!)
doc2 = [0.888, 0.222, 0.444]
similarity(doc1, doc2) = 0.10  ❌ COMPLETELY DIFFERENT!

Why? Different dimensions, different learned representations, 
different scales. You can't mix them.
```

### Fix:

1. **Rebuild entire index with new model**
   ```python
   # 1. Load raw documents
   docs = load_documents()
   
   # 2. Split into chunks
   chunks = chunk_documents(docs)
   
   # 3. Embed with NEW model
   embeddings = [embed_with_new_model(chunk) for chunk in chunks]
   
   # 4. Clear old index
   vector_db.delete_collection("docs")
   
   # 5. Rebuild
   for chunk, emb in zip(chunks, embeddings):
       vector_db.add(chunk, emb)
   ```

2. **Version your embedding model**
   ```python
   # Save what model was used
   metadata = {
       "embedding_model": "text-embedding-3-small",
       "chunk_size": 500,
       "chunk_overlap": 50,
       "indexed_date": "2025-01-15"
   }
   
   # On query time, check:
   if query_metadata["embedding_model"] != index_metadata["embedding_model"]:
       raise ValueError("Embedding model mismatch! Rebuild index.")
   ```

3. **Plan model upgrades carefully**
   ```
   You want to try a new, better embedding model?
   
   Approach 1 (Risky): Switch immediately
   - ❌ Breaks entire index, requires rebuild
   
   Approach 2 (Safe): Run parallel
   - Index with both models for transition period
   - Gradually migrate queries to new model
   - Delete old index only after confidence is high
   ```

---

## Quick Diagnosis: "Everything is Broken"

If you're stuck and don't know where the problem is, run this checklist:

```python
# 1. Verify embedding model consistency
print("Indexing model:", index_metadata.embedding_model)
print("Query model:", query_metadata.embedding_model)
assert they match, else REBUILD

# 2. Test retrieval at basic level
test_query = "Hello world"
test_embedding = embed(test_query)
top_results = vector_db.search(test_embedding, k=5)
print(f"Found {len(top_results)} results")
print(f"Top similarity: {top_results[0].score}")
# If score is 0.99 on everything: vectors are pre-normalized and search is working
# If score is 0.50: normal, documents are diverse

# 3. Test with known answer
known_query = "Write a fact from your documents"
results = rag.query(known_query)
print(results)
# Does it appear in the results? If yes: retrieval works, prompt issue
# If no: retrieval broken, check items 1-2

# 4. Manually verify top retrieved chunk
top_chunk = results[0].page_content
print(top_chunk)
# Does it actually answer the query? If yes: retrieval good, generation bad
# If no: retrieval bad, tune chunk size or embedding model

# 5. Check token counts
from tiktoken import encoding_for_model
enc = encoding_for_model("gpt-4")
context_size = sum(len(enc.encode(r.page_content)) for r in results)
print(f"Context: {context_size} tokens")
# If > 3000: context might be truncated, reduce k or chunk size
```

---

## Common Mistakes Summary

| Mistake | Impact | How to Fix |
|---------|--------|-----------|
| Mixed embedding models | Complete retrieval failure | Rebuild index with one model |
| Chunks too large (>1500 tokens) | Noisy vectors, wrong results | Reduce chunk size to 500-800 |
| No index built | Very slow queries (>1 second) | Create HNSW/IVF index |
| Re-embedding unchanged docs | Wasted money | Add content-hash caching |
| Context token limit exceeded | LLM truncates context | Fewer chunks or smaller chunks |
| Bad prompt (no grounding instruction) | Hallucinations | Add "only use context" instruction |
| Query too ambiguous | Bad retrieval | Try query expansion or rephrase |
| Different chunking strategies mid-project | Inconsistent retrieval | Standardize on one strategy |

---

## Still Stuck?

1. **Isolate the problem:**
   - Is it embeddings? (test cosine similarity on known vectors)
   - Is it retrieval? (test vector DB directly)
   - Is it generation? (test LLM prompt separately)

2. **Measure each component:**
   ```python
   # Embedding quality: Does cosine similarity correlate with meaning?
   # Retrieval quality: Do top-K results actually answer the query?
   # Generation quality: Does LLM follow the prompt?
   ```

3. **Check logs and metrics:**
   - Vector DB latency
   - API error rates
   - Token usage
   - Cache hit rates

4. **Start simple:**
   - Test with 10 documents
   - Use simple queries with clear answers
   - Gradually increase complexity
   - Scale up only after verification

---

## Resources

- [RAG Evaluation Framework (RAGAS)](https://docs.ragas.io/)
- [LangChain Debugging Guide](https://python.langchain.com/docs/guides/debugging)
- [Vector DB Performance Tuning](https://qdrant.tech/documentation/concepts/configuration/)
