# LLM Learning Path

**Materials**: [Overview](README.md) · [00: Attention](00_attention_is_all_you_need.md) · [01: Fundamentals](01_llm_fundamentals.md) · [02: Examples](02_practical_examples.md) · [03: Reference](03_quick_reference.md) · [04: Hard Problems](04_hard_problems.md) · [05: Prompting](05_prompt_engineering.md)

A structured sequence to go from "what's an LLM?" to building production systems.

> Work through the files in order. Each builds on the previous one.

**Note**: File 00 is optional foundation. Start with it if you want deep understanding of Transformers; skip to file 01 if you want to learn LLMs faster.

---

## The Learning Sequence

### 00 — Attention Is All You Need (Optional Foundation)

**File**: `00_attention_is_all_you_need.md`

A deep dive into the paper that changed everything. Start here if you want to understand the math behind Transformers.

**Topics**:
- The problem it solves (word-by-word vs. all-at-once)
- How attention works (query, key, value vectors)
- Multi-head attention (multiple perspectives)
- Positional encoding (word order)
- Complete Transformer architecture (encoder + decoder)
- Step-by-step forward pass
- Connection to vector geometry
- Why it matters (parallelization, long-range memory)

| Info | Details |
|------|---------|
| **Best for** | Understanding the foundation deeply, implementing attention yourself |
| **Prerequisite** | Comfortable with vectors, dot products, matrix math |
| **Time** | 2-3 hours |
| **Note** | Read *before* file 01 if you want deep understanding. Optional but recommended. |

---

### 01 — LLM Fundamentals

**File**: `01_llm_fundamentals.md`

Start here. This covers the core concepts you need to know.

**Topics**:
- What LLMs actually are (weights + code)
- Transformers and self-attention
- Three-stage training pipeline
- Scaling laws (why bigger = better)
- Reasoning models (test-time compute)
- Tool use, agents, and RAG
- Security and alignment

| Info | Details |
|------|---------|
| **Hands-on** | Run a local LLM, implement attention, use Claude API |
| **Prerequisite** | None |
| **Time** | 3-4 days (1-2 hours per day) |

---

### 02 — Practical Examples

**File**: `02_practical_examples.md`

Time to write code. Don't just read—implement these.

**Topics**:
- Next-token prediction (understand the core mechanism)
- Self-attention (implement from scratch)
- Claude API calls (use tools, build agents)
- Fine-tuning a model
- RAG (retrieval-augmented generation)
- Security vulnerabilities and defenses
- Scaling laws (see them visually)

| Info | Details |
|------|---------|
| **Hands-on** | Run and modify every code example |
| **Prerequisite** | Basic Python |
| **Time** | 2-3 days |

---

### 03 — Quick Reference

**File**: `03_quick_reference.md`

Use this alongside files 1 and 2. Skip ahead anytime you need a definition.

**Topics**:
- Terminology (what does each term mean?)
- Model comparison table
- Decision trees (which model? fine-tune or RAG?)
- Key takeaways per section
- Diagnostic checklist (if X happens, try Y)

| Info | Details |
|------|---------|
| **Hands-on** | Lookup material only—no exercises |
| **Prerequisite** | Completed file 01 |
| **Time** | 15-30 min to skim |

---

### 04 — Hard Problems & Limitations

**File**: `04_hard_problems.md`

**Read this before you ship anything.** Seriously.

**What actually breaks in production**:
- Hallucination (models make things up—it's architectural)
- Alignment conflicts (helpful vs. honest vs. harmless—pick two)
- Why agents fail (they don't recover from mistakes well)
- Data quality matters more than scale
- Scaling laws are flattening
- Reasoning faithfulness is unknown
- Security is an arms race
- Interpretability at scale doesn't exist yet
- Production gaps (benchmarks ≠ real world)

| Info | Details |
|------|---------|
| **Hands-on** | Identify failure modes in your own projects |
| **Prerequisite** | Completed file 01 |
| **Time** | 1-2 days |
| **Important** | This separates people who build hype demos from people who build systems that work. |

---

### 05 — Prompt Engineering

**File**: `05_prompt_engineering.md`

How to actually get good behavior from these models.

**Approaches**:
- Anthropic approach (constitutional principles + reasoning)
- OpenAI approach (explicit instructions + examples)
- Hybrid approach (best for production)

| Info | Details |
|------|---------|
| **Hands-on** | Write prompts both ways, measure what works |
| **Prerequisite** | Completed files 01-02 |
| **Time** | 1-2 days |

---

## Timeline Options

### Intensive (2-3 weeks)

- **Week 1**: Read fundamentals, understand production reality (hard problems)
- **Week 2**: Code examples, prompt engineering
- **Week 3**: Build something (chatbot, RAG, agent)

### Structured (4-6 weeks)

- **Week 1**: Fundamentals sections 1-2, understand attention
- **Week 2**: Training & scaling, run your first code
- **Week 3**: Hard problems + prompt engineering
- **Week 4**: More code, build a working chatbot
- **Week 5+**: Specialize in what interests you

---

## Check Your Understanding

**After file 00** (if you read it):
- Can you explain the three vectors in attention (Query, Key, Value)?
- Do you understand how dot products become attention scores?
- Can you trace through a complete forward pass?

**After file 01**:
- Can you explain what an LLM is (weights + code)?
- Do you get how self-attention works?
- Why is training in three stages?
- What do scaling laws predict?

**After file 02**:
- Did you run the code examples?
- Can you make a Claude API call?
- Can you understand and modify the attention example?

**After file 03**:
- Can you look up a term quickly?
- Are the decision trees making sense?

**After file 04**:
- Know what hallucination really is?
- Understand why agents fail?
- Get the alignment conflicts?
- Know how to defend against prompt injection?

**After file 05**:
- Can you write prompts both ways?
- Do you know when to use each style?

---

## Quick Start (1 Hour)

1. Read this README (10 min)
2. Skim file 01, sections 1-2 (30 min)
3. Run one code example from file 02 (20 min)

**You'll understand**:
- What an LLM actually is
- How attention works
- How to use the Claude API

---

## Learning Outcomes

By the end, you should be able to:
- Explain LLMs to a non-ML person
- Understand and modify transformer code
- Fine-tune a model
- Build a RAG system
- Write effective prompts
- Spot potential failure modes
- Add security defenses
- Deploy a working chatbot
- Understand why data quality matters
- Defend against prompt injection

---

## How to Learn This

**Do:**
- Read, run code, then review—don't just read passively
- Take notes in your own words
- Run code as you read
- Build mini-projects after each section
- Use the quick reference to unblock
- Don't skip file 04 (separates pros from amateurs)
- Iterate on prompts and measure what works

**Don't:**
- Try to memorize everything
- Read without running code
- Skip the hard problems section
- Assume you understand without testing it
- Build without thinking about failure modes
- Deploy without understanding what can go wrong

---

## What's Next?

After you finish all 5 files:

**Go Deep**: Reasoning models, multimodality, RAG at scale, agents, security hardening

**Build Something**: A real chatbot, code assistant, research tool, customer support system

**Research**: Read papers, follow model releases, contribute to open source

---

## Quick Navigation

| Looking For | Location |
|---|---|
| Attention mechanism deep dive | File 00 (complete) |
| Transformers intro | File 00 (complete) or File 01 Section 2 (brief) |
| Fine-tuning | File 02 Section 4 |
| RAG | File 01 Section 6 + File 02 Section 5 |
| Prompting | File 05 (all) |
| Production challenges | File 04 (all) |
| Terminology | File 03 (all) |

---

## Stuck?

1. Check file 03 for terminology
2. Search with Ctrl+F for the term
3. Jump to the relevant section in files 01-05
4. Run the code example from file 02
5. Check if it's covered in file 04

---

## The Hard Truth

The hardest part of LLM engineering isn't understanding the models. It's building systems that work reliably in production.

That's why files 04 and 05 matter. You'll spend more time there than on concepts.

---

## Start Now

Open [`01_llm_fundamentals.md`](01_llm_fundamentals.md) and read sections 1-2. Takes 30 minutes, and you'll understand the foundation.
