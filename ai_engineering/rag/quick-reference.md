# RAG Quick Reference Guide

> **RAG Materials** - [Overview](README.md) | [Study Guide](notes.md) | [Code Examples](implementation-examples.md) | [Quick Reference](quick-reference.md)

## At a Glance

**RAG = Retrieval + Augmented + Generation**

Takes a query → Finds relevant documents → Generates answer based on those documents

---

## The 4 Steps

| Step | What | How | Output |
|------|------|-----|--------|
| **1. Query Encoding** | Convert query to vector | Use embedding model | Query vector (e.g., 1536D) |
| **2. Retrieval** | Find similar docs | Vector DB similarity search | Top K relevant chunks |
| **3. Augmentation** | Combine context | Format chunks + query into prompt | Enriched prompt |
| **4. Generation** | Create answer | Send to LLM | Final answer |

---

## Embedding Models

```
Popular Options:
├─ OpenAI (text-embedding-3-small, text-embedding-3-large)
├─ Sentence Transformers (all-MiniLM-L6-v2)
├─ Cohere (embed-english-light-v3.0)
├─ Google (text-embedding-004)
└─ Open Source (BGE, MTEB models)

KEY: Same model for indexing AND retrieval!
```

---

## Vector Databases

```
Cloud Managed:
├─ Pinecone        (Easiest, serverless)
├─ Weaviate        (Open-source option)
├─ Azure Search    (Enterprise)
└─ AWS OpenSearch  (AWS ecosystem)

Local/Open-source:
├─ Chroma          (Lightweight, embedded)
├─ FAISS           (Facebook's fast search)
├─ Milvus          (Scalable)
└─ Qdrant          (Fast & scalable)
```

---

## Chunking Quick Decisions

**Ask yourself:**

1. **How factual is the content?**
   - Very factual (legal, medical) → Smaller chunks (256-512)
   - More narrative (blogs, reports) → Larger chunks (512-1024)

2. **What's your priority?**
   - Precision (correct answers) → Smaller chunks
   - Recall (find all relevant) → Larger chunks

3. **What's the format?**
   - Markdown/structured → Use MarkdownHeaderTextSplitter
   - Code/technical → Use code-aware separators
   - Plain text → Use RecursiveCharacterTextSplitter

**Default:** RecursiveCharacterTextSplitter with chunk_size=1000, overlap=200

---

## Similarity Metrics

```
Cosine Similarity:     Measures angle between vectors (0-1)
                       Higher = more similar
                       MOST COMMON for embeddings

Euclidean Distance:    Straight-line distance in high-D space
                       Lower = more similar

Dot Product:           Simple mathematical product
                       Higher = more similar
                       Faster but less stable
```

---

## Prompt Engineering for RAG

**Bad:**
```
User asks: "What is quantum computing?"
Prompt: "Answer this: {query}"
```

**Good:**
```
Prompt: """
Based on the following context, answer the question.
If you cannot answer from the context, say "I don't know".

CONTEXT:
{retrieved_chunks}

QUESTION: {query}

ANSWER:"""
```

**Better (with instructions):**
```
Prompt: """
You are a helpful assistant. Answer questions based ONLY on the provided context.
If the context doesn't contain the answer, explicitly say so.
Be concise and cite the source.

CONTEXT:
{retrieved_chunks}
[Source: {metadata}]

QUESTION: {query}

ANSWER:"""
```

---

## Common Failure Modes & Fixes

| Problem | Symptom | Fix |
|---------|---------|-----|
| Wrong docs retrieved | "I don't have info about that" | Use hybrid search, rerank, or rewrite chunks |
| Context too small | Missing important details | Increase chunk size or overlap |
| Context too large | Token limit exceeded | Use reranking, compression, or smaller K |
| Embedding mismatch | Retrieval fails silently | Use same model for index & query |
| Hallucinations | LLM makes up facts | Use stricter prompts, source attribution |
| Slow queries | Takes >1 second | Add indexing, caching, reduce K |
| Stale data | Old information returned | Refresh embeddings, version control |

---

## Quick Evaluation

**Check Retrieval Quality:**
```python
# Run query, inspect top results
results = retriever.get_relevant_documents("Your question")
for i, doc in enumerate(results[:3]):
    print(f"Result {i}: {doc.page_content[:200]}...")
    print(f"Relevant? Score: {relevance_score}")
```

**Check Generation Quality:**
```python
# Compare output to ground truth
actual = rag_chain("Question")
expected = "Ground truth answer"

# Manual assessment:
# - Accuracy: Does it answer correctly?
# - Faithfulness: Does it stay true to context?
# - Clarity: Is it easy to understand?
```

---

## Configuration Templates

### For Customer Support
```yaml
Embedding: sentence-transformers (small, fast)
Chunk Size: 256 tokens
Chunk Overlap: 20%
Retrieval: Hybrid (75% dense, 25% sparse)
Reranking: Yes (top 5 → top 3)
Top-K: 3
```

### For Research/Analysis
```yaml
Embedding: OpenAI text-embedding-3-large
Chunk Size: 1024 tokens
Chunk Overlap: 20%
Retrieval: Dense only
Reranking: Yes (top 10 → top 5)
Top-K: 5
```

### For Chat/Conversational
```yaml
Embedding: sentence-transformers (balanced)
Chunk Size: 512 tokens
Chunk Overlap: 20%
Retrieval: Hybrid (50/50)
Reranking: Optional
Top-K: 3-5
```

---

## Metrics to Track

### Retrieval Metrics
- **Recall@K**: % of relevant docs in top K
- **Precision@K**: % of top K that are relevant
- **MRR**: Position of first relevant result
- **NDCG**: Quality of ranking

### Generation Metrics
- **Faithfulness**: Answer matches context
- **Relevance**: Answer addresses question
- **Hallucination Rate**: % of made-up facts
- **Citation Accuracy**: Sources are correct

### System Metrics
- **Latency**: Query response time
- **Throughput**: Queries/second
- **Cost**: Per-query expense
- **Uptime**: System availability

---

## Decision Tree

```
START: Do I need RAG?
│
├─ Is my knowledge base current? (updated regularly)
│  └─ Yes → Consider RAG
│  └─ No  → LLM knowledge might be enough
│
├─ Do I need citations/sources?
│  └─ Yes → RAG required
│  └─ No  → Depends on other factors
│
├─ Is latency critical? (<100ms required)
│  └─ Yes → RAG might be too slow
│  └─ No  → RAG is feasible
│
└─ Domain-specific knowledge needed?
   └─ Yes → RAG strongly recommended
   └─ No  → Might not need RAG
```

---

## Common Mistakes to Avoid

❌ Using different embedding models for indexing vs querying  
❌ Storing raw documents without chunking  
❌ Chunk size too large (losing precision)  
❌ No overlap between chunks (lost context at boundaries)  
❌ Ignoring metadata (can't filter or cite)  
❌ Only using keyword search (misses semantic matches)  
❌ No reranking (relies on first retrieval)  
❌ Poor prompt engineering (LLM confused by context)  
❌ Not evaluating retrieval quality (optimizing wrong thing)  
❌ Forgetting to version knowledge base  

---

## Quick Setup (LangChain)

```python
# Minimal working RAG in 10 lines
from langchain.document_loaders import PDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.llms import ChatOpenAI

docs = PDFLoader("file.pdf").load()
chunks = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(docs)
db = Chroma.from_documents(chunks, OpenAIEmbeddings())
rag = RetrievalQA.from_chain_type(ChatOpenAI(), retriever=db.as_retriever())

# Query!
answer = rag("Your question?")
```

---

## Resources

- [NVIDIA RAG 101](https://developer.nvidia.com/blog/rag-101-demystifying-retrieval-augmented-generation-pipelines/)
- [LangChain RAG Docs](https://python.langchain.com/en/latest/)
- [LlamaIndex Guide](https://docs.llamaindex.ai/)
- [RAGAS Evaluation](https://docs.ragas.io/)

---


