# Practical Code Examples: Vector Databases

This file contains runnable examples for vector database concepts.

---

## Example 5: pgvector Setup (SQL)

```sql
-- Enable the extension (run once per database)
CREATE EXTENSION IF NOT EXISTS vector;

-- Create a table with vector column
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    content TEXT,
    embedding VECTOR(1536),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create an HNSW index for fast similarity search
CREATE INDEX idx_embedding_hnsw ON documents USING hnsw (embedding vector_cosine_ops);

-- Insert sample data
INSERT INTO documents (title, content, embedding, metadata) VALUES
    ('Kings and Queens', 'Information about royal families', 
     ARRAY[0.21, -0.05, 0.88, ...], '{"category": "royalty", "source": "wiki"}'),
    ('Fruits of the World', 'Guide to exotic fruits',
     ARRAY[-0.77, 0.65, 0.01, ...], '{"category": "food", "source": "cookbook"}');

-- Query: Find top 5 most similar documents to a query vector
SELECT 
    id, title, 
    1 - (embedding <=> $1::vector) AS similarity_score,
    metadata->>'category' AS category
FROM documents
WHERE metadata->>'category' = 'royalty'  -- Filter by metadata
ORDER BY embedding <=> $1::vector         -- Order by distance
LIMIT 5;

-- Note: <=> is pgvector's cosine distance operator
-- 1 - distance = similarity (since we want high similarity = high score)
```

---

## Example 6: Qdrant Python Setup

```python
from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams, Distance, PointStruct,
    Filter, FieldCondition, MatchValue
)

# Connect to Qdrant (local or remote)
client = QdrantClient("http://localhost:6333")

# Create a collection
client.create_collection(
    collection_name="documents",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
)

# Add vectors with metadata
client.upsert(
    collection_name="documents",
    points=[
        PointStruct(
            id=1,
            vector=[0.21, -0.05, 0.88, ...],  # Your embedding
            payload={
                "title": "Kings and Queens",
                "content": "Information about royal families",
                "category": "royalty",
                "source": "wiki"
            }
        ),
        PointStruct(
            id=2,
            vector=[-0.77, 0.65, 0.01, ...],
            payload={
                "title": "Fruits of the World",
                "content": "Guide to exotic fruits",
                "category": "food",
                "source": "cookbook"
            }
        ),
    ],
)

# Search with filter
results = client.search(
    collection_name="documents",
    query_vector=[0.20, -0.03, 0.90, ...],  # Query embedding
    query_filter=Filter(
        must=[
            FieldCondition(key="category", match=MatchValue(value="royalty"))
        ]
    ),
    limit=5,
    with_payload=True,  # Return metadata
)

# Process results
for result in results:
    print(f"ID: {result.id}")
    print(f"Similarity: {result.score:.4f}")
    print(f"Payload: {result.payload}")
```

---

## Example 7: Docker Quick Start (Qdrant)

```bash
# Start Qdrant in Docker
docker run -p 6333:6333 qdrant/qdrant

# Verify it's running
curl http://localhost:6333/health

# Stop it
docker stop <container_id>
```

---

## Example 8: Reciprocal Rank Fusion (Hybrid Search)

```python
def reciprocal_rank_fusion(rank_lists, k=60):
    """
    Combine multiple ranked lists (e.g., semantic + keyword search results).
    Each list is a sequence of (doc_id, score) tuples.
    """
    scores = {}
    for ranked_list in rank_lists:
        for rank, (doc_id, _) in enumerate(ranked_list):
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1)
    
    # Sort by RRF score descending
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)

# Example: combining semantic search and keyword (BM25) results
semantic_results = [
    ("doc_1", 0.95),  # high semantic similarity
    ("doc_2", 0.80),
    ("doc_3", 0.70),
]

keyword_results = [
    ("doc_3", 0.85),  # high keyword match
    ("doc_1", 0.60),
    ("doc_4", 0.75),
]

hybrid = reciprocal_rank_fusion([semantic_results, keyword_results], k=60)
print("Hybrid results (RRF combined):")
for doc_id, rrf_score in hybrid:
    print(f"  {doc_id}: {rrf_score:.4f}")
# Output: doc_1 and doc_3 ranked higher (present in both lists)
```

---

## Example 9: BM25 Scoring

```python
import math
from collections import defaultdict

class BM25:
    """Simplified BM25 scorer."""
    
    def __init__(self, documents, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.documents = documents
        self.avgdl = sum(len(doc.split()) for doc in documents) / len(documents)
        self.idf = self._compute_idf()
    
    def _compute_idf(self):
        """Compute IDF for each term."""
        idf = defaultdict(float)
        for doc in self.documents:
            for term in set(doc.split()):
                idf[term] += 1
        
        idf_dict = {}
        for term, count in idf.items():
            idf_dict[term] = math.log(len(self.documents) - count + 0.5) / \
                           (count + 0.5)
        return idf_dict
    
    def score(self, query, doc_idx):
        """Score a document for a query."""
        doc = self.documents[doc_idx]
        score = 0
        doc_len = len(doc.split())
        
        for term in query.split():
            if term not in self.idf:
                continue
            
            # Term frequency in document
            tf = doc.split().count(term)
            
            # BM25 formula
            idf = self.idf[term]
            numerator = idf * tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avgdl)
            score += numerator / denominator
        
        return score

# Example
docs = [
    "the king of england",
    "the queen of england",
    "apple pie recipe",
    "banana bread baking",
]

bm25 = BM25(docs)
query = "king queen"

print("BM25 scores for query 'king queen':")
for i, doc in enumerate(docs):
    score = bm25.score(query, i)
    print(f"  Doc {i}: {score:.4f} - {doc}")
# Output: docs 0 and 1 (king/queen) score highest
```

---

## Integration Example: Complete Pipeline with Real Vector DB

```python
import math
import random
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

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

# Step 3: Setup Qdrant (local in-memory for demo)
client = QdrantClient(":memory:")
client.create_collection(
    collection_name="docs",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE),
)

# Step 4: Index documents
documents = [
    "The king and queen ruled the kingdom with wisdom and justice.",
    "Apple pie is a delicious dessert made with fresh apples and cinnamon.",
    "Banana bread is a popular baked good enjoyed worldwide.",
]

chunk_id = 0
for doc_id, doc in enumerate(documents):
    for chunk in chunk_text(doc):
        client.upsert(
            collection_name="docs",
            points=[
                PointStruct(
                    id=chunk_id,
                    vector=embed(chunk),
                    payload={"text": chunk, "doc_id": doc_id}
                )
            ],
        )
        chunk_id += 1

# Step 5: Search
query = "royal families"
query_emb = embed(query)
results = client.search(
    collection_name="docs",
    query_vector=query_emb,
    limit=3,
    with_payload=True,
)

print("Search results for 'royal families':")
for result in results:
    print(f"  Similarity: {result.score:.4f}")
    print(f"  Text: {result.payload['text'][:60]}...")
```

---

## Useful Libraries (No Framework Needed)

```python
# For vector databases
from qdrant_client import QdrantClient  # Qdrant
import psycopg2  # Postgres (for pgvector)

# For search/ranking
from rank_bm25 import BM25Okapi  # BM25 implementation
import faiss  # Meta's vector search library

# For benchmarking
import time
import numpy as np
```

---

## Debugging & Profiling

```python
import time
import numpy as np

def profile_search(client, query_vector, collection_name, num_iterations=100):
    """Profile search latency."""
    start = time.time()
    for _ in range(num_iterations):
        client.search(collection_name, query_vector, limit=5)
    elapsed = time.time() - start
    print(f"Average latency: {elapsed / num_iterations * 1000:.2f}ms")

def validate_vectors(vectors):
    """Check vector quality."""
    v = np.array(vectors)
    print(f"Shape: {v.shape}")
    print(f"Magnitude: {np.linalg.norm(v, axis=1)}")
    print(f"Min/max values: {v.min():.4f} / {v.max():.4f}")

def benchmark_at_scale(client, collection_name, sizes=[1000, 10000, 100000]):
    """Benchmark latency at different scales."""
    for size in sizes:
        query_vector = [random.gauss(0, 0.1) for _ in range(384)]
        start = time.time()
        for _ in range(100):
            client.search(collection_name, query_vector, limit=5)
        elapsed = time.time() - start
        print(f"{size:,} vectors: {elapsed / 100 * 1000:.2f}ms avg latency")
```

---

## Comparing pgvector vs. Qdrant

Both are excellent choices. Here's a quick comparison in code:

### pgvector (if using Postgres)
```python
import psycopg2

conn = psycopg2.connect("dbname=mydb user=postgres")
cursor = conn.cursor()

# Insert vectors
cursor.execute("""
    INSERT INTO documents (title, embedding, metadata)
    VALUES (%s, %s::vector, %s)
""", ("My Title", "[0.1, 0.2, ...]", {"key": "value"}))

# Search
cursor.execute("""
    SELECT title, 1 - (embedding <=> %s::vector) as sim
    FROM documents
    ORDER BY embedding <=> %s::vector
    LIMIT 5
""", ("[0.1, 0.2, ...]", "[0.1, 0.2, ...]"))
```

### Qdrant (dedicated vector DB)
```python
from qdrant_client import QdrantClient

client = QdrantClient("http://localhost:6333")

# Insert vectors
client.upsert("collection", [PointStruct(...)])

# Search
results = client.search("collection", query_vector, limit=5)
```

Qdrant is easier for vector-focused work; pgvector is better if you need to join vectors with other SQL data.

---

## Next Steps

1. **Choose pgvector or Qdrant** (see quick reference)
2. **Set up locally** (Example 5 or 6)
3. **Run the integration example** on your documents
4. **Add metadata filtering** to your queries
5. **Implement hybrid search** (Example 8) combining semantic + BM25
6. **Profile latency** at 1K, 10K, 100K vectors
7. **Move to Phase 4: RAG** - using these vectors in an LLM pipeline
