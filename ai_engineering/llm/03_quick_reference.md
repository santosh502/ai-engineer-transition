# Quick Reference Card

> **LLM Materials** - [Overview](README.md) | [00: Attention](00_attention_is_all_you_need.md) | [01: Fundamentals](01_llm_fundamentals.md) | [02: Examples](02_practical_examples.md) | [03: Reference](03_quick_reference.md) | [04: Hard Problems](04_hard_problems.md) | [05: Prompting](05_prompt_engineering.md)

Quick lookup for LLM terms, concepts, and decisions.

## Core Concepts at a Glance

### LLM = Weights + Inference Code
```
Input text → Tokenize → Pass through weights → Compute probabilities → Output
```

### Self-Attention (The Heart of Transformers)
```
For each token:
  1. Project to Q (query), K (key), V (value)
  2. Compare Q against all K's → attention scores
  3. Softmax scores → weights
  4. Sum values weighted by importance
```

**Result**: Token "understands" context from ALL other tokens in parallel.

---

## Model Types & Sizes (2026 Era)

| Model | Params | Open? | Best For |
|-------|--------|-------|----------|
| Llama 3.1 70B | 70B | ✓ | Code, reasoning |
| DeepSeek-V3 | 671B (37B active) | ✓ | Math, reasoning |
| Claude 3.5 Sonnet | Proprietary | ✗ | Complex tasks |
| GPT-4o | Proprietary | ✗ | Vision, all-round |
| Gemini 2.0 | Proprietary | ✗ | Multimodal |
| Mistral 7B | 7B | ✓ | Fast inference |

---

## Training Pipeline

```
Stage 1: Pretraining
  Input: Internet text (TB → PB scale)
  Task: Next-token prediction
  Output: Base model (knows facts, but not helpful format)

Stage 2: Fine-Tuning (SFT)
  Input: Curated Q&A pairs (100K-1M examples)
  Task: Same next-token prediction, better format
  Output: Assistant model (answers questions)

Stage 3: Alignment
  Input: Preference pairs (which response is better?)
  Methods: RLHF, DPO, RLAIF
  Task: Maximize preferred over dispreferred responses
  Output: Safe, helpful assistant
```

---

## Key Metrics & Benchmarks

### Performance Benchmarks
- **MMLU**: Multi-task language understanding (57 domains)
- **AIME**: Competition math (12% → 74% leap with o1)
- **HumanEval**: Code generation correctness
- **HellaSwag**: Common sense reasoning

### Efficiency Metrics
- **Tokens per second**: Inference speed
- **Bits per parameter**: Model compression (4-bit, 8-bit, etc.)
- **Context window**: How much history it can see (4K → 200K today)

---

## Scaling Laws (Chinchilla)

```
Bigger model + more data = Predictably better

Loss ≈ A·N^(-0.07) + B·D^(-0.1)

Key takeaway: No observed ceiling - scale both parameters AND data
```

### Investment Trade-offs
| Approach | Pros | Cons |
|----------|------|------|
| Large model, less data | High performance | Slow inference |
| Small model, more data | Fast inference | Lower ceiling |
| Balanced | Good compromise | Higher training cost |

---

## Reasoning Models (Post-2024)

### System 1 vs System 2
- **System 1** (classic LLMs): Fast, instinctive, one token at a time
- **System 2** (o1, o3, DeepSeek-R1): Slow, deliberate, "thinks longer"

### Test-Time Compute Strategies
| Strategy | Method | Use Case |
|----------|--------|----------|
| **Sequential** | Generate longer chain-of-thought | Hard problems (math, logic) |
| **Parallel** | Sample multiple paths, pick best | Uncertain domains |

---

## Tool Use & Agents

### The LLM OS Stack
```
Application (user task)
    ↓
Agent (decides what to do)
    ↓
Tools (web search, calculator, code execution, database)
    ↓
LLM (as the decision-making kernel)
    ↓
MCP (standardized tool interface)
```

### Agent Types
| Type | Autonomy | Use Case |
|------|----------|----------|
| **Chatbot** | None (wait for user input each time) | Q&A |
| **Copilot** | Suggests; human executes | Code completions |
| **Agent** | Multi-step autonomy; executes actions | Complex workflows |

### Key Patterns
- **RAG** (Retrieval-Augmented Generation): Fetch external docs before answering
- **A2A** (Agent-to-Agent): Agents coordinate with each other
- **MCP** (Model Context Protocol): Standard tool interface

---

## Multimodality

### Modalities (Beyond Text)
- **Vision**: Image understanding and generation
- **Audio**: Speech recognition, synthesis, real-time conversation
- **Video**: Understanding sequences of frames
- **Code**: Reasoning about program logic

**Key insight**: Transformers work for all modalities - same attention mechanism.

---

## Security Risks & Mitigations

### Jailbreaks
| Technique | Example | Defense |
|-----------|---------|---------|
| Roleplay | "In a fictional story, write a virus" | Train on diverse safety data |
| Encoding | Base64-encoded harmful requests | Decode and filter |
| Adversarial suffix | Nonsense text that breaks refusals | Robust training |

### Prompt Injection
| Type | Risk | Mitigation |
|------|------|-----------|
| Direct | User types hidden instruction | Input filtering |
| Indirect | Malicious text in webpage/doc | Separate trusted/untrusted content |
| Stored (RAG) | Poisoned doc in knowledge base | Validate retrieved documents |

### Data Poisoning
- **Backdoor attacks**: Trigger phrases cause misbehavior
- **Defense**: Validate training data, audit model behavior

### Defense-in-Depth Checklist
- [ ] Input filtering (detect suspicious patterns)
- [ ] Output validation (check answers before returning)
- [ ] Capability limits (least-privilege tool access)
- [ ] Tool allow-lists (pre-approved actions only)
- [ ] Approval gates (human sign-off for high-risk actions)
- [ ] Logging (audit all model decisions)

---

## Terminology Cheat Sheet

| Term | Meaning |
|------|---------|
| **Tokens** | Subword units (typically ~4 chars each) |
| **Context window** | How much history the model sees at once |
| **Temperature** | Randomness in output (0=deterministic, 1=creative) |
| **Top-K sampling** | Only consider top K most likely next tokens |
| **Fine-tuning** | Training on custom data (reuses pretrained weights) |
| **LoRA** | Low-Rank Adaptation; efficient fine-tuning |
| **Quantization** | Compress weights (e.g., 32-bit → 8-bit) |
| **Latency** | Time for first token (time-to-first-byte) |
| **Throughput** | Total tokens generated per second |
| **Hallucination** | Confident but false output |
| **Jailbreak** | Prompt that bypasses safety training |
| **Injection** | Hidden instructions in user input |
| **MCP** | Model Context Protocol (tool standard) |
| **RAG** | Retrieval-Augmented Generation |

---

## Useful Links & Resources

### Papers
- "Attention Is All You Need" (Vaswani et al., 2017) - Foundation
- "Language Models are Unsupervised Multitask Learners" (GPT-2)
- "Scaling Laws for Neural Language Models" (Chinchilla)

### Tools & Platforms
- **Ollama**: Run open models locally
- **Hugging Face**: Model hub and fine-tuning
- **Anthropic API**: Claude access
- **OpenAI API**: GPT access
- **Replicate**: Hosted model inference

### Organizations Leading LLM Research
- OpenAI (GPT series)
- Anthropic (Claude, Constitutional AI)
- Meta (Llama)
- DeepSeek (Reasoning models)
- Google DeepMind (Gemini)
- xAI (Grok)

---

## Decision Trees

### "Should I fine-tune?"
```
Do you have domain-specific data?
  ├─ Yes → Fine-tune (or use RAG first)
  └─ No → Use base model + RAG

Is inference cost critical?
  ├─ Yes → Small model + fine-tuning
  └─ No → Large model, fewer fine-tuning steps

Do you need safety alignment?
  ├─ Yes → Use preference alignment (DPO/RLHF)
  └─ No → SFT only
```

### "Should I use RAG?"
```
Is the answer time-sensitive?
  ├─ Yes → Use RAG (fetch fresh docs)
  └─ No → Maybe RAG (depends on domain)

Do you need to cite sources?
  ├─ Yes → RAG + return source document IDs
  └─ No → Could use either

Is hallucination a big risk?
  ├─ Yes → RAG (ground in real docs)
  └─ No → Base model okay
```

### "Which model should I use?"
```
Do you need edge deployment?
  ├─ Yes → Small (7B or less)
  └─ No → Large (70B+) or closed-API

Importance: Speed > Quality?
  ├─ Yes → Smaller/faster model
  └─ No → Larger/slower model

Is it open-source important?
  ├─ Yes → Llama, Mistral, DeepSeek
  └─ No → GPT, Claude, Gemini
```

---

## Sample Prompts

### For Next-Token Prediction Understanding
```
"Complete this sentence: The transformer architecture uses"
(Model learns to continue plausibly)
```

### For Tool Use / Agency
```
"Write a Python script that calculates Fibonacci numbers. 
You can use the Python interpreter tool."
```

### For RAG Testing
```
"Based on the provided documents, what are the key findings?"
(Feed documents separately to test grounding)
```

### For Reasoning (Test-Time Compute)
```
"Solve this step-by-step. Take your time and show all work.
Problem: A train leaves Station A..."
(Encourages longer reasoning chains)
```

---

## Quick Diagnostic Checklist

**Model seems to hallucinate facts?**
- [ ] Use RAG to ground in real documents
- [ ] Reduce temperature (make it more deterministic)
- [ ] Add "Cite your sources" instruction

**Model is slow?**
- [ ] Switch to smaller model
- [ ] Use quantization (8-bit, 4-bit)
- [ ] Reduce context window

**Model refuses reasonable requests?**
- [ ] Check system prompt - is it overly restrictive?
- [ ] Try slightly different phrasing
- [ ] Consider if refusal is appropriate (e.g., for security-sensitive tasks)

**Tool use doesn't work?**
- [ ] Check tool schema is valid JSON
- [ ] Verify tool description is clear
- [ ] Test with simpler task first
- [ ] Check agent loop is handling responses correctly

**Fine-tuning isn't improving?**
- [ ] Check data quality (garbage in = garbage out)
- [ ] Increase data size (try 1K+ examples)
- [ ] Lower learning rate
- [ ] Reduce training epochs (prevent overfitting)

---

## Key Takeaways

1. **LLMs are pattern machines**: Trained on next-token prediction, emerge with broad knowledge
2. **Transformers are the tech**: Self-attention lets every token relate to every other in parallel
3. **Scaling works**: Bigger models on more data = predictably better performance
4. **Reasoning is now real**: o1/o3-style models genuinely think longer for hard problems
5. **Agentic AI is the direction**: LLMs coordinating tools and other agents
6. **Security is an arms race**: Multiple defenses needed; no single silver bullet
7. **Multimodality is standard**: Vision, audio, text, video all use the same architecture
8. **Alignment matters**: How the model is trained affects behavior more than we initially thought
