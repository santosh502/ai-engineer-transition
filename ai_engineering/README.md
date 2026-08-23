# AI Engineering Learning Path

A practical guide to understanding Large Language Models-how they actually work, how to build with them, and what matters in 2026.

## Directory Structure

```
ai_engineering/
├── llm/                    # How LLMs work
│   ├── llm_fundamentals.md    # Core concepts, explained
│   ├── practical_examples.md  # Code you can run
│   └── quick_reference.md     # Lookup when you need it
├── rag/                    # Retrieval-Augmented Generation
│   └── README.md          # WIP
├── agentic/               # AI Agents & Multi-Agent Systems
│   └── README.md          # WIP
└── README.md              # This file
```

## Getting Started

**Just starting out?**
1. Read [LLM Fundamentals](llm/llm_fundamentals.md) first-it covers what LLMs actually are, not the hype version
2. Keep the [Quick Reference](llm/quick_reference.md) nearby for terms and decision trees
3. Work through [Practical Examples](llm/practical_examples.md) to see it in action

**Already comfortable with the basics?**
1. Dig into Transformer architecture and why self-attention works
2. Play with fine-tuning in practical_examples.md
3. Build something real: a RAG system or a simple agent

**Deep into it?**
1. Understand scaling laws and what they predict about future models
2. Read about reasoning models and test-time compute (o1, DeepSeek-R1)
3. Build multi-agent systems that compose tools together
4. Learn security hardening-prompt injection, jailbreaks, alignment challenges

## What's Here

### Large Language Models (LLM)
What you'll learn: the architecture, how training actually works, why scaling matters, and how to think about reasoning models vs standard inference.
- What is an LLM really? (it's weights + inference code)
- Transformer architecture and why self-attention changed everything
- Training pipeline: pretraining → fine-tuning → alignment
- Scaling laws and what they tell us about future models
- Reasoning models and test-time compute (o1, DeepSeek-R1)
- Multimodal models (vision, audio, text in one)
- Security challenges (jailbreaks, prompt injection, alignment)

### Retrieval-Augmented Generation (RAG)
In progress-covering vector embeddings, semantic search, how to wire up a RAG pipeline, and which databases work where.

### Agentic AI
Coming soon-how agents think, tool use, multi-agent coordination, and building systems that can reason over multiple steps.

## Key Concepts At a Glance

| Concept | Why It Matters | Learn More |
|---------|---|---|
| **Transformers** | The architecture behind every major LLM | llm/llm_fundamentals.md §2 |
| **Self-Attention** | Lets tokens understand context from all positions | llm/llm_fundamentals.md §2 |
| **Scaling Laws** | Bigger model + more data = predictably better | llm/llm_fundamentals.md §4 |
| **Fine-tuning** | Customize models for specific domains/tasks | llm/practical_examples.md §4 |
| **RAG** | Ground LLM answers in real documents | rag/README.md |
| **Agents** | LLMs coordinating tools for autonomous action | agentic/README.md |
| **Reasoning Models** | "Think longer" for harder problems | llm/llm_fundamentals.md §5 |
| **Multimodality** | LLMs understanding vision, audio, text | llm/llm_fundamentals.md §7 |
| **Security** | Jailbreaks, injection, alignment challenges | llm/llm_fundamentals.md §8 |

## Tools & Platforms

**Running models locally**
- Ollama (easiest way to run Llama, Mistral, etc. on your machine)
- Hugging Face (model hub + inference, lots of community support)
- LM Studio (if you want a GUI)

**Via API**
- Anthropic (Claude)
- OpenAI (GPT)
- Together.ai (if you want to experiment with open-source models at scale)
- Replicate (serverless inference for anything)

**Building with agents**
- LangChain (lots of examples, very popular)
- LlamaIndex (great for RAG specifically)
- Claude SDK (Python/TypeScript, works directly with Anthropic API)

## What You'll Be Able to Do

After working through this, you'll understand:
- How LLMs actually work (not the simplified version)
- Why transformers and attention work, and when alternatives might matter
- What happens during training and why it matters for your use case
- How to pick the right model for a problem (or build your own)
- When to fine-tune vs. RAG vs. just use a bigger model
- How to build systems that use tools and can reason across multiple steps
- What can go wrong in LLM systems and how to defend against it  

## Quick Decision Trees

**Picking a model?**
- Need to run it on your laptop? → Llama 2, Mistral, or DeepSeek (7B-70B)
- Running via API is fine? → Claude, GPT, Gemini
- Need math or hard reasoning? → DeepSeek-R1, o1, or Claude w/ extended thinking
- Need vision? → GPT-4o, Claude 3.5 Sonnet, or Gemini 2.0

**Fine-tuning worth it?**
- Have 1K+ examples in your domain? → Probably yes
- Less than that? → Try RAG first, it's usually cheaper
- Cost per inference is critical? → Fine-tune a smaller model
- Otherwise? → Start with a big model + RAG, fine-tune later if needed

**RAG vs. fine-tuning?**
- Data changes all the time? → RAG (update without retraining)
- Data is stable? → Fine-tuning (faster at inference)
- Need to cite sources? → RAG is natural for that
- Unsure? → RAG first, then fine-tune if it's not working

## Resources

**Papers that actually matter**
- "Attention Is All You Need" (Vaswani et al., 2017)-read this if you're serious
- "Scaling Laws for Neural Language Models" (Hoffmann et al.)-understanding scaling
- "Language Models are Unsupervised Multitask Learners" (GPT-2 paper)-foundational

**Talks**
- Andrej Karpathy's "Intro to LLMs" (very clear, very good)
- Jeremy Howard's deep learning course

**Communities**
- Hugging Face forums (lots of practitioners)
- r/MachineLearning (Reddit)
- Anthropic Discord
- OpenAI community

### Papers (Foundational)
- "Attention Is All You Need" (Vaswani et al., 2017)
- "Language Models are Unsupervised Multitask Learners" (Radford et al., GPT-2)
- "Scaling Laws for Neural Language Models" (Hoffmann et al., Chinchilla)

### Talks
- Andrej Karpathy: "Intro to LLMs" (referenced extensively)
- Jeremy Howard: "A Practical Deep Learning for Coders" (courses)

### Communities
- Hugging Face Discuss
- r/MachineLearning
- Anthropic Discord
- OpenAI Community Forum

## Contributing

As you learn, add to this. Things worth documenting:
- Architecture tricks that actually work (Flash Attention, GQA, MQA-whatever you find useful)
- Frameworks or tools you've tried and what you actually think of them
- Things that broke in production and what you learned
- Security surprises or incidents and how to avoid them
- Papers or talks that changed how you think about this stuff
