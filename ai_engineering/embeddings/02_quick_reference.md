# Embeddings - Quick Reference

## One-Page Cheat Sheet

### Embedding Models at a Glance

| Need | Recommendation | Dimensions | Cost | Notes |
|------|---|---|---|---|
| **Fastest prototyping** | `all-MiniLM-L6-v2` | 384 | Free (self-hosted) | Sentence-Transformers, very fast, good enough |
| **Production semantic search** | OpenAI `text-embedding-3-small` | 1536 | Low API cost | Best price/quality tradeoff, reliable |
| **Best quality** | OpenAI `text-embedding-3-large` | 3072 | Medium API cost | State-of-the-art, use when quality > cost |
| **Multilingual** | Cohere `embed-v3` | 1024 | Low-Medium API cost | Strong cross-language, clean API |
| **Self-hosted at scale** | BAAI `bge-large` | 1024 | Free (GPU compute) | Very good, supports 10K+ token context |

---

### Cosine Similarity vs. Other Distances

| Distance Type | Formula | When to Use | Trade-off |
|---|---|---|---|
| **Cosine similarity** | `1 - cos(θ)` | Text embeddings (DEFAULT) | Direction only, ignores magnitude |
| **Euclidean (L2)** | `√((a-b)²)` | Image embeddings, normalized vectors | Considers magnitude, sensitive to outliers |
| **Manhattan (L1)** | `Σ\|a-b\|` | Sparse vectors, interpretability | Cheaper than L2, less smooth |
| **Dot product** | `a · b` | Pre-normalized vectors | Fastest on GPU, same ranking as cosine |

---

### Chunking Sizes (Quick Lookup)

| Document Type | Chunk Size | Overlap | Notes |
|---|---|---|---|
| Blog posts / articles | 300-600 tokens | 50-100 tokens | Preserve natural paragraphs |
| Technical documentation | 400-800 tokens | 100-150 tokens | Keep sections together |
| Code files | 200-400 tokens | 50-100 tokens | Respect function boundaries |
| Legal / medical docs | 500-1000 tokens | 100-200 tokens | Context critical |
| Books / long form | 600-1000 tokens | 150-200 tokens | Generous overlap for context |

**Token estimation:** ~1 token per 4 characters, or ~250 tokens per 100 words.

---

### API Quick Reference

**OpenAI Embeddings:**
```python
from openai import OpenAI
client = OpenAI()
response = client.embeddings.create(
    input="text to embed",
    model="text-embedding-3-small"
)
vector = response.data[0].embedding
```

**Cohere Embeddings:**
```python
import cohere
co = cohere.Client()
response = co.embed(texts=["text"], model="embed-english-v3.0")
vector = response.embeddings[0]
```

**Local (Sentence Transformers):**
```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")
vectors = model.encode(["text"])
```

---

### Common Mistakes to Avoid

| Mistake | Impact | Fix |
|---|---|---|
| **Using different embedding models for index + query** | Breaks all ranking | Keep model identical |
| **Chunks too large (>1000 tokens)** | Noisy vectors, poor precision | Split at 300-800 tokens |
| **No overlap between chunks** | Lost meaning at boundaries | Add 10-20% overlap |
| **Forgetting to normalize embeddings** | Wrong similarity scores | Call `.normalize()` or check model docs |
| **Only semantic search, no keyword** | Misses acronyms, exact terms | Move to Vector Databases module for hybrid search |
| **Testing on tiny datasets only** | Doesn't scale to production | Profile at 1K, 10K, 100K chunks |

---

### Performance Tuning Checklist

- [ ] Chunk size: tested 300-800 tokens, picked one, measured recall@5
- [ ] Embedding model: compared 2-3 models on your domain, picked winner
- [ ] Batch embedding: if using API, batch requests (50-100 at a time)
- [ ] Caching: checked if re-embedding same texts (cache vectors)
- [ ] Dimensionality: tested truncation (if supported) to reduce storage

---

### Typical Costs (2024)

| Provider | Model | Cost | Per Million Tokens |
|---|---|---|---|
| OpenAI | text-embedding-3-small | $0.02 | ~400K tokens |
| OpenAI | text-embedding-3-large | $0.13 | ~65K tokens |
| Cohere | embed-v3 | $0.10 | ~600K tokens |
| Self-hosted (GPU) | Local cost only | ~$1/month (cloud GPU) | Varies by hardware |

**Rule:** For <10M tokens/month, API is cheaper. Beyond that, self-hosted wins.

---

### Debug: Why Are My Embeddings Wrong?

1. **Check vector dimensions**: all vectors same size?
   ```python
   assert all(len(v) == 1536 for v in vectors)
   ```

2. **Verify magnitude**: should be ~1.0 if normalized
   ```python
   import numpy as np
   mag = np.linalg.norm(vectors, axis=1)
   assert all(0.99 < m < 1.01 for m in mag)  # If pre-normalized
   ```

3. **Compare similarity scores**: similar texts should be close
   ```python
   sim = cosine_similarity("the king", "the queen")
   sim2 = cosine_similarity("the king", "banana")
   assert sim > sim2
   ```

4. **Check if model changed**: did you switch models?
   ```python
   index_model = "text-embedding-3-small"  # ← save this!
   query_model = "text-embedding-3-small"  # must match
   ```

---

### Timeline: How Long to Learn This?

| Topic | Time | Resources |
|---|---|---|
| Manual cosine similarity (hand, then code) | 30 min | Section 5, Example 1 |
| Text chunking & naive vector store | 1-2 hours | Sections 6-8, Examples 2-3 |
| First API embedding call | 15 min | Example 4, OpenAI/Cohere docs |
| **Embeddings fundamentals** | 1 week | Understand concepts + build project |

---

### Resources to Bookmark

- **Interactive:** https://projector.tensorflow.org/ (visualize embeddings in 2D)
- **Benchmarks:** https://huggingface.co/spaces/mteb/leaderboard (model comparison)
- **Docs:** https://www.sbert.net/ (Sentence Transformers guide)

---

### One Example: End-to-End

```python
# 1. Chunk a document
text = open("chapter_1.txt").read()
chunks = [text[i:i+500] for i in range(0, len(text), 400)]

# 2. Embed each chunk
from openai import OpenAI
client = OpenAI()
embeddings = []
for chunk in chunks:
    resp = client.embeddings.create(input=chunk, model="text-embedding-3-small")
    embeddings.append(resp.data[0].embedding)

# 3. Store in simple vector store
class VectorStore:
    def __init__(self):
        self.records = []
    
    def add(self, vec, text):
        self.records.append({"vector": vec, "text": text})
    
    def cosine(self, v, w):
        import math
        dot = sum(a*b for a,b in zip(v, w))
        mag_v = math.sqrt(sum(a*a for a in v))
        mag_w = math.sqrt(sum(a*a for a in w))
        return dot / (mag_v * mag_w) if mag_v and mag_w else 0
    
    def search(self, query_emb, top_k=3):
        scores = [(self.cosine(query_emb, r["vector"]), r["text"]) for r in self.records]
        return sorted(scores, reverse=True)[:top_k]

store = VectorStore()
for chunk, emb in zip(chunks, embeddings):
    store.add(emb, chunk)

# 4. Search
query = "What is the main character's motivation?"
query_emb = client.embeddings.create(input=query, model="text-embedding-3-small").data[0].embedding
results = store.search(query_emb, top_k=3)

for sim, text in results:
    print(f"Score: {sim:.4f}, Text: {text[:60]}...")
```

Done! You've embedded and searched a document.

---

### Next: Vector Databases

When you're ready to:
- Scale beyond 10K chunks
- Add metadata filtering
- Combine keyword + semantic search
- Get sub-100ms queries

Move to the **Vector Databases** module.
