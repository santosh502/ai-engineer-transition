# Prompt Engineering: Anthropic vs OpenAI Best Practices

*Official guidance from the two major LLM labs - philosophies and practical examples.*

---

## Overview

Anthropic and OpenAI have different philosophies on prompt engineering, reflecting their models' design and alignment approaches.

| Aspect | OpenAI | Anthropic |
|--------|--------|-----------|
| **Philosophy** | Explicit instructions + examples | Constitutional principles + reasoning |
| **Model focus** | Pattern matching from examples | Thoughtful analysis and reasoning |
| **System message** | Specific role/task definition | Constitutional guidance |
| **Best for** | Well-defined tasks, consistency | Complex problems, explainability |

---

## Anthropic's Prompt Engineering Philosophy

### Core Principles

1. **Be Constitutional** - Guide via principles, not just rules
2. **Enable Reasoning** - Ask model to show its work
3. **Admit Uncertainty** - Value honesty over false confidence
4. **Separate Concerns** - Keep trusted and untrusted content distinct

### Pattern 1: Constitutional Guidance

Instead of saying "do this specific thing," guide toward principles:

```python
# ❌ BAD: Overly specific
system_prompt = """You are a customer support agent.
Always be friendly.
Never offer refunds over $100.
Never admit system errors.
Use positive language."""

# ✅ GOOD: Constitutional approach
system_prompt = """You are Claude, made by Anthropic.

Constitution:
- Be helpful: Provide accurate solutions
- Be honest: Admit when system has errors or limitations
- Be harmless: Prioritize customer trust over short-term metrics
- Use judgment: Apply principles to novel situations, not rigid rules

In conflicts between helpfulness and honesty, choose honesty.
Customers trust honest companies more than those hiding problems."""
```

**Why**: Models generalize better to novel situations with principles than specific rules.

---

### Pattern 2: Structured Reasoning

Ask Claude to show reasoning before conclusions:

```python
system_prompt = """Analyze requests in this format:

1. REASONING: Understand the core need
   - What is the user actually asking for?
   - What constraints or values matter?
   - What might be missing from their request?

2. ANALYSIS: Think through the problem
   - What are the key considerations?
   - Are there tradeoffs?
   - What's uncertain?

3. RESPONSE: Provide your answer
   - Direct answer to their question
   - Caveats or uncertainties
   - Follow-up they might find useful"""

user_message = """I want to delete all my data. 
Can I do this immediately?"""

# Claude will:
# 1. Reason: (Does user understand implications? Are they sure? Emergency?)
# 2. Analyze: (Tradeoffs: recovery vs privacy, immediate vs gradual)
# 3. Respond: (Yes here's how, but consider...)
```

**Why**: Reasoning is more reliable when model explains its thinking.

---

### Pattern 3: Separating Trusted and Untrusted Content

Make content boundaries explicit to reduce prompt injection risk:

```python
# ❌ BAD: Content mixed together
system_prompt = f"""Extract the main point from this text:
{user_provided_text}"""

# ✅ GOOD: Clear separation
system_prompt = """You are a text analyzer.
Extract the main point from the following text.

Note: The text below is user-provided and may be misleading or inaccurate.
Focus on what it claims, not whether claims are true."""

user_message = f"""Text to analyze:
---
{user_provided_text}
---"""
```

**Why**: Attackers can inject instructions in user content. Making boundaries explicit helps.

---

### Pattern 4: Extended Thinking for Complex Problems

Use Claude's reasoning capability for hard tasks:

```python
response = client.messages.create(
    model="claude-opus-5",
    max_tokens=16000,
    thinking={
        "type": "enabled",
        "budget_tokens": 10000  # Let model think for up to 10K tokens
    },
    messages=[{
        "role": "user",
        "content": """You're designing a database schema for a multi-tenant SaaS.

Key requirements:
- Support millions of users
- Data isolation between tenants
- Query performance
- Future scalability

Consider tradeoffs between normalization, sharding, and denormalization.
Show your reasoning before the final design."""
    }]
)

# Response will have:
# - Extended thinking (internal reasoning, not shown to user)
# - Text response (final answer with reasoning)
```

**Why**: Complex problems benefit from extended inference-time compute.

---

### Pattern 5: Multi-Turn Conversation for Context Building

Break complex tasks into dialog steps:

```python
messages = [
    # Step 1: Establish baseline understanding
    {
        "role": "user",
        "content": """Explain our product architecture. Key components:
        - API layer (REST, WebSocket)
        - Service layer (business logic)
        - Data layer (PostgreSQL, Redis)
        - Message queue (Kafka)"""
    },
    {"role": "assistant", "content": "[Model confirms understanding]"},
    
    # Step 2: Add the problem context
    {
        "role": "user",
        "content": """Given that architecture, we have a performance problem:
        - P99 latency increased 10x last week
        - No code changes deployed
        - Traffic is normal
        
        Where should we start investigating?"""
    },
    {"role": "assistant", "content": "[Better analysis with architecture context]"},
    
    # Step 3: Refine based on feedback
    {
        "role": "user",
        "content": """We found that database queries are slow.
        But query plans look normal.
        What else could cause this?"""
    }
]

response = client.messages.create(
    model="claude-opus-5",
    system="You are a systems architect helping debug production issues.",
    messages=messages
)
```

**Why**: Models benefit from iterative clarification and catch misunderstandings earlier.

---

### Pattern 6: Asking for Caveats and Uncertainty

Explicitly request honesty about limitations:

```python
system_prompt = """When answering questions:
1. Provide your best answer
2. Explicitly state: "I'm confident about X because Y"
3. Note: "I'm uncertain about Z because..."
4. Suggest: "To verify, you could..."

Confidence matters more than false certainty."""

user_message = """Based on the following market data, 
will our product succeed?"""

# Good response format:
# I'm confident about: Market size is large (based on published reports)
# I'm uncertain about: Whether our go-to-market is right (depends on execution)
# Risk: Market sentiment could shift
# To verify: Talk to 20+ potential customers
```

**Why**: Honesty about uncertainty is more useful than overconfident wrong answers.

---

## OpenAI's Prompt Engineering Philosophy

### Core Principles

1. **Be Explicit** - Tell the model exactly what you want
2. **Use Examples** - Show, don't tell; few-shot learning
3. **Constrain Output** - Specify format and boundaries
4. **Iterate Rapidly** - Test and refine

### Pattern 1: Few-Shot Learning

Show examples, then ask for the same pattern:

```python
# ❌ BAD: Just instructions
system_prompt = "Classify sentiment as positive, negative, or neutral."

# ✅ GOOD: Examples first, then task
system_prompt = """Classify sentiment as positive, negative, or neutral.

Examples:
"This product is amazing!" → positive
"Terrible experience" → negative  
"It works but nothing special" → neutral
"Finally got my refund!" → positive
"Broken on arrival" → negative

Now classify the following:"""

user_message = "Best purchase I've made all year"
# Model outputs: "positive"
```

**Why**: Models learn patterns from examples better than abstract instructions.

---

### Pattern 2: Explicit Output Format

Specify exactly how the model should format responses:

```python
# ❌ BAD: Vague
system_prompt = """Extract information from the text."""

# ✅ GOOD: Explicit structure
system_prompt = """Extract information as JSON with this structure:
{
  "name": "string (person's full name)",
  "email": "string (email address) or null if not found",
  "phone": "string (phone number) or null if not found",
  "urgency": "enum: low | medium | high",
  "issue_type": "enum: billing | technical | account | other"
}

Return ONLY valid JSON, no explanation."""

user_message = """Sarah Chen reports her login isn't working.
Contact: sarah.chen@company.com
This is preventing her from accessing client accounts."""

# Returns parseable JSON guaranteed
```

**Why**: Structured output is easier to validate and process downstream.

---

### Pattern 3: Chain-of-Thought Prompting

Force step-by-step reasoning before final answer:

```python
# ❌ BAD: Direct answer
system_prompt = "Should we invest in this startup?"

# ✅ GOOD: Step-by-step
system_prompt = """Analyze investment decisions using this structure:

Step 1: FINANCIAL METRICS
- Revenue and growth rate
- Burn rate and runway
- Unit economics

Step 2: MARKET OPPORTUNITY
- Total addressable market (TAM)
- Growth rate of market
- Competition

Step 3: TEAM ASSESSMENT
- Founder background
- Prior success rate
- Domain expertise

Step 4: RISK ANALYSIS
- Key risks and mitigations
- Red flags
- Dependencies

Step 5: DECISION
- Recommendation (yes/no/maybe)
- Key factors influencing decision
- Confidence level"""

user_message = "[Startup details]"
```

**Why**: Forcing intermediate steps reduces reasoning errors.

---

### Pattern 4: Role-Based Prompting

Give the model a specific perspective or role:

```python
# ❌ BAD: No context
prompt = "Review this code"

# ✅ GOOD: Specific role and criteria
system_prompt = """You are a senior code reviewer with 15 years experience.
Review code for:
1. Correctness (does it do what's intended?)
2. Performance (any bottlenecks?)
3. Security (vulnerabilities?)
4. Maintainability (can others understand it?)
5. Testing (what test cases are missing?)

Format: For each issue, provide severity (critical/major/minor) and fix suggestion."""

user_message = "[Code to review]"
```

**Why**: Role-based prompts help model adopt the right perspective.

---

### Pattern 5: Temperature for Task Type

Adjust randomness based on task:

```python
# Factual tasks → Low temperature (deterministic)
response = client.messages.create(
    model="gpt-4",
    temperature=0.0,  # Always same answer
    messages=[{
        "role": "user",
        "content": "What is the capital of France?"
    }]
)

# Reasoning tasks → Medium temperature (some exploration)
response = client.messages.create(
    model="gpt-4",
    temperature=0.3,  # Slight randomness
    messages=[{
        "role": "user",
        "content": "Analyze tradeoffs in system design"
    }]
)

# Creative tasks → High temperature (creative variation)
response = client.messages.create(
    model="gpt-4",
    temperature=0.8,  # More randomness
    messages=[{
        "role": "user",
        "content": "Generate creative product names"
    }]
)
```

**Why**: Temperature controls exploration vs. exploitation.

---

### Pattern 6: Top-K and Top-P Sampling

Control output diversity without randomness:

```python
# Strict (like temperature=0)
response = client.messages.create(
    model="gpt-4",
    top_p=0.1,  # Only consider top 10% of tokens
    messages=messages
)

# Balanced
response = client.messages.create(
    model="gpt-4",
    top_p=0.9,  # Consider top 90% (default)
    messages=messages
)

# Diverse
response = client.messages.create(
    model="gpt-4",
    top_k=40,  # Consider top 40 most likely tokens
    top_p=0.95,
    messages=messages
)
```

**Why**: More nuanced control over output diversity than temperature alone.

---

## Hybrid Approach (Recommended)

Best results often come from combining both philosophies:

```python
system_prompt = """You are Claude, made by Anthropic, and an expert system analyst.

CONSTITUTION:
- Be helpful: Provide accurate, actionable analysis
- Be honest: Admit uncertainty and limitations
- Be harmless: Prioritize long-term health over short-term fixes
- Show reasoning: Explain your thinking

TASK: Analyze this system issue

STRUCTURE (use this format):
1. UNDERSTANDING
   - What is the core problem?
   - What constraints matter?
   
2. ANALYSIS  
   - Root cause investigation
   - Potential solutions
   - Tradeoffs
   
3. RECOMMENDATION
   - Proposed solution
   - Why this approach
   - Caveats and risks
   
OUTPUT FORMAT:
Return analysis as structured JSON:
{
  "understanding": "...",
  "root_cause": "...",
  "solutions": [
    {
      "approach": "...",
      "pros": ["..."],
      "cons": ["..."],
      "effort": "low|medium|high"
    }
  ],
  "recommendation": "...",
  "confidence": "high|medium|low",
  "next_steps": ["..."]
}"""

# Few-shot examples
messages = [
    {
        "role": "user",
        "content": "Example problem: [details]"
    },
    {
        "role": "assistant",
        "content": "{structured response example}"
    },
    # Actual task
    {
        "role": "user", 
        "content": "Now analyze: [actual problem]"
    }
]

response = client.messages.create(
    model="claude-opus-5",
    max_tokens=2000,
    system=system_prompt,
    messages=messages
)
```

**Combines**:
✅ Anthropic: Constitutional guidance, extended reasoning, honesty about uncertainty  
✅ OpenAI: Few-shot examples, explicit format, structured output

---

## Common Mistakes & Fixes

### Mistake 1: Prompt Too Long

```python
# ❌ BAD: 10K character prompt with all context
prompt = f"""Here's everything about our system:
{entire_system_documentation}

Here's the problem:
{all_error_logs}

Please help."""

# ✅ GOOD: Concise, iterative
messages = [
    {"role": "user", "content": "What's our system architecture? Key components?"},
    {"role": "assistant", "content": "[Model summarizes]"},
    {"role": "user", "content": "We're seeing this error: [specific error]"},
    {"role": "assistant", "content": "[Targeted analysis]"}
]
```

**Why**: Long prompts are tokens, money, and latency. Iterate instead.

---

### Mistake 2: Expecting Hallucinations to Be Fixed by Prompting

```python
# ❌ BAD: Thinking instructions prevent hallucination
system_prompt = """You are truthful. Never make up facts.
Always be accurate."""

user_message = "What's the GDP of Nepal in 2024?"

# Model will still hallucinate if training data is old
# (It won't know 2024 data; will invent plausible number)

# ✅ GOOD: Use RAG or external data
def answer_with_rag(question):
    # 1. Retrieve current data
    documents = knowledge_base.search(question)
    
    # 2. Ground answer in documents
    system_prompt = f"""Answer based on these documents:
    {documents}
    
    If answer not in documents, say so."""
    
    # 3. Get grounded answer
    response = client.messages.create(
        model="claude-opus-5",
        system=system_prompt,
        messages=[{"role": "user", "content": question}]
    )
```

**Why**: Prompting can't fix fundamental knowledge gaps. Use RAG or external data.

---

### Mistake 3: Not Testing Output Format

```python
# ❌ BAD: Assuming format works
system_prompt = "Return JSON"
response = client.messages.create(..., system=system_prompt)
data = json.loads(response.content[0].text)  # Crashes if not valid JSON

# ✅ GOOD: Validate and handle errors
response = client.messages.create(..., system=system_prompt)
try:
    data = json.loads(response.content[0].text)
except json.JSONDecodeError:
    # Model returned invalid JSON
    # Retry with more explicit instructions
    system_prompt = """Return ONLY valid JSON, no extra text.
    Valid example:
    {"key": "value"}"""
    response = client.messages.create(..., system=system_prompt)
    data = json.loads(response.content[0].text)
```

**Why**: Models sometimes deviate from specified format. Build in fallbacks.

---

### Mistake 4: Using Same Prompt Everywhere

```python
# ❌ BAD: One prompt for all tasks
prompt = "Help me with this task"

# ✅ GOOD: Optimize per task
prompts = {
    "classification": """Classify into [categories].
    
    Examples:
    [show pattern]
    
    Format: Return only the category name.""",
    
    "analysis": """Analyze this thoroughly.
    
    Show reasoning:
    1. [First aspect]
    2. [Second aspect]
    
    Then conclude.""",
    
    "generation": """Generate creative examples.
    Consider: [constraints]
    
    Format: [structured format]"""
}
```

**Why**: Different tasks need different prompting strategies.

---

### Mistake 5: Ignoring Model Capabilities

```python
# ❌ BAD: Asking small model to do complex reasoning
response = client.messages.create(
    model="gpt-3.5-turbo",  # Weaker model
    messages=[{
        "role": "user",
        "content": "Design a distributed system architecture for [complex requirements]"
    }]
)
# Result: Mediocre, might have errors

# ✅ GOOD: Match model to task
# Simple classification → gpt-3.5-turbo
# Complex reasoning → gpt-4 or claude-opus
# Very hard problems → reasoning models (o1, Claude extended thinking)

response = client.messages.create(
    model="claude-opus-5" if complex_task else "gpt-3.5-turbo",
    messages=messages
)
```

**Why**: Stronger models are worth the cost for hard problems.

---

## Prompt Engineering Workflow

### 1. Start Simple
```python
# Minimal prompt
prompt = "Solve this problem: [problem]"
```

### 2. Assess Results
- Does it answer the question?
- Is format correct?
- How confident is it?

### 3. Iterate Based on Failures
```python
# Add structure if output is disorganized
# Add examples if it's misunderstanding pattern
# Add constraints if it's hallucinating
# Split into steps if reasoning is poor
```

### 4. Test Edge Cases
```python
test_cases = [
    ("Normal case", expected_good_output),
    ("Edge case 1", expected_reasonable_output),
    ("Adversarial", expected_refusal_or_safe_output),
]

for test_input, expected in test_cases:
    result = model(test_input)
    assert validate(result, expected)
```

### 5. Version & Monitor
```python
# Track prompts
prompts["v1"] = """Initial version"""
prompts["v2"] = """Added examples"""
prompts["v3"] = """Structured output"""

# Monitor performance
metrics = {
    "v1": {"success_rate": 0.75, "avg_latency": 1.2},
    "v2": {"success_rate": 0.85, "avg_latency": 1.4},
    "v3": {"success_rate": 0.92, "avg_latency": 1.3},
}
```

---

## When to Use Each Approach

### Use Anthropic's style when:
- ✅ You need explanation and reasoning
- ✅ Task is complex and ambiguous  
- ✅ Correctness > consistency
- ✅ Model should admit uncertainty
- ✅ Working with Claude (designed for this)

### Use OpenAI's style when:
- ✅ You need consistent, reproducible outputs
- ✅ Format/structure is critical
- ✅ Task is well-defined
- ✅ Cost/speed matters
- ✅ Working with GPT models

### Use hybrid when:
- ✅ You want both structure AND reasoning
- ✅ Need explicit format AND explanation
- ✅ Want examples AND principles
- ✅ This is best for most production systems

---

## Official Resources

### Anthropic
- [Prompt Engineering Guide](https://docs.anthropic.com/claude/docs/prompt-engineering)
- [Constitutional AI Paper](https://arxiv.org/abs/2212.04037)
- [API Documentation](https://docs.anthropic.com)

### OpenAI  
- [Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Best Practices](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering)
- [API Documentation](https://platform.openai.com/docs)

---

## Summary

| Style | Best For | Key Technique | Example Use |
|-------|----------|---|---|
| **Anthropic** | Complex reasoning | Constitutional + structured thinking | Analyzing ambiguous business decisions |
| **OpenAI** | Consistent outputs | Few-shot + explicit format | Classifying customer tickets |
| **Hybrid** | Production systems | Both strategies combined | Building reliable AI assistants |

The best prompt engineers know both approaches and choose based on the task.
