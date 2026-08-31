# RAG Study Guide

**Navigation**: [Overview](README.md) · [Study Guide](notes.md) · [Code Examples](implementation-examples.md) · [Quick Reference](quick-reference.md)

Comprehensive study notes for Retrieval-Augmented Generation.

## What is RAG?

RAG is a technique that combines information retrieval with generative AI. It allows LLMs to retrieve relevant external documents/data before generating responses, enabling the model to:
- Ground answers in actual data
- Reduce hallucinations
- Stay current with updated information
- Work with specialized domain knowledge

---

## RAG Pipeline Architecture

### Visual Overview
The RAG pipeline follows a 4-step process:

```
┌─────────────┐
│   Query     │
└──────┬──────┘
       │
       ▼
┌──────────────────────┐
│  1. Query Encoding   │ (Convert query to vector embedding)
└──────┬───────────────┘
       │
       ▼
┌──────────────────────────────────┐
│  2. Document Retrieval           │ (Search vector store for similar chunks)
└──────┬───────────────────────────┘
       │
       ▼
┌──────────────────────────────────┐
│  3. Context Augmentation         │ (Combine retrieved docs with query)
└──────┬───────────────────────────┘
       │
       ▼
┌──────────────────────────────────┐
│  4. Answer Generation by LLM     │ (Generate response based on context)
└──────┬───────────────────────────┘
       │
       ▼
    Answer (grounded in documents)
```

**Reference:** [RAG 101: Demystifying Retrieval-Augmented Generation Pipelines](https://developer.nvidia.com/blog/rag-101-demystifying-retrieval-augmented-generation-pipelines/)

---

## Core Components

### 1. **Retriever**
- Finds relevant documents/chunks from a knowledge base
- Uses **embedding models** to convert text to vector representations
- Types:
  - **Dense retrieval**: Uses embeddings (semantic/similarity search)
  - **Sparse retrieval**: BM25, keyword-based search
  - **Hybrid**: Combination of both for robustness

### 2. **Vector Embeddings & Similarity Search**

Embeddings are numerical representations of text captured in high-dimensional space (typically 768-1536 dimensions).

**Key Concepts:**
- Same embedding model must be used for both indexing and retrieval
- Similarity measured using **cosine similarity** - how closely vectors align in space
- You can visualize embeddings using **t-SNE** or **PCA** to reduce to 2D/3D space

**Visualization Tools:**
- **t-SNE**: Reduces high-dimensional embeddings to 2D for visualization
- **PCA (Principal Component Analysis)**: Extracts components with greatest variance
- **FAISS (Facebook AI Similarity Search)**: Efficient vector indexing for retrieval

**Reference:** [Visualize Vector Embeddings in a RAG System](https://medium.com/@sarmadafzalj/visualize-vector-embeddings-in-a-rag-system-89d0c44a3be4) · [Text Embeddings and Vector Search](https://www.btelligent.com/en/blog/text-embeddings-vector-search)

### 3. **Knowledge Base / Vector Store**
- Repository of documents/data to retrieve from
- Documents are chunked and converted to embeddings (offline process)
- Popular tools:
  - **Pinecone**: Managed vector database
  - **Weaviate**: Open-source vector search engine
  - **Chroma**: Lightweight embedding database
  - **FAISS**: Facebook's similarity search library
  - **Milvus**: Open-source vector database
  - **Azure Cognitive Search**: Cloud-based solution

### 4. **Document Chunking Strategy** ⭐ Critical Component

How you split documents directly impacts retrieval quality:

**Recommended Chunk Sizes:**
- **256-512 tokens**: For fact-focused retrieval (better precision)
- **512-1,024 tokens**: For context-heavy tasks (better meaning preservation)
- **Overlap**: 10-20% overlap recommended (50-100 tokens for 500-token chunk)

**Chunking Methods:**

| Strategy · Best For · Pros · Cons |
|----------|----------|------|------|
| **Fixed-size** · General documents · Simple, predictable · Splits sentences, loses context |
| **Sentence-based** · Structured text · Preserves sentences · May be too small or large |
| **Paragraph-based** · Reports, papers · Natural boundaries · Varying sizes |
| **Recursive** (Recommended) · Most use cases · Balances efficiency & context · Slightly complex |
| **Semantic** · Unstructured data · Groups by meaning · Computationally expensive |
| **Overlapping** · Technical content · Preserves context flow · More storage overhead |

**Best Practice:**
- Use **RecursiveCharacterTextSplitter** as default (hierarchy of natural separators)
- For structured docs (reports, papers): Use paragraph-based or recursive chunking
- For unstructured docs (notes, social media): Use semantic or embedding-based chunking
- Always preserve metadata: title, author, URL, timestamp, page numbers

**Reference:** [13 RAG chunking strategies for better retrieval](https://www.meilisearch.com/blog/rag-chunking-strategies) · [RAG Document Chunking: 6 Best Practices](https://airbyte.com/agentic-data/ag-document-chunking-best-practices) · [11 Chunking Strategies for RAG — Simplified & Visualized](https://masteringllm.medium.com/11-chunking-strategies-for-rag-simplified-visualized-df0dbec8e373)

### 5. **Generator (LLM)**
- Takes retrieved context + original query
- Generates response based on both inputs
- **Prompt engineering** is crucial: how you format retrieved context affects output quality
- Must work within token limits (balance between context and generation space)

---

## Two-Phase Processing

### Phase 1: Offline Indexing Pipeline
```
Documents
    ↓
Split into Chunks
    ↓
Generate Embeddings (using embedding model)
    ↓
Store in Vector Database
```
This happens once, offline.

### Phase 2: Online Query Pipeline
```
User Query
    ↓
Encode Query (same embedding model)
    ↓
Vector Similarity Search
    ↓
Retrieve Top-K Relevant Chunks
    ↓
Rank/Rerank Results
    ↓
Format into Prompt
    ↓
Send to LLM
    ↓
Generate Response
```
This happens for each query in real-time.

---

## Advanced Retrieval Techniques

### Reranking
- Initial retrieval may not be perfect
- **Rerankers** (specialized models) improve ranking quality
- Uses **cross-encoders** to score relevance
- Trade-off: Extra computation vs. better results

### Hybrid Retrieval
- Combines dense (embedding-based) + sparse (keyword-based) search
- More robust than either alone
- Better handles both semantic and keyword matching

### Query Expansion
- Generate multiple variations of the query
- Retrieve results for all variations
- Improves coverage of relevant documents

### Multi-hop Retrieval
- For complex questions requiring multiple pieces of information
- Iteratively retrieve and reason
- Each retrieval refined based on previous results

---

## Key Challenges & Solutions

| Challenge · Impact · Solution |
|-----------|--------|----------|
| **Poor retrieval results** · LLM generates wrong answers · Use hybrid retrieval, reranking, better chunking |
| **Context contradiction** · LLM confused by conflicting info · Filter contradictory results, rerank better |
| **Lost context in chunks** · Important info split across chunks · Use overlapping chunks, adjust chunk size |
| **Embedding model mismatch** · Retrieval fails · Use same model for indexing & retrieval |
| **Scalability issues** · Slow queries · Use vector indexes (FAISS), parallel processing |
| **Knowledge base updates** · Stale information · Version control, update pipeline automation |
| **Hallucinations** · LLM makes up info · Better context, source attribution |
| **Token limit exceeded** · Can't fit all context · Compress context, select top-K smarter |

---

## Evaluation Metrics

**Retrieval Quality:**
- **Recall@K**: What % of relevant docs appeared in top K results?
- **Precision@K**: What % of top K results were relevant?
- **NDCG (Normalized Discounted Cumulative Gain)**: Ranking quality
- **MRR (Mean Reciprocal Rank)**: Position of first relevant result

**Generation Quality:**
- **BLEU Score**: Similarity to reference text
- **ROUGE**: Recall-Oriented Understudy for Gisting Evaluation
- **Human Evaluation**: Best for assessing coherence and correctness

**End-to-End:**
- **RAGAS (RAG Assessment)**: Framework specifically for RAG evaluation
- **Answer Correctness**: Does the answer match ground truth?
- **Source Attribution**: Are sources properly cited?

---

## When to Use RAG

### Good Fit:
- Working with up-to-date information (documents updated frequently)
- Domain-specific knowledge (legal, medical, technical docs)
- Citation/source requirements (compliance, transparency)
- Large knowledge bases (too much for model context)
- When hallucinations are costly (financial, medical, legal)
- Current events or recent data

### Poor Fit:
- General knowledge questions (model has sufficient knowledge)
- Small queries that don't need external context
- When latency is critical (retrieval adds overhead)
- Highly specialized reasoning beyond document content
- Real-time data requiring sub-second updates
- When document quality is unreliable

---

## Popular RAG Frameworks & Tools

| Framework · Focus · Best For |
|-----------|-------|----------|
| **LangChain** · Full-featured framework · General RAG applications |
| **LlamaIndex** · Data indexing & retrieval · Structured knowledge |
| **Haystack** · Modular pipelines · Custom RAG systems |
| **FastEmbed** · Lightweight embeddings · Edge devices, performance |
| **Azure AI Search** · Enterprise RAG · Cloud deployments |
| **Weaviate** · Vector database · Open-source solutions |

---

## Best Practices Checklist

✓ **Use same embedding model** for indexing and retrieval  
✓ **Experiment with chunk size** (typically 512-1024 tokens)  
✓ **Implement reranking** for better relevance  
✓ **Monitor retrieval quality** separately from generation  
✓ **Add hybrid retrieval** (dense + sparse) for robustness  
✓ **Version your knowledge base** and retrieval logic  
✓ **Cache embeddings** to avoid recomputing  
✓ **Test with real queries** from your domain  
✓ **Preserve metadata** (source, date, version)  
✓ **Implement fallback** when no good matches found  
✓ **Set overlap** between chunks (10-20%)  
✓ **Use recursive chunking** as default strategy  

---

## Advanced Techniques

- **Prompt chaining**: Use LLM to refine retrieval queries
- **Adaptive retrieval**: Decide when to retrieve vs. use model knowledge
- **Knowledge graphs**: Structure knowledge with relationships (Graph RAG)
- **Multi-hop reasoning**: Iterative retrieval for complex questions
- **Query classification**: Route to different knowledge bases
- **Context compression**: Summarize long contexts to fit token limits
- **Cross-lingual RAG**: Support multiple languages
- **Multimodal RAG**: Images, videos, tables + text

---

## Learning Resources

### Foundational:
- [NVIDIA RAG 101 Guide](https://developer.nvidia.com/blog/rag-101-demystifying-retrieval-augmented-generation-pipelines/)
- [IBM RAG Architecture Patterns](https://www.ibm.com/think/architectures/patterns/genai-rag)
- [What is RAG - NVIDIA Glossary](https://www.nvidia.com/en-us/glossary/retrieval-augmented-generation/)

### Deep Dives:
- [A Comprehensive Guide to RAG Pipelines - Medium](https://medium.com/@yashpaddalwar/a-comprehensive-guide-to-retrieval-augmented-generation-rag-pipelines-4a39d7bd366f)
- [Engineering the RAG Stack - Academic Paper](https://arxiv.org/pdf/2601.05264)
- [Retrieval-Augmented Generation Complete Guide](https://rudrai.medium.com/retrieval-augmented-generation-rag-a-complete-guide-to-architecture-types-and-building-your-fe9db3f0fdd8)

### Chunking Strategies:
- [Best Chunking Strategies for RAG 2026](https://www.firecrawl.dev/blog/best-chunking-strategies-rag)
- [Chunking for RAG Best Practices - Unstructured](https://unstructured.io/blog/chunking-for-rag-best-practices)
- [Mastering Chunking Strategies - Medium](https://medium.com/@sahin.samia/mastering-document-chunking-strategies-for-retrieval-augmented-generation-rag-c9c16785efc7)

### Vector Embeddings:
- [Azure Guide: Generate Embeddings](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-generate-embeddings)
- [Vector Databases for RAG - IBM](https://www.ibm.com/think/topics/rag-vector-database)
- [Ultimate Guide to Vector DB and RAG - LearnOpenCV](https://learnopencv.com/vector-db-and-rag-pipeline-for-document-rag/)

---

## Key Takeaways

1. **RAG = Retrieval + Generation**: The system retrieves relevant context before generating answers
2. **Chunking is critical**: How you split documents significantly impacts retrieval quality
3. **Embeddings are semantic**: Vector embeddings capture meaning, enabling similarity-based search
4. **Same model matters**: Use identical embedding model for indexing and retrieval
5. **Hybrid approach wins**: Combining dense + sparse retrieval improves robustness
6. **Evaluation is important**: Monitor both retrieval and generation quality separately
7. **Use the right tool**: RAG excels with domain knowledge, current data, and source requirements

---
