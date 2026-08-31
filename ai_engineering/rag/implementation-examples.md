# RAG Implementation Examples

**RAG Materials** - [Overview](README.md) · [Study Guide](notes.md) · [Code Examples](implementation-examples.md) · [Quick Reference](quick-reference.md)

## 1. Simple RAG Pipeline with LangChain

```python
from langchain.document_loaders import PDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.llms import ChatOpenAI

# Step 1: Load documents
loader = PDFLoader("document.pdf")
documents = loader.load()

# Step 2: Split into chunks (RecursiveCharacterTextSplitter - recommended)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # Size of each chunk
    chunk_overlap=200,    # 20% overlap
    separators=["\n\n", "\n", " ", ""]
)
chunks = text_splitter.split_documents(documents)

# Step 3: Create embeddings
embeddings = OpenAIEmbeddings()

# Step 4: Store in vector database
vector_db = Chroma.from_documents(chunks, embeddings)

# Step 5: Create retriever
retriever = vector_db.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}  # Retrieve top 3 chunks
)

# Step 6: Setup RAG chain
llm = ChatOpenAI(model="gpt-4", temperature=0)
rag_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True
)

# Step 7: Query
result = rag_chain("What is the main topic of the document?")
print(result['result'])
print("Sources:", result['source_documents'])
```

---

## 2. Hybrid Retrieval (Dense + Sparse)

```python
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

# Dense retriever (semantic/embedding-based)
dense_retriever = Chroma.from_documents(
    chunks, 
    OpenAIEmbeddings()
).as_retriever(search_kwargs={"k": 3})

# Sparse retriever (keyword-based BM25)
sparse_retriever = BM25Retriever.from_documents(chunks)
sparse_retriever.k = 3

# Ensemble retriever combines both
ensemble_retriever = EnsembleRetriever(
    retrievers=[dense_retriever, sparse_retriever],
    weights=[0.5, 0.5]  # Equal weight to each
)

# Use in RAG chain
rag_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=ensemble_retriever,
    return_source_documents=True
)
```

---

## 3. Reranking for Better Relevance

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CohereRerank

# Base retriever
base_retriever = vector_db.as_retriever(search_kwargs={"k": 10})

# Reranker - reorder results by relevance
compressor = CohereRerank(
    model="rerank-english-v2.0",
    top_n=3  # Keep top 3 after reranking
)

# Wraps base retriever with compression/reranking
reranking_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=base_retriever
)

# Use in RAG chain
rag_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=reranking_retriever,
    return_source_documents=True
)
```

---

## 4. Query Expansion for Better Coverage

```python
from langchain.retrievers import MultiQueryRetriever
from langchain.llms import ChatOpenAI

# Generate multiple query variations automatically
retriever = MultiQueryRetriever.from_llm(
    retriever=vector_db.as_retriever(),
    llm=ChatOpenAI(temperature=0),
    prompt=prompt_template  # Custom prompt to generate variations
)

# The retriever will:
# 1. Generate alternative queries
# 2. Retrieve for each variation
# 3. Merge and deduplicate results
results = retriever.get_relevant_documents("What are quantum computing benefits?")
```

---

## 5. Metadata Filtering (Advanced)

```python
# Add metadata when creating chunks
from langchain.schema import Document

documents_with_metadata = []
for doc in chunks:
    doc_with_meta = Document(
        page_content=doc.page_content,
        metadata={
            "source": "financial_report_2024.pdf",
            "section": "revenue",
            "page": 5,
            "date": "2024-01-15",
            "author": "Finance Team"
        }
    )
    documents_with_metadata.append(doc_with_meta)

# Store in vector DB
vector_db = Chroma.from_documents(documents_with_metadata, embeddings)

# Filter during retrieval
retriever = vector_db.as_retriever(
    search_type="similarity",
    search_kwargs={
        "k": 5,
        "filter": {
            "section": {"$eq": "revenue"},
            "date": {"$gte": "2024-01-01"}
        }
    }
)
```

---

## 6. Chunking Strategies Comparison

```python
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
    MarkdownHeaderTextSplitter,
    SpacyTextSplitter
)

# Strategy 1: Simple character-based (NOT RECOMMENDED)
simple_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=1000,
    chunk_overlap=200
)

# Strategy 2: Recursive (RECOMMENDED - default)
recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", " ", ""]  # Try these in order
)

# Strategy 3: Markdown-aware (for markdown documents)
markdown_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=[
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
)

# Strategy 4: Spacy-based (sentence-aware)
spacy_splitter = SpacyTextSplitter(chunk_size=1000)

# Best practice: RecursiveCharacterTextSplitter
chunks = recursive_splitter.split_text(text)
```

---

## 7. Similarity Visualization (t-SNE)

```python
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from langchain.embeddings import OpenAIEmbeddings

# Get embeddings for your chunks
embeddings_model = OpenAIEmbeddings()
embedding_vectors = embeddings_model.embed_documents(
    [chunk.page_content for chunk in chunks]
)

# Also embed your query
query = "What is machine learning?"
query_embedding = embeddings_model.embed_query(query)

# Reduce to 2D using t-SNE
tsne = TSNE(n_components=2, random_state=42)
reduced_embeddings = tsne.fit_transform(embedding_vectors + [query_embedding])

# Plot
plt.figure(figsize=(10, 8))
plt.scatter(reduced_embeddings[:-1, 0], reduced_embeddings[:-1, 1], 
            alpha=0.6, label="Document chunks")
plt.scatter(reduced_embeddings[-1, 0], reduced_embeddings[-1, 1], 
            color='red', s=200, marker='*', label="Your query")
plt.legend()
plt.title("Document Embeddings (t-SNE Visualization)")
plt.show()
```

---

## 8. Evaluating RAG Quality

```python
# RAGAS - RAG Assessment framework
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_recall,
    context_precision
)

# Prepare evaluation dataset
eval_dataset = {
    "question": ["What is RAG?", "How do embeddings work?"],
    "answer": ["RAG combines...", "Embeddings are..."],
    "context": [["Retrieved chunk 1", "Retrieved chunk 2"], ...],
    "ground_truth": ["Expected answer 1", "Expected answer 2"]
}

# Evaluate
results = evaluate(
    dataset=eval_dataset,
    metrics=[
        faithfulness,        # Is answer faithful to context?
        answer_relevancy,    # Is answer relevant to question?
        context_recall,      # Did we retrieve all relevant context?
        context_precision    # Was retrieved context precise?
    ]
)

print(f"Faithfulness Score: {results['faithfulness']}")
print(f"Answer Relevancy Score: {results['answer_relevancy']}")
print(f"Context Recall: {results['context_recall']}")
print(f"Context Precision: {results['context_precision']}")
```

---

## 9. Chunking Config Best Practices

```python
# Configuration for different use cases

# For fact-focused retrieval (Q&A systems)
FACT_CONFIG = {
    "chunk_size": 256,      # Smaller for precision
    "chunk_overlap": 50,    # ~20% overlap
    "separators": ["\n\n", "\n", " ", ""]
}

# For context-heavy retrieval (summarization, reports)
CONTEXT_CONFIG = {
    "chunk_size": 1024,     # Larger for context preservation
    "chunk_overlap": 200,   # ~20% overlap
    "separators": ["\n\n", "\n", " ", ""]
}

# For technical documentation
TECH_CONFIG = {
    "chunk_size": 512,      # Medium - balance
    "chunk_overlap": 100,   # ~20% overlap
    "separators": ["\n```\n", "\n\n", "\n", " ", ""]  # Code-aware
}

# Apply config
splitter = RecursiveCharacterTextSplitter(
    chunk_size=FACT_CONFIG["chunk_size"],
    chunk_overlap=FACT_CONFIG["chunk_overlap"],
    separators=FACT_CONFIG["separators"]
)
```

---

## Key Implementation Checklist

- [ ] Choose appropriate embedding model (OpenAI, Sentence Transformers, etc.)
- [ ] Select chunking strategy (RecursiveCharacterTextSplitter recommended)
- [ ] Configure chunk size & overlap based on use case
- [ ] Preserve metadata (source, date, section, etc.)
- [ ] Use same embedding model for indexing and retrieval
- [ ] Implement hybrid retrieval (dense + sparse) for robustness
- [ ] Add reranking for better relevance
- [ ] Set up evaluation metrics (RAGAS framework)
- [ ] Monitor retrieval quality separately from generation
- [ ] Test with domain-specific queries
- [ ] Implement caching for frequently used documents
- [ ] Set up logging and monitoring for production

---
