# Retrieval-Augmented Generation (RAG)

**Materials**: [Overview](README.md) · [Study Guide](notes.md) · [Code Examples](implementation-examples.md) · [Quick Reference](quick-reference.md)

This directory contains comprehensive study materials for **Retrieval-Augmented Generation (RAG)**, a powerful technique that combines information retrieval with generative AI to build more accurate, grounded, and current LLM applications.

---

## What's Inside

### [notes.md](notes.md) — Comprehensive Study Guide

**Best for**: Understanding concepts and theory

- What is RAG and why it matters
- Core components: Retriever, Embeddings, Vector Stores, Generator
- Complete pipeline architecture with visual diagrams
- Document chunking strategies comparison
- Advanced techniques (reranking, hybrid retrieval, multi-hop)
- Key challenges and solutions
- Evaluation metrics
- When to use RAG (and when not to)
- Best practices checklist
- Learning resources

### [implementation-examples.md](implementation-examples.md) — Practical Code

**Best for**: Building and implementing RAG systems

- Simple RAG pipeline with LangChain
- Hybrid retrieval (dense + sparse)
- Reranking for better relevance
- Query expansion
- Metadata filtering
- Chunking strategies comparison
- Embedding visualization (t-SNE)
- Evaluation with RAGAS framework
- Configuration templates for different use cases

### [quick-reference.md](quick-reference.md) — Quick Lookup

**Best for**: Quick answers during development

- The 4 steps of RAG at a glance
- Embedding models comparison
- Vector database options
- Chunking decisions (quick guide)
- Similarity metrics
- Prompt engineering examples
- Common failure modes and fixes
- Configuration templates
- Metrics to track
- Common mistakes to avoid
- Decision tree for "Should I use RAG?"

---

## RAG at a Glance

**RAG Pipeline (4 Steps)**

```
Query → Encode → Retrieve → Augment → Generate → Answer
```

**Why RAG Matters**

> Ground answers in actual data (reduce hallucinations)  
> Keep information current (even if training data is old)  
> Work with specialized domain knowledge  
> Provide citations and sources  
> Handle large knowledge bases efficiently

---

## Quick Start

### Build a RAG System

1. Read [notes.md](notes.md) — "What is RAG?" section
2. Check [quick-reference.md](quick-reference.md) — "Quick Setup" section
3. Use code from [implementation-examples.md](implementation-examples.md) — "Simple RAG Pipeline"

### Understand RAG Deeply

1. Start with [notes.md](notes.md) — Read completely
2. Study [implementation-examples.md](implementation-examples.md) — Understand each example
3. Review [quick-reference.md](quick-reference.md) — Reinforce key points

---

## Core Components

### 1. Embeddings
- Text → Vector (768-1536 dimensions)
- Capture semantic meaning
- Enable similarity search

### 2. Chunking
- Split documents into manageable pieces
- Recommended: RecursiveCharacterTextSplitter
- Typical: 512-1024 tokens, 20% overlap

### 3. Vector Database
- Store and retrieve embeddings
- Options: Pinecone, Weaviate, Chroma, FAISS
- Enable semantic search

### 4. Retriever
- Finds relevant chunks for a query
- Can be dense (embedding-based) or sparse (keyword-based)
- Hybrid approach is more robust

### 5. Generator (LLM)
- Takes query + retrieved context
- Generates grounded response
- Prompt engineering matters

---

## Should I Use RAG?

### Use RAG When

- Knowledge base updates frequently
- Domain-specific information matters
- Need citations/sources (compliance)
- Large knowledge base
- Hallucinations are costly (medical, legal)

### Don't Use RAG When

- General knowledge questions
- Extremely low latency required (<100ms)
- Model already knows the answer
- Unreliable document quality
- Real-time data requirements impossible

---

## Best Practices

1. Use same embedding model everywhere
2. RecursiveCharacterTextSplitter is your default
3. Chunk size: 512-1024 tokens (adjust by use case)
4. Chunk overlap: 20% (50-200 tokens)
5. Hybrid retrieval (dense + sparse) beats either alone
6. Reranking improves results significantly
7. Separate metrics for retrieval vs generation
8. Test with real queries from your domain
9. Preserve metadata (source, date, version)
10. Version your knowledge base and configs

---

## Popular Frameworks

| Framework | Use Case | Learning Curve |
|-----------|----------|-----------------|
| **LangChain** | General RAG, full-featured | Medium |
| **LlamaIndex** | Data indexing & retrieval | Low |
| **Haystack** | Custom modular pipelines | Medium |
| **FastEmbed** | Lightweight embeddings | Low |

---

## Common Challenges & Solutions

| Challenge | Root Cause | Solution |
|-----------|-----------|----------|
| Wrong docs retrieved | Poor chunking or embedding | Hybrid search, reranking |
| Context too small | Low chunk size | Increase chunk size or overlap |
| Token overflow | Too many retrieved chunks | Reranking, compression |
| Slow queries | No indexing/caching | Add vector DB indexing |
| Hallucinations | Poor context | Better chunking, source attribution |

---

## Evaluation

**Retrieval Quality Metrics:**
- Recall@K — Did relevant docs appear?
- Precision@K — Were top-K relevant?
- NDCG — Is ranking good?

**Generation Quality Metrics:**
- Faithfulness — Does answer match context?
- Relevance — Does answer address question?
- Hallucination rate — How many made-up facts?

> Use **RAGAS Framework** for comprehensive RAG evaluation

---

## Getting Started

1. **Learn the theory** — Read [notes.md](notes.md)
2. **See code examples** — Study [implementation-examples.md](implementation-examples.md)
3. **Build something** — Start with simple pipeline
4. **Evaluate** — Use RAGAS framework
5. **Iterate** — Monitor metrics and improve

---

## External Resources

**Foundational**
- [NVIDIA RAG 101](https://developer.nvidia.com/blog/rag-101-demystifying-retrieval-augmented-generation-pipelines/)
- [IBM RAG Architecture](https://www.ibm.com/think/architectures/patterns/genai-rag)

**Implementation**
- [LangChain Documentation](https://python.langchain.com/)
- [LlamaIndex Guide](https://docs.llamaindex.ai/)

**Advanced**
- [Engineering the RAG Stack (arxiv)](https://arxiv.org/pdf/2601.05264)
- [Best Chunking Strategies 2026](https://www.firecrawl.dev/blog/best-chunking-strategies-rag)

**Evaluation**
- [RAGAS Framework](https://docs.ragas.io/)

---

## Quick Command Reference

**Extract embeddings and visualize:**
```bash
python -c "from sklearn.manifold import TSNE; import matplotlib.pyplot as plt; ..."
```

**Test chunking strategy:**
```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_text(text)
```

**Quick RAG setup:**
```python
from langchain.vectorstores import Chroma
db = Chroma.from_documents(chunks, embeddings)
retriever = db.as_retriever()
```

---

## Key Takeaways

1. **RAG = Smart Context** — Retrieve relevant info before generating
2. **Chunking is Critical** — How you split docs affects everything
3. **Embeddings + Vector DB** — Enable semantic search at scale
4. **Prompt Matters** — Good formatting improves answers
5. **Hybrid > Single** — Dense + sparse retrieval is more robust
6. **Evaluate Separately** — Check retrieval and generation independently
7. **Same Model Everywhere** — Use identical embedding model throughout
8. **Domain-Specific Wins** — RAG excels with specialized knowledge
