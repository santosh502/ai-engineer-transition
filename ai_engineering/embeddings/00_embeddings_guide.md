# Phase 2A: Embeddings, Chunking & Semantic Search

> Builds on: **Phase 1 – Vector Geometry**. Everything here is literally "Phase 1 ideas, but the vectors have 384–3072 dimensions instead of 2, and we use them to compare *meaning* instead of *position*."

## Learning Objectives

By the end of this phase, you will understand:
- What an embedding is and why we need one (geometry from Phase 1, extended to N dimensions)
- Cosine similarity as the "angle between meanings"
- Chunking strategy and why it makes or breaks retrieval quality
- How to build a semantic search engine from raw text, with zero frameworks
- How to choose and compare embedding models

---

# PART A - EMBEDDINGS & SEMANTIC SEARCH

## 1. What Is an Embedding?

**Definition**: An embedding is a function that maps a piece of data (word, sentence, image, audio) to a point in a high-dimensional vector space, such that **similar meaning → nearby points**.

```
"king"    → [0.21, -0.05, 0.88, ... ]   (e.g. 1536 numbers)
"queen"   → [0.19, -0.02, 0.91, ... ]
"banana"  → [-0.77, 0.65, 0.01, ... ]

Same idea as Phase 1's [3, 2] - just way more components.
Instead of (x, y) = (right, up), each dimension captures
some latent aspect of meaning (learned, not hand-labeled).
```

### The core promise
```
distance/angle in vector space  ≈  difference in meaning

  "king" and "queen"  → small angle between them (similar)
  "king" and "banana" → large angle between them (unrelated)
```

### Visual (2D simplification of a 1536-D space)
```
        ↑
   royal│      ● king
        │    ● queen
        │
        │
        │                    ● banana
        │                  ● apple
        └──────────────────────────→
                        food-ness

Real embeddings live in hundreds/thousands of dimensions -
this 2D picture is a teaching simplification (like PCA/t-SNE plots).

See: https://projector.tensorflow.org/ (interactive embedding visualization tool)
```

---

## 2. Why Are Embeddings Required?

| Problem with keyword search | How embeddings fix it |
|---|---|
| "car" doesn't match "automobile" | Both map to nearby vectors - synonyms are close |
| "Apple" (company) vs "apple" (fruit) confusion | Context-aware embeddings place them differently based on surrounding text |
| Can't search across languages | Multilingual embedding models map translations near each other |
| Can't compare images/text/audio directly | Any modality can be embedded into a shared or comparable vector space |
| Exact string match only | Embeddings capture *semantic* similarity, not just literal overlap |

**One-line answer:** computers can't natively compare "meaning" - but they're very good at comparing numbers. Embeddings convert meaning into numbers so geometry (Phase 1!) can do the comparing.

---

## 3. Best Way of Embedding (Practical Guidelines)

There's no single "best" embedding - it depends on trade-offs:

1. **Match the model to the task**
   - Short queries/documents → general-purpose text embedding models (e.g., `text-embedding-3-small/large`, Cohere `embed-v3`, open-source `bge`, `e5`, `gte`)
   - Code → code-specific embedding models
   - Multilingual data → multilingual models
2. **Normalize your vectors** (unit length) so cosine similarity and dot product become interchangeable - most modern models output pre-normalized (or near-normalized) vectors.
3. **Keep embedding + query-time model identical** - you can't mix vectors from two different models in the same index; the geometry won't mean the same thing.
4. **Batch your embedding calls** - far cheaper/faster than one-at-a-time.
5. **Cache embeddings** - re-embedding unchanged text wastes money and time.
6. **Right-size dimensionality** - higher dimensions ≠ always better; they cost more storage/compute for often-marginal quality gains (many providers now let you truncate via Matryoshka embeddings).

---

## 4. Dense Vectors

**Dense vector** = almost every dimension has a non-zero value (as opposed to a **sparse vector** like a bag-of-words, where most entries are 0).

```
Sparse (BM25/TF-IDF style):        Dense (embedding):
[0,0,0,3,0,0,0,0,1,0,0,...]        [0.21,-0.05,0.88,0.02,-0.11,...]
   ↑ mostly zeros                     ↑ almost all non-zero
   one dim per vocabulary word         each dim = learned latent feature
```

Dense vectors from neural embedding models capture *semantic* relationships; sparse vectors capture *literal token* relationships.

---

## 5. Cosine Similarity - The Geometry You Already Know

Recall from Phase 1: a vector has magnitude and direction. Cosine similarity measures **only the angle** between two vectors, ignoring their length.

### 5.1 Formula
```
                 v · w
cos(θ)  =  ─────────────
             ||v|| · ||w||

where:
  v · w   = dot product = v1w1 + v2w2 + ... + vnwn
  ||v||   = magnitude (length) of v = sqrt(v1² + v2² + ... + vn²)
```

### 5.2 Geometric meaning
```
cos(θ) =  1   → same direction        (identical meaning)
cos(θ) =  0   → perpendicular         (unrelated)
cos(θ) = -1   → opposite direction    (opposite meaning)

      w
      ↑
      |  θ (small angle → high similarity)
      | /
      |/____→ v
```

### 5.3 Worked Example (2D, using Phase 1 tools)
```
v = [3, 4]        w = [4, 3]

v · w      = 3·4 + 4·3 = 12 + 12 = 24
||v||      = sqrt(3² + 4²) = sqrt(25) = 5
||w||      = sqrt(4² + 3²) = sqrt(25) = 5

cos(θ) = 24 / (5 · 5) = 24/25 = 0.96   → very similar direction
```

### 5.4 Why cosine and not plain Euclidean distance?
Text embeddings often vary in magnitude for reasons unrelated to meaning (e.g. sentence length). Cosine similarity cares about *direction* only, which correlates better with semantic similarity than raw distance does. (If vectors are normalized to length 1, cosine similarity and Euclidean distance actually rank results identically - many vector DBs exploit this.)

**Visual reference:**
- https://en.wikipedia.org/wiki/Cosine_similarity#/media/File:Cosine_similarity.png (Wikipedia illustration)
- https://github.com/qdrant/qdrant/tree/master/examples (Qdrant has interactive examples)

---

## 6. Chunking - And Why Size/Overlap Matters

You can't embed a whole book as one vector and expect useful search - you need to split ("chunk") the text first.

### 6.1 Why chunk at all?
- Embedding models have a **max token limit** (context window)
- Smaller chunks → more precise retrieval (you get the *relevant paragraph*, not an entire chapter)
- Larger chunks → more context per result, but noisier/less precise vectors (averaging dilutes meaning)

### 6.2 The trade-off
```
Too small (e.g. 1 sentence)        Too large (e.g. 5 pages)
─────────────────────────────────────────────────────────────
+ Very precise matches              + Lots of context returned
- Loses surrounding context         - Vector "blurs" many topics together
- May retrieve fragments that       - Wastes LLM context window
  don't make sense alone            - Harder to pinpoint exact answer
```

### 6.3 Chunk overlap
```
Chunk 1: [....................]
Chunk 2:              [....................]
                       ^^^^^^^^
                    overlap region

Without overlap, a sentence that spans a chunk boundary gets
cut in half and neither chunk fully captures its meaning.
Typical overlap: 10-20% of chunk size.
```

### 6.4 Common chunking strategies
| Strategy | How it works | Best for |
|---|---|---|
| Fixed-size (tokens/characters) | Split every N tokens, with overlap | Simple, uniform docs |
| Sentence/paragraph-based | Split on natural boundaries | Preserves readability |
| Recursive character splitting | Try paragraph → sentence → word, in order | General-purpose (LangChain default) |
| Semantic chunking | Split where embedding similarity between adjacent sentences drops | Highest quality, more compute |
| Document-structure aware | Split by markdown headers/sections | Structured docs (like this file!) |

**Rule of thumb starting point:** 300–800 tokens per chunk, ~10–15% overlap - then tune based on retrieval quality.

---

## 7. Build: Embed a Book/Docs Folder From Scratch (No Framework)

### 7.1 Pipeline overview
```
docs folder
    │
    ▼
[1] Load & clean text files
    │
    ▼
[2] Chunk each document (Section 6)
    │
    ▼
[3] Call embedding model on each chunk → dense vector
    │
    ▼
[4] Store (vector, chunk_text, metadata) somewhere
    │
    ▼
[5] At query time: embed the query → compare to all stored vectors
    │
    ▼
[6] Return top-K most similar chunks
```

### 7.2 Manual cosine similarity in pure Python (no numpy, no framework)
```python
import math

def dot(v, w):
    return sum(a * b for a, b in zip(v, w))

def magnitude(v):
    return math.sqrt(sum(a * a for a in v))

def cosine_similarity(v, w):
    return dot(v, w) / (magnitude(v) * magnitude(w))

# Example
v = [3, 4]
w = [4, 3]
print(cosine_similarity(v, w))  # 0.96
```

### 7.3 Minimal from-scratch pipeline sketch
```python
import math

def chunk_text(text, chunk_size=500, overlap=75):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap  # step forward, keeping overlap
    return chunks

def embed(text):
    # placeholder: call your embedding API/model here
    # returns a list[float]
    ...

def cosine_similarity(v, w):
    dot = sum(a * b for a, b in zip(v, w))
    mag_v = math.sqrt(sum(a * a for a in v))
    mag_w = math.sqrt(sum(a * a for a in w))
    return dot / (mag_v * mag_w)

# Build the index
docs = ["...text of chapter 1...", "...text of chapter 2...", "..."]
index = []  # list of (chunk_text, vector)
for doc in docs:
    for chunk in chunk_text(doc):
        index.append((chunk, embed(chunk)))

# Query
def search(query, index, top_k=5):
    q_vec = embed(query)
    scored = [(cosine_similarity(q_vec, vec), text) for text, vec in index]
    scored.sort(reverse=True, key=lambda x: x[0])
    return scored[:top_k]
```

This is a full semantic search engine - just brute-force (compares the query against *every* stored vector). That brute-force comparison is exactly the bottleneck vector databases exist to solve (see the Vector Databases module).

### 7.4 When to Stop Building and Start Using APIs

You now understand cosine similarity, chunking, and retrieval. Next question: should you keep building, or start using pre-built models?

**Use free/open-source local embeddings when:**
- Prototyping or learning
- Dataset < 10K documents
- Latency-insensitive (queries can take 1+ second)
- Privacy-critical (don't want to send data to APIs)
- Budget-constrained (self-hosted cost is just GPU electricity)

**Use paid API embeddings (OpenAI, Cohere) when:**
- Production system, quality matters
- Dataset > 10K documents
- Latency requirements < 100ms
- You can afford API costs
- Want best-in-class model quality

**Cost example for 100M tokens/month:**
```
text-embedding-3-small (OpenAI):
  100M tokens × $0.02/1M = $2,000/month

all-MiniLM-L6-v2 (self-hosted on GPU):
  GPU cost: ~$1/month (batch embeddings efficiently)
  BUT: requires maintaining GPU infrastructure

Rule of thumb:
- < 10M tokens/month: self-host wins on cost
- > 100M tokens/month: API becomes comparable
- Quality-critical: API models win
```

**Practical path forward:**
1. Prototype locally with `all-MiniLM-L6-v2` (free, fast)
2. Test retrieval quality on your domain data
3. If quality acceptable → keep it, save money
4. If quality needs improvement → try `text-embedding-3-small`
5. Measure ROI: does better embedding quality justify 50x cost?

---

## 8. Add: Basic Vector Store (Local, No Framework)

A "vector store" at its simplest is just: a list of vectors + metadata + a similarity function + a sort.

```python
class SimpleVectorStore:
    def __init__(self):
        self.records = []  # each: {"id":, "vector":, "text":, "metadata":}

    def add(self, id, vector, text, metadata=None):
        self.records.append({
            "id": id, "vector": vector, "text": text,
            "metadata": metadata or {}
        })

    def search(self, query_vector, top_k=5, filter_fn=None):
        candidates = self.records
        if filter_fn:
            candidates = [r for r in candidates if filter_fn(r["metadata"])]
        scored = [
            (cosine_similarity(query_vector, r["vector"]), r)
            for r in candidates
        ]
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[:top_k]
```

This is O(n) per query - fine for thousands of chunks, too slow for millions. When you need to scale beyond this, move to the Vector Databases module.

---

## 9. Experiment: Comparing Embedding Models

| Model | Dimensions | Type | Speed | Quality | Cost |
|---|---|---|---|---|---|
| OpenAI `text-embedding-3-small` | 1536 (truncatable) | API | Fast | Good | Low |
| OpenAI `text-embedding-3-large` | 3072 (truncatable) | API | Medium | Best-in-class | Medium |
| Cohere `embed-v3` | 1024 | API | Fast | Very good, strong multilingual | Low-Medium |
| `bge-base/large` (BAAI) | 768/1024 | Open-source, self-hosted | Fast (local GPU/CPU) | Very good | Free (compute cost only) |
| `e5-base/large` | 768/1024 | Open-source | Fast | Very good | Free |
| `all-MiniLM-L6-v2` (sentence-transformers) | 384 | Open-source | Very fast | Decent | Free |

**What to actually test in your experiment:**
1. Retrieval quality: does the top result actually answer the query? (measure recall@k on a small labeled set)
2. Latency: milliseconds per embedding call, batch vs single
3. Cost: $ per million tokens (API models) vs GPU/CPU time (self-hosted)
4. Dimensionality trade-off: does truncating 3072→256 dims meaningfully hurt quality for your data?

**Rule of thumb:** small/local models (384–768 dim) are great for prototyping and cost-sensitive apps; large API models win when retrieval quality directly drives product value (e.g. legal/medical search).

---

## 10. Summary Tables

### Embeddings Core Concepts
| Concept | Meaning |
|---|---|
| Embedding | Text/image/audio → dense vector, similar meaning = nearby vectors |
| Dense vector | Most dimensions non-zero, learned latent features |
| Cosine similarity | Angle between vectors; ignores magnitude |
| Chunking | Splitting long text before embedding; balances precision vs. context |
| Overlap | Prevents meaning loss at chunk boundaries |

---

## 11. Practice Problems

1. Given `v = [1, 2, 2]` and `w = [2, 2, 1]`, compute cosine similarity by hand.
2. You have a 50-page PDF. Propose a chunk size + overlap, and justify it.
3. Explain why dense embeddings capture semantic meaning better than sparse vectors (like bag-of-words).
4. You're choosing between `text-embedding-3-small` ($0.02/1M tokens) and `bge-large` (self-hosted, $1/month GPU). You embed 100M tokens/month. Which is cheaper?

---

## 12. Key Takeaways

✓ **Embeddings** turn meaning into geometry - same Phase 1 vector math, way more dimensions

✓ **Cosine similarity** measures the angle between vectors - direction, not length

✓ **Chunking strategy** is often the single biggest lever on retrieval quality - bigger isn't always better

✓ **Build it by hand once** (manual cosine similarity, linear-scan store) before reaching for frameworks

✓ **No single best embedding model** - pick based on latency/quality/cost trade-offs and your domain

---

## 13. Recommended Next Steps

1. Implement Section 7's from-scratch pipeline on a real folder of docs/book chapters.
2. Manually compute cosine similarity for a few pairs before trusting library functions.
3. Experiment with 2-3 embedding models on your domain data (Section 9).
4. Benchmark chunking strategies: does 300 vs 500 vs 800 tokens change retrieval quality?
5. Move to **Vector Databases module** - learn how to scale this to millions of vectors with ANN algorithms.

---

## 14. Online Resources & Visualizations

### Interactive Tools
- **TensorFlow Embedding Projector**: https://projector.tensorflow.org/ - visualize high-dimensional embeddings in 2D/3D
- **Sentence Transformers**: https://www.sbert.net/ - guide to modern embedding models

### Benchmarks
- **MTEB Leaderboard**: https://huggingface.co/spaces/mteb/leaderboard - compare embedding model quality on your task

### Articles
- **Chunking Strategies** (LangChain): https://python.langchain.com/docs/modules/data_connection/document_loaders/
