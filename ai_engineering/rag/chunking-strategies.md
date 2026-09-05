# RAG Chunking Strategies: End-to-End Implementation

## Table of Contents
1. [Why Chunking Matters](#why-chunking-matters)
2. [Setup](#setup)
3. [Level 1: Fixed-Size Character Splitting](#level-1-fixed-size-character-splitting)
4. [Level 2: Recursive Character Splitting](#level-2-recursive-character-splitting)
5. [Level 3: Document-Structure-Aware Splitting](#level-3-document-structure-aware-splitting)
6. [Level 4: Token-Based Splitting](#level-4-token-based-splitting)
7. [Level 5: Sentence-Based Splitting](#level-5-sentence-based-splitting)
8. [Level 6: Semantic Chunking](#level-6-semantic-chunking)
9. [Level 7: Small-to-Big / Parent-Document Retrieval](#level-7-small-to-big--parent-document-retrieval)
10. [Level 8: Hierarchical Chunking](#level-8-hierarchical-chunking)
11. [Level 9: Contextual Retrieval (Anthropic Technique)](#level-9-contextual-retrieval-anthropic-technique)
12. [Level 10: Agentic Chunking](#level-10-agentic-chunking)
13. [Level 11: Late Chunking](#level-11-late-chunking)
14. [Level 12: Table & Structured-Data-Aware Chunking](#level-12-table--structured-data-aware-chunking)
15. [Decision Framework](#decision-framework)
16. [Full End-to-End Example](#full-end-to-end-example)

---

## 🚀 TL;DR: Which Strategy Should I Use?

**Don't read all 12 levels if you're new.** Pick one based on your data:

| Your Data | Use This | Why | Difficulty |
|-----------|----------|-----|------------|
| General text, prose, articles | **Level 2: Recursive Character** | Default, balanced, works everywhere | Easy |
| Code, Markdown, structured docs | **Level 3: Structure-Aware** | Respects syntax, no mid-function splits | Easy |
| Long documents (books, reports) | **Level 7: Small-to-Big** | Small chunks for search, big chunks for context | Medium |
| Meeting transcripts, unstructured | **Level 6: Semantic** | Splits where topic changes, not at char count | Medium |
| Everything else | **Start with Level 2, upgrade if needed** | 80% of cases use Level 2 | Easy |

**Pro tip:** Start with Level 2 (Recursive). When retrieval quality plateaus, try Level 7 (Small-to-Big), then Level 6 (Semantic). Advanced levels (8-12) are for optimization, not foundation.

---

## Why Chunking Matters

A RAG pipeline has two phases:

```
INDEXING:  Documents → Chunks → Embeddings → Vector DB
QUERYING:  User question → Embed question → Retrieve relevant chunks → 
           Feed chunks + question to LLM → Answer
```

**Bad chunking** → irrelevant or broken context retrieved → bad answers, no matter how good your LLM is.
**Good chunking** → the retrieved text is complete, relevant, and self-contained → accurate answers.

The strategies below progress from naive (breaks words mid-sentence) to production-grade (preserves full document context).

---

## Setup

```bash
conda create -n chunking python=3.11
conda activate chunking

pip install langchain langchain-experimental langchain-openai langchain-community
pip install chromadb tiktoken sentence-transformers spacy nltk
pip install rich pydantic

python -m spacy download en_core_web_sm

export OPENAI_API_KEY="your-key-here"
```

Sample text used in examples:

```python
sample_text = """
LangChain is a framework for developing applications powered by language models.
It enables applications that are context-aware and can reason about their environment.

ChatGPT was developed by OpenAI and released in November 2022. It is built on top of
the GPT architecture and fine-tuned using reinforcement learning from human feedback.
ChatGPT allows for dynamic interaction between users and the model, enabling
conversational applications across many domains.

Text splitting is a critical preprocessing step in any retrieval-augmented generation
system. Without proper splitting, retrieval quality degrades significantly, leading to
incomplete or misleading context being passed to the language model.
"""
```

---

## Level 1: Fixed-Size Character Splitting

**Idea:** Cut the text every N characters. Simplest, worst quality — breaks words and sentences mid-way.

```python
from langchain.text_splitter import CharacterTextSplitter

text_splitter = CharacterTextSplitter(
    separator="",       # no separator awareness — pure character count
    chunk_size=50,
    chunk_overlap=4,    # overlap helps LLM see continuity between chunks
)

docs = text_splitter.create_documents([sample_text])
for d in docs:
    print(repr(d.page_content))
```

**Problem:** with `chunk_size=50` you'll see words like "mountains" split into "mo" + "untains". Raising `chunk_overlap` only partially helps — the root issue is ignoring word/sentence boundaries.

**When to use:** Almost never in production. Only for quick prototyping or truly unstructured byte streams.

---

## Level 2: Recursive Character Splitting

**Idea:** Try splitting on a prioritized list of separators (`\n\n` → `\n` → `" "` → `""`), falling back to the next only if a chunk is still too big. This respects paragraph/sentence structure much better.

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=450,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " ", ""],  # priority order
)

docs = text_splitter.create_documents([sample_text])
for d in docs:
    print(d.page_content)
    print("---")
```

**Key tuning insight:** `chunk_size` is highly sensitive to your content. Too small (e.g. 65 chars) truncates mid-thought constantly; 400–800 chars (or ~150–300 tokens) is a common starting point. Always tune against your actual corpus.

**When to use:** This is the default, sane baseline for most RAG systems on unstructured text. Start here before reaching for anything fancier.

---

## Level 3: Document-Structure-Aware Splitting

**Idea:** Use splitters that understand the syntax of the source format (Markdown headers, Python functions, JS code) so chunks align with logical units, not arbitrary character counts.

### Markdown

```python
from langchain.text_splitter import MarkdownTextSplitter

md_text = """
# Introduction
This section introduces the topic.

## Details
This section goes into detail about the topic and provides examples.
"""

md_splitter = MarkdownTextSplitter(chunk_size=200, chunk_overlap=20)
docs = md_splitter.create_documents([md_text])
```

For header-aware chunking that **preserves metadata** (which section a chunk came from):

```python
from langchain.text_splitter import MarkdownHeaderTextSplitter

headers_to_split_on = [("#", "H1"), ("##", "H2"), ("###", "H3")]
md_header_splitter = MarkdownHeaderTextSplitter(headers_to_split_on)
docs = md_header_splitter.split_text(md_text)
# each doc.metadata now contains {'H1': 'Introduction', ...}
```

### Python Code

```python
from langchain.text_splitter import PythonCodeTextSplitter

python_code = """
def add(a, b):
    return a + b

class Calculator:
    def multiply(self, a, b):
        return a * b
"""

python_splitter = PythonCodeTextSplitter(chunk_size=100, chunk_overlap=0)
docs = python_splitter.create_documents([python_code])
```

### JavaScript & Other Languages

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter, Language

js_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.JS, chunk_size=100, chunk_overlap=0
)
docs = js_splitter.create_documents([js_code])
```

Supported `Language` enums: `PYTHON`, `JS`, `TS`, `JAVA`, `MARKDOWN`, `HTML`, `CPP`, `GO`, `RUST`, etc.

**When to use:** Any time your source has explicit structure (code repos, Markdown docs, HTML pages). Don't throw away structure you already have.

---

## Level 4: Token-Based Splitting

**Idea:** Character count ≠ token count (what the LLM actually "sees"). Splitting by tokens keeps chunks aligned with your model's context window and embedding model's input limits.

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tiktoken

# Use tiktoken directly to count tokens for a given model
encoding = tiktoken.encoding_for_model("gpt-4")

def token_len(text):
    return len(encoding.encode(text))

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,          # now measured in TOKENS
    chunk_overlap=30,
    length_function=token_len,
)
docs = text_splitter.create_documents([sample_text])
```

Or use LangChain's built-in tiktoken splitter:

```python
from langchain.text_splitter import TokenTextSplitter

splitter = TokenTextSplitter(chunk_size=300, chunk_overlap=30)
docs = splitter.split_text(sample_text)
```

**Why it matters:** Embedding models (e.g. `text-embedding-3-small`) and LLMs have hard token limits. A 450-character chunk in English is ~90-120 tokens, but in Chinese/Japanese can be 2-3x more tokens. Token-based splitting avoids silent truncation.

**When to use:** Any production system, especially multilingual corpora, or when you need precise cost/context-window control.

---

## Level 5: Sentence-Based Splitting

**Idea:** Split on actual sentence boundaries using NLP (not naive `.` splitting, which breaks on abbreviations like "Dr.", "U.S.", "3.14").

```python
import spacy

nlp = spacy.load("en_core_web_sm")

def sentence_split(text, max_chunk_chars=500):
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents]

    chunks, current = [], ""
    for sent in sentences:
        if len(current) + len(sent) <= max_chunk_chars:
            current += " " + sent
        else:
            chunks.append(current.strip())
            current = sent
    if current:
        chunks.append(current.strip())
    return chunks

chunks = sentence_split(sample_text)
```

**Why it beats naive full-stop splitting:** "Dr. Smith earns $3.5 million." won't be incorrectly split at "Dr." or "$3.5".

**When to use:** Prose-heavy documents (articles, legal text, transcripts) where sentence integrity matters more than fixed size.

---

## Level 6: Semantic Chunking

**Idea:** Embed sentences, measure the semantic distance between consecutive sentences, and split where the *meaning* shifts — not where a character count runs out.

```python
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()

text_splitter = SemanticChunker(
    embeddings,
    breakpoint_threshold_type="percentile",
    breakpoint_threshold_amount=95,  # top 5% biggest jumps = new chunk
)

docs = text_splitter.create_documents([sample_text])
for d in docs:
    print(d.page_content)
    print("---")
```

**Threshold types:**
| Type | How it decides |
|---|---|
| `percentile` | Split at the Nth percentile of all distance jumps |
| `standard_deviation` | Split where the jump exceeds mean + k·std_dev |
| `interquartile` | Split using IQR-based outlier detection |

**When to use:** Long-form content with topic shifts (research papers, meeting transcripts, multi-topic articles) where fixed-size chunks would arbitrarily cut across unrelated ideas.

---

## Level 7: Small-to-Big / Parent-Document Retrieval

**Idea:** Embed **small** chunks for precise semantic search, but when retrieved, return the **larger parent chunk** to the LLM so it has full context. Solves "chunk too small to be useful, too big to be precise".

```python
from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

# Small chunks used ONLY for embedding/search
child_splitter = RecursiveCharacterTextSplitter(chunk_size=200)

# Big chunks returned to the LLM as actual context
parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000)

vectorstore = Chroma(collection_name="small_chunks", embedding_function=OpenAIEmbeddings())
store = InMemoryStore()  # holds the parent documents

retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter,
)

docs = TextLoader("content.txt").load()
retriever.add_documents(docs)

# On query: searches small chunks, returns full parent chunk
results = retriever.invoke("What is LangChain used for?")
```

**When to use:** One of the most common production patterns — nearly always an upgrade over plain fixed-size/recursive chunking when you have room in your context window.

---

## Level 8: Hierarchical Chunking

**Idea:** Build a tree — Document → Sections → Paragraphs → Sentences — and retrieve at whichever level of granularity best answers the query, optionally walking up the tree for more context.

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

def build_hierarchy(document_text, doc_id):
    section_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000, separators=["\n## ", "\n# "]
    )
    paragraph_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, separators=["\n\n"]
    )

    tree = []
    sections = section_splitter.split_text(document_text)
    for s_idx, section in enumerate(sections):
        paragraphs = paragraph_splitter.split_text(section)
        for p_idx, para in enumerate(paragraphs):
            tree.append({
                "doc_id": doc_id,
                "section_id": f"{doc_id}-s{s_idx}",
                "paragraph_id": f"{doc_id}-s{s_idx}-p{p_idx}",
                "text": para,
                "parent_section_text": section,
            })
    return tree

hierarchy = build_hierarchy(sample_text, doc_id="doc1")
# Embed at paragraph level for precision, fetch full section for context
```

**When to use:** Very long documents (legal contracts, technical manuals, books) where a flat chunk list loses too much structural relationship info.

---

## Level 9: Contextual Retrieval (Anthropic Technique)

**Idea:** Before embedding each chunk, ask an LLM to generate a short (~50-100 token) contextual blurb explaining what the chunk is about *relative to the whole document*, and prepend it to the chunk before embedding. Much cheaper than agentic chunking, and empirically improves retrieval accuracy significantly.

```python
from anthropic import Anthropic

client = Anthropic()

CONTEXT_PROMPT = """<document>
{doc_content}
</document>

Here is the chunk we want to situate within the whole document:
<chunk>
{chunk_content}
</chunk>

Give a short, succinct context (2-3 sentences) to situate this chunk within
the overall document for improving search retrieval of the chunk.
Answer only with the succinct context and nothing else."""

def add_context_to_chunk(full_document, chunk_text):
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        messages=[{
            "role": "user",
            "content": CONTEXT_PROMPT.format(
                doc_content=full_document, chunk_content=chunk_text
            ),
        }],
    )
    context = response.content[0].text
    return f"{context}\n\n{chunk_text}"

# Apply to every chunk from any splitter above
contextualized_chunks = [
    add_context_to_chunk(sample_text, chunk.page_content) for chunk in docs
]
```

**Cost tip:** Use prompt caching on the full document (it's the same across all chunks of that doc) so you're only paying full price once per document, not once per chunk.

**When to use:** Strong default upgrade for any RAG system where retrieval accuracy matters and you can afford a one-time preprocessing LLM call per chunk. Cheaper and simpler than agentic chunking.

---

## Level 10: Agentic Chunking

**Idea (two sub-levels):**
1. **Proposition-based chunking** — use an LLM to rewrite passages into atomic, self-contained "propositions" (each stands alone with full context, e.g. resolving pronouns).
2. **Agentic grouping** — use an LLM to dynamically decide which propositions belong together into semantically coherent groups, creating/updating "chunk summaries" as it goes (like a human editor sorting index cards into folders).

```python
# --- Step 1: Proposition extraction ---
from langchain import hub
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

class Sentences(BaseModel):
    sentences: list[str]

def get_propositions(text):
    paragraphs = text.split("\n\n")
    propositions = []
    for para in paragraphs:
        # LLM call to decompose paragraph into propositions
        result = llm.with_structured_output(Sentences).invoke(
            f"Break this into self-contained sentences: {para}"
        )
        propositions.extend(result.sentences)
    return propositions

props = get_propositions(sample_text)
# e.g. ["Text splitting in LangChain is a critical feature.",
#       "ChatGPT was developed by OpenAI.",
#       "ChatGPT allows for dynamic interaction.", ...]
```

```python
# --- Step 2: Agentic grouping ---
class AgenticChunker:
    def __init__(self, llm):
        self.llm = llm
        self.chunks = {}

    def add_proposition(self, proposition):
        best_chunk_id = self._find_relevant_chunk(proposition)
        if best_chunk_id:
            self.chunks[best_chunk_id]["propositions"].append(proposition)
            self._update_chunk_summary(best_chunk_id)
        else:
            self._create_new_chunk(proposition)

    def _find_relevant_chunk(self, proposition):
        # LLM call: "Does this fit an existing chunk? Return chunk_id or None."
        ...

    def get_chunks(self):
        return [
            "\n".join(c["propositions"]) for c in self.chunks.values()
        ]

chunker = AgenticChunker(llm)
for prop in props:
    chunker.add_proposition(prop)

final_chunks = chunker.get_chunks()
```

**Tradeoff:** Highest quality, self-contained, well-grouped chunks — but requires an LLM call per proposition and per grouping decision (slow and expensive at scale).

**When to use:** High-value, lower-volume corpora (internal knowledge bases, curated documentation) where retrieval quality justifies the cost. For large-scale corpora, prefer Contextual Retrieval or Small-to-Big instead.

---

## Level 11: Late Chunking

**Idea:** Reverse the usual order. Instead of chunking first then embedding each chunk (losing document-level context), embed the **entire document** first using a long-context embedding model, then split the resulting *token-level embeddings* into chunks afterward (mean-pooling each span). Every chunk's embedding is influenced by the full document.

```python
from transformers import AutoModel, AutoTokenizer
import torch

tokenizer = AutoTokenizer.from_pretrained("jinaai/jina-embeddings-v2-base-en")
model = AutoModel.from_pretrained("jinaai/jina-embeddings-v2-base-en", trust_remote_code=True)

def late_chunking(document_text, chunk_size_tokens=200):
    inputs = tokenizer(document_text, return_tensors="pt", truncation=False)
    with torch.no_grad():
        # token-level embeddings for the WHOLE document
        token_embeddings = model(**inputs)[0][0]

    num_tokens = token_embeddings.shape[0]
    chunk_embeddings = []
    chunk_texts = []

    for start in range(0, num_tokens, chunk_size_tokens):
        end = min(start + chunk_size_tokens, num_tokens)
        # mean-pool this span of token embeddings
        span_embedding = token_embeddings[start:end].mean(dim=0)
        chunk_embeddings.append(span_embedding)
        chunk_text = tokenizer.decode(inputs["input_ids"][0][start:end])
        chunk_texts.append(chunk_text)

    return list(zip(chunk_texts, chunk_embeddings))

chunks_with_embeddings = late_chunking(sample_text)
```

**Requirement:** Needs a long-context embedding model (e.g. Jina Embeddings v2/v3, supporting 8K token context) since the whole document must fit in one forward pass.

**When to use:** When chunks currently lose important document-wide context and you have a long-context embedding model available.

---

## Level 12: Table & Structured-Data-Aware Chunking

**Idea:** Never let a generic text splitter break a table row, cell, or code block mid-way. Detect and handle tables/code separately from prose.

```python
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_preserving_tables(text):
    # crude table detector for markdown-style tables
    table_pattern = r"(\|.+\|\n)+"
    parts = re.split(f"({table_pattern})", text)

    prose_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    final_chunks = []

    for part in parts:
        if not part.strip():
            continue
        if re.match(table_pattern, part):
            # keep the ENTIRE table as one chunk
            final_chunks.append(part.strip())
        else:
            final_chunks.extend(prose_splitter.split_text(part))

    return final_chunks

chunks = split_preserving_tables(document_with_tables)
```

For PDFs with real tables, use a layout-aware extractor first:

```python
import camelot

tables = camelot.read_pdf("report.pdf", pages="all")
for i, table in enumerate(tables):
    table_markdown = table.df.to_markdown()
    # treat table_markdown as ONE indivisible chunk
```

**When to use:** Any corpus with financial reports, spec sheets, pricing tables, or structured data — splitting a table mid-row silently destroys the data's meaning.

---

## Decision Framework

| Your situation | Recommended strategy |
|---|---|
| Quick prototype | Recursive character splitting |
| General-purpose production RAG, prose | Recursive + Contextual Retrieval |
| Code, Markdown, structured sources | Document-structure-aware splitting |
| Multilingual / need token control | Token-based splitting |
| Long docs with topic shifts | Semantic chunking |
| Chunks need more context | Small-to-big / parent-document |
| Very long documents (books, contracts) | Hierarchical chunking |
| High-value corpus, best accuracy | Contextual retrieval or agentic |
| Long-context embedding model | Late chunking |
| Financial reports, structured tables | Table-aware chunking |
| Massive scale, cost-sensitive | Recursive + Contextual Retrieval |

**Practical recommendation (2025+):** Start with recursive character/token splitting as your base, add Contextual Retrieval on top for a big accuracy boost at reasonable cost, and use Small-to-Big retrieval so embedded chunks stay small/precise while the LLM still gets full paragraph context. Reserve full agentic chunking for smaller, high-stakes corpora.

---

## Full End-to-End Example

Putting recursive splitting + contextual retrieval + Chroma together:

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from anthropic import Anthropic

# --- 1. Load & split ---
with open("content.txt") as f:
    raw_text = f.read()

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
raw_chunks = splitter.create_documents([raw_text])

# --- 2. Add context to each chunk (contextual retrieval) ---
client = Anthropic()

def contextualize(chunk_text, full_doc):
    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=150,
        messages=[{"role": "user", "content": f"""<document>{full_doc}</document>
<chunk>{chunk_text}</chunk>
Give 1-2 sentences situating this chunk in the document. Answer only with the context."""}]
    )
    return resp.content[0].text

for doc in raw_chunks:
    context = contextualize(doc.page_content, raw_text)
    doc.page_content = f"{context}\n\n{doc.page_content}"

# --- 3. Embed & store ---
vectorstore = Chroma.from_documents(raw_chunks, OpenAIEmbeddings())
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# --- 4. RAG chain ---
prompt = ChatPromptTemplate.from_template("""
Answer the question based only on the context below.

Context:
{context}

Question: {question}
""")

llm = ChatOpenAI(model="gpt-4", temperature=0)

def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

answer = rag_chain.invoke("What is LangChain used for?")
print(answer)
```

---

## Key Takeaways

✓ Fixed-size splitting is the naive baseline — avoid it in production  
✓ Recursive character/token splitting is a solid, cheap default  
✓ Respect existing structure (Markdown headers, code syntax)  
✓ Semantic chunking groups by meaning, not character count  
✓ Small-to-big retrieval solves "small chunk = precise, but not enough context"  
✓ Contextual retrieval is the best cost/accuracy tradeoff upgrade  
✓ Agentic chunking gives highest quality but doesn't scale cheaply  
✓ Late chunking preserves whole-document context inside every embedding  
✓ Always special-case tables/code — never let a generic splitter break them
