# Practical Code Examples: Embeddings & Semantic Search

This file contains runnable, minimal code examples for embeddings concepts.

---

## Example 1: Manual Cosine Similarity (Pure Python)

```python
import math

def cosine_similarity(v, w):
    """Compute cosine similarity between two vectors."""
    dot = sum(a * b for a, b in zip(v, w))
    mag_v = math.sqrt(sum(a * a for a in v))
    mag_w = math.sqrt(sum(a * a for a in w))
    if mag_v == 0 or mag_w == 0:
        return 0
    return dot / (mag_v * mag_w)

# Test
v = [3, 4]
w = [4, 3]
print(f"Cosine similarity: {cosine_similarity(v, w):.4f}")  # 0.96

# More realistic example
king = [0.21, -0.05, 0.88, 0.11, -0.02]
queen = [0.19, -0.02, 0.91, 0.09, -0.01]
banana = [-0.77, 0.65, 0.01, -0.50, 0.23]

print(f"king vs queen: {cosine_similarity(king, queen):.4f}")   # high (similar)
print(f"king vs banana: {cosine_similarity(king, banana):.4f}") # low (different)
```

---

## Example 2: Text Chunking

```python
def chunk_text_fixed_size(text, chunk_size=300, overlap=50):
    """Chunk text by character count with overlap."""
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start = end - overlap
        if start >= len(text):
            break
    return chunks

def chunk_text_by_sentences(text, chunk_size=3):
    """Chunk text by grouping sentences."""
    import re
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    for i in range(0, len(sentences), chunk_size):
        chunk = ' '.join(sentences[i:i+chunk_size])
        chunks.append(chunk)
    return chunks

# Example
text = """The quick brown fox jumps over the lazy dog. 
This is the second sentence. Here's a third one. 
And here is the fourth sentence for testing."""

print("Fixed-size chunks:")
for i, chunk in enumerate(chunk_text_fixed_size(text, chunk_size=50, overlap=10)):
    print(f"  [{i}] {chunk[:40]}...")

print("\nSentence-based chunks:")
for i, chunk in enumerate(chunk_text_by_sentences(text, chunk_size=2)):
    print(f"  [{i}] {chunk[:60]}...")
```

---

## Example 3: Simple Vector Store (No Framework)

```python
import math

class SimpleVectorStore:
    """A minimal in-memory vector store for semantic search."""
    
    def __init__(self):
        self.records = []
    
    def add(self, id, vector, text, metadata=None):
        """Add a vector + text to the store."""
        self.records.append({
            "id": id,
            "vector": vector,
            "text": text,
            "metadata": metadata or {}
        })
    
    def cosine_similarity(self, v, w):
        """Compute cosine similarity."""
        dot = sum(a * b for a, b in zip(v, w))
        mag_v = math.sqrt(sum(a * a for a in v))
        mag_w = math.sqrt(sum(a * a for a in w))
        if mag_v == 0 or mag_w == 0:
            return 0
        return dot / (mag_v * mag_w)
    
    def search(self, query_vector, top_k=3, filter_fn=None):
        """Search for top-K most similar vectors."""
        candidates = self.records
        if filter_fn:
            candidates = [r for r in candidates if filter_fn(r["metadata"])]
        
        scores = [
            (self.cosine_similarity(query_vector, r["vector"]), r)
            for r in candidates
        ]
        scores.sort(key=lambda x: x[0], reverse=True)
        return scores[:top_k]

# Example usage
store = SimpleVectorStore()
store.add(1, [0.21, -0.05, 0.88], "king", {"category": "royalty"})
store.add(2, [0.19, -0.02, 0.91], "queen", {"category": "royalty"})
store.add(3, [-0.77, 0.65, 0.01], "banana", {"category": "food"})
store.add(4, [-0.75, 0.68, 0.02], "apple", {"category": "food"})

query = [0.20, -0.03, 0.90]  # Close to "king" and "queen"
results = store.search(query, top_k=2)

print("Search results:")
for sim, record in results:
    print(f"  {record['text']} (sim: {sim:.4f})")

# With metadata filter
print("\nFiltered search (royalty only):")
royalty_results = store.search(query, top_k=2, filter_fn=lambda m: m.get("category") == "royalty")
for sim, record in royalty_results:
    print(f"  {record['text']} (sim: {sim:.4f})")
```

---

## Example 4: Mock Embedding API (Placeholder)

```python
import random

def mock_embed(text, model="text-embedding-3-small", dim=384):
    """
    Mock embedding function for testing.
    In practice, call OpenAI, Cohere, or local model here.
    """
    random.seed(hash(text) % 2**32)  # Deterministic for same input
    return [random.gauss(0, 0.1) for _ in range(dim)]

# Real API examples (commented):
# from openai import OpenAI
# client = OpenAI()
# response = client.embeddings.create(input="text", model="text-embedding-3-small")
# vector = response.data[0].embedding

# From Cohere:
# import cohere
# co = cohere.Client()
# response = co.embed(texts=["text"], model="embed-english-v3.0", input_type="search_document")
# vector = response.embeddings[0]

# From sentence-transformers:
# from sentence_transformers import SentenceTransformer
# model = SentenceTransformer("all-MiniLM-L6-v2")
# vectors = model.encode(["text"])

print("Embedding test:")
e1 = mock_embed("hello world")
print(f"hello world: {e1[:5]}... (length: {len(e1)})")
```

---

## Integration Example: Complete Semantic Search Pipeline

```python
import math
import random

# Step 1: Mock embedding function
def embed(text, dim=384):
    random.seed(hash(text) % 2**32)
    return [random.gauss(0, 0.1) for _ in range(dim)]

# Step 2: Chunk text
def chunk_text(text, chunk_size=100):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(' '.join(words[i:i+chunk_size]))
    return chunks

# Step 3: Simple vector store
class VectorStore:
    def __init__(self):
        self.records = []
    
    def add(self, id, vector, text):
        self.records.append({"id": id, "vector": vector, "text": text})
    
    def cosine(self, v, w):
        dot = sum(a * b for a, b in zip(v, w))
        mag_v = math.sqrt(sum(a * a for a in v))
        mag_w = math.sqrt(sum(a * a for a in w))
        return dot / (mag_v * mag_w) if mag_v and mag_w else 0
    
    def search(self, query, top_k=3):
        q_vec = embed(query)
        scores = [(self.cosine(q_vec, r["vector"]), r["text"]) 
                  for r in self.records]
        return sorted(scores, reverse=True)[:top_k]

# Run the pipeline
documents = [
    "The king and queen ruled the kingdom with wisdom.",
    "Apple pie is a delicious dessert made with fresh apples.",
    "Banana bread is a popular baked good enjoyed worldwide.",
]

store = VectorStore()
for doc_id, doc in enumerate(documents):
    for chunk_id, chunk in enumerate(chunk_text(doc)):
        store.add(f"{doc_id}_{chunk_id}", embed(chunk), chunk)

# Query
query = "royal families"
results = store.search(query, top_k=2)

print("Search results for 'royal families':")
for sim, text in results:
    print(f"  Similarity: {sim:.4f}")
    print(f"  Text: {text[:60]}...")
```

---

## Useful Libraries (No Framework Needed)

```python
# For embeddings
from openai import OpenAI  # OpenAI API
import cohere  # Cohere API
from sentence_transformers import SentenceTransformer  # Local models

# For text processing
import re  # Regex for sentence splitting
from nltk.tokenize import sent_tokenize  # Better sentence splitting
```

---

## Debugging & Profiling

```python
import time
import numpy as np

def profile_search(store, query, num_iterations=100):
    """Profile search latency."""
    start = time.time()
    for _ in range(num_iterations):
        store.search(query, top_k=5)
    elapsed = time.time() - start
    print(f"Average latency: {elapsed / num_iterations * 1000:.2f}ms")

def validate_vectors(vectors):
    """Check vector quality."""
    v = np.array(vectors)
    print(f"Shape: {v.shape}")
    print(f"Magnitude: {np.linalg.norm(v, axis=1)}")
    print(f"Min/max values: {v.min():.4f} / {v.max():.4f}")
```

---

## Next Steps

1. **Try Example 1–3** on your own documents
2. **Compare embedding models** (Example 4) using the OpenAI/Cohere APIs
3. **Benchmark chunking strategies** with Example 2: does 300 vs 500 tokens change results?
4. **Move to Vector Databases module** when you're ready to scale beyond 10K vectors
