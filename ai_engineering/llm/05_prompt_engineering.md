# Prompt Engineering: Anthropic vs OpenAI Best Practices

> **LLM Materials** - [Overview](README.md) | [00: Attention](00_attention_is_all_you_need.md) | [01: Fundamentals](01_llm_fundamentals.md) | [02: Examples](02_practical_examples.md) | [03: Reference](03_quick_reference.md) | [04: Hard Problems](04_hard_problems.md) | [05: Prompting](05_prompt_engineering.md)

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

## Advanced Prompting Patterns

### Pattern 1: Thought, Action, Observation Loop (TAO)

Break complex problems into iterative cycles of reasoning:

```python
system_prompt = """Solve problems using the Thought-Action-Observation loop:

1. THOUGHT: Analyze the problem
   - What's the core issue?
   - What information do I need?
   - What's my hypothesis?

2. ACTION: Take a step toward solving it
   - Execute an action (code, query, calculation)
   - Gather information
   - Test a hypothesis

3. OBSERVATION: Review the results
   - What did I learn?
   - Did it work as expected?
   - What's next?

Repeat until you solve the problem. Be explicit about each cycle."""

user_message = """Debug why our API response time increased from 100ms to 500ms.
We have access to logs, metrics, and database query info."""

# Model will iteratively:
# Thought: "Could be database, caching, or network"
# Action: "Let me check database query times"
# Observation: "Query times are normal"
# Thought: "Try looking at cache hit rates"
# ... continues until root cause found
```

**Why**: Iterative reasoning catches errors and refines understanding.

---

### Pattern 2: Tree of Thoughts (ToT)

Explore multiple reasoning paths simultaneously:

```python
system_prompt = """Use Tree of Thoughts: explore multiple solution paths.

For each problem:
1. Generate multiple hypotheses
2. Evaluate each path's promise
3. Prune unlikely branches
4. Deeply explore promising branches
5. Compare final solutions

Format your exploration:
- HYPOTHESES: [list 3-5 different approaches]
- EVALUATION: [rate each: high/medium/low promise]
- DEEP DIVE: [explore top 2 hypotheses fully]
- COMPARISON: [which is best and why]
- DECISION: [final choice with reasoning]"""

user_message = """Design a caching strategy for a microservice that handles
10M requests/day with 80% read and 20% write operations."""

# Model explores multiple approaches:
# - Redis + TTL
# - Multi-tier (memory + disk)
# - Event-based invalidation
# Evaluates tradeoffs of each, then recommends best
```

**Why**: Multiple paths catch blind spots; prevents premature optimization.

---

### Pattern 3: Directional Stimulus Prompting

Focus model on specific keywords or constraints:

```python
system_prompt = """When solving this problem, focus specifically on:
- PERFORMANCE: Response time must be <100ms
- SCALABILITY: Must handle 1000 concurrent users
- SECURITY: No sensitive data in logs
- MAINTAINABILITY: Code must be readable

Each decision should be evaluated against these keywords.
If tradeoffs exist, mention which keyword you're prioritizing."""

user_message = """Suggest how to handle file uploads in our web application."""

# Model keeps suggestions aligned with the specified keywords
# Won't suggest inefficient solutions
# Explicitly notes tradeoffs against the stated constraints
```

**Why**: Guides model toward solutions aligned with your actual constraints.

---

### Pattern 4: Iterative Refinement (Refinement Loop)

Progressively improve output through structured feedback:

```python
messages = [
    # Round 1: Generate initial solution
    {
        "role": "user",
        "content": """Design a mobile app architecture for a fitness tracker.
        Requirements: iOS + Android, offline-first, 1M users."""
    },
    {"role": "assistant", "content": "[Initial architecture]"},
    
    # Round 2: Refine with specific feedback
    {
        "role": "user",
        "content": """This is good but:
        1. Too complex - simplify the data sync layer
        2. Add privacy considerations
        3. Reduce the number of microservices from 5 to 3
        
        Refine the persona and constraints:
        - Target users: Casual fitness enthusiasts (not athletes)
        - Budget: MVP with $50K engineering budget"""
    },
    {"role": "assistant", "content": "[Refined architecture]"},
    
    # Round 3: Final polish
    {
        "role": "user",
        "content": """Perfect. Now provide:
        1. Technology stack recommendations
        2. Implementation roadmap (3 phases)
        3. Key metrics to track"""
    }
]

response = client.messages.create(
    model="claude-opus-5",
    messages=messages
)
```

**Why**: Iterative refinement converges on better solutions than single-shot.

---

## Multimodal Prompting (Vision)

### Pattern 1: Image Analysis with Context

Combine images with structured analysis requests:

```python
import anthropic
import base64

# Load and encode image
with open("architecture_diagram.png", "rb") as f:
    image_data = base64.standard_b64encode(f.read()).decode("utf-8")

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-5",
    max_tokens=2048,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": image_data,
                    },
                },
                {
                    "type": "text",
                    "text": """Analyze this architecture diagram:

1. COMPONENTS: What are the main components?
2. FLOW: How does data flow through the system?
3. BOTTLENECKS: Where could scaling issues occur?
4. IMPROVEMENTS: What would you change?

Be specific about what you see in the diagram."""
                }
            ],
        }
    ],
)
```

**Why**: Models can reason about diagrams, screenshots, and charts directly.

---

### Pattern 2: Multi-Image Comparison

Compare multiple images or analyze image sequences:

```python
response = client.messages.create(
    model="claude-opus-5",
    max_tokens=2048,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Compare these two UI mockups:"
                },
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": mockup_v1_base64,
                    },
                },
                {
                    "type": "text",
                    "text": "Version 1 (above) vs Version 2 (below):"
                },
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": mockup_v2_base64,
                    },
                },
                {
                    "type": "text",
                    "text": """Which is better for user experience?
                    Consider: clarity, accessibility, engagement."""
                }
            ],
        }
    ],
)
```

**Why**: Comparing visuals is more efficient than describing them in text.

---

## Function Calling & Tool Use

### Pattern 1: Structured Function Calls

Ask model to call functions for specific tasks:

```python
tools = [
    {
        "name": "search_database",
        "description": "Search customer database for specific records",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "SQL-like search query"
                },
                "filters": {
                    "type": "object",
                    "description": "Additional filters (date_range, status, etc)"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "update_record",
        "description": "Update a customer record with new information",
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_id": {"type": "string"},
                "updates": {"type": "object"}
            },
            "required": ["customer_id", "updates"]
        }
    }
]

response = client.messages.create(
    model="claude-opus-5",
    max_tokens=1024,
    tools=tools,
    messages=[
        {
            "role": "user",
            "content": """Find all customers who purchased in the last 30 days
            and update their loyalty status to 'premium'."""
        }
    ]
)

# Model will call:
# 1. search_database with query for last 30 days
# 2. update_record for each customer found
```

**Why**: Models can invoke tools accurately when structure is clear.

---

### Pattern 2: Tool Use with Error Handling

Handle tool failures and retries gracefully:

```python
def run_tool(tool_name, tool_input):
    """Execute a tool and handle errors"""
    try:
        if tool_name == "search_database":
            return database.search(**tool_input)
        elif tool_name == "update_record":
            return database.update(**tool_input)
    except Exception as e:
        return {"error": str(e), "status": "failed"}

# Agentic loop with tool use
messages = [
    {
        "role": "user",
        "content": "Find customers in NYC and upgrade their accounts"
    }
]

while True:
    response = client.messages.create(
        model="claude-opus-5",
        max_tokens=1024,
        tools=tools,
        messages=messages
    )
    
    # Check if model wants to use a tool
    if response.stop_reason == "tool_use":
        tool_results = []
        for content_block in response.content:
            if content_block.type == "tool_use":
                tool_result = run_tool(
                    content_block.name,
                    content_block.input
                )
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": content_block.id,
                    "content": str(tool_result)
                })
        
        # Add tool results to messages
        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})
    else:
        # Model finished without tools
        break

print(response.content[0].text)
```

**Why**: Agentic loops let models solve complex tasks step-by-step.

---

## Prompt Caching Strategy

### Pattern 1: Cache Large Context

Cache expensive context that's reused across requests:

```python
# For Anthropic API with prompt caching
response = client.messages.create(
    model="claude-opus-5",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": """You are an expert code reviewer."""
        },
        {
            "type": "text",
            "text": """## Company Code Standards
[100+ lines of detailed guidelines]
[These are reused across many requests]""",
            "cache_control": {"type": "ephemeral"}  # Cache this block
        }
    ],
    messages=[
        {
            "type": "user",
            "content": """Review this code:
            [User's specific code to review]"""
        }
    ]
)

# First request: pays full cost + cache write
# Subsequent requests: cache hit = 10% of cache cost + input cost
# (Cache reduces cost significantly for heavy reuse)
```

**Why**: Caching reduces costs 90% for repeated context (guidelines, documentation).

---

### Pattern 2: Multi-Turn Conversation Caching

Cache conversation history for long discussions:

```python
messages = [
    # These build up and can be cached
    {"role": "user", "content": "Explain our system architecture"},
    {"role": "assistant", "content": "[Long explanation]"},
    
    {"role": "user", "content": "Show the database layer details"},
    {"role": "assistant", "content": "[Database explanation]"},
]

# After several turns, cache the conversation
# New requests with this history are cheaper

response = client.messages.create(
    model="claude-opus-5",
    max_tokens=1024,
    system=[{
        "type": "text",
        "text": "You are a system architect",
        "cache_control": {"type": "ephemeral"}
    }],
    messages=messages  # This history gets cached after sufficient tokens
)
```

**Why**: Long conversations save 90% cost on subsequent requests.

---

## Token Counting & Optimization

### Pattern 1: Token Budget Planning

Plan tokens before making API calls:

```python
import anthropic

client = anthropic.Anthropic()

# Estimate tokens before calling API
def estimate_cost(system_prompt, messages, model="claude-opus-5"):
    """Estimate tokens and cost before making request"""
    
    # Use token counting API
    response = client.messages.count_tokens(
        model=model,
        system=system_prompt,
        messages=messages
    )
    
    input_tokens = response.input_tokens
    
    # Estimate output (rough: 1.3x the expected response length)
    estimated_output_tokens = 1500  # For example
    
    # Pricing (example rates)
    pricing = {
        "claude-opus-5": {"input": 0.003, "output": 0.015},  # per 1K tokens
        "claude-sonnet-5": {"input": 0.003, "output": 0.015},
        "claude-haiku-4-5": {"input": 0.00080, "output": 0.004},
    }
    
    rates = pricing.get(model, pricing["claude-opus-5"])
    
    estimated_cost = (
        (input_tokens / 1000) * rates["input"] +
        (estimated_output_tokens / 1000) * rates["output"]
    )
    
    return {
        "input_tokens": input_tokens,
        "estimated_output_tokens": estimated_output_tokens,
        "estimated_cost": estimated_cost
    }

# Before making expensive calls
estimates = estimate_cost(system_prompt, messages)
print(f"Estimated cost: ${estimates['estimated_cost']:.4f}")

if estimates['estimated_cost'] > budget_per_request:
    # Reduce context or use cheaper model
    model = "claude-haiku-4-5"  # Cheaper alternative
```

**Why**: Avoid surprise costs; choose right model for task complexity.

---

### Pattern 2: Context Optimization

Reduce tokens without losing quality:

```python
# ❌ BAD: Include everything
system_prompt = f"""
[Full 50K character documentation]
[All code examples]
[Complete error logs]
[Historical context]
"""

# ✅ GOOD: Iterative, minimal context
messages = [
    {
        "role": "user",
        "content": """What's our main service doing? 
        Key components: API (REST), DB (PostgreSQL), Cache (Redis)"""
    },
    {"role": "assistant", "content": "[Model summarizes understanding]"},
    
    {
        "role": "user",
        "content": """We're seeing 500ms latency spikes. 
        Error: query timeout in user_service.
        Today's traffic: normal. 
        Last change: 3 days ago, cache update."""
    },
    {
        "role": "assistant",
        "content": "[Targeted analysis based on context]"
    }
]

# Saves 70% of tokens vs dumping all context at once
```

**Why**: Iterative context is cheaper and often better quality.

---

### Pattern 3: Token Limit Strategy

Set appropriate max_tokens for different tasks:

```python
def create_response(user_input, task_type):
    """Set max_tokens based on task type"""
    
    token_budgets = {
        "classification": 100,      # "Yes/No" or category
        "extraction": 500,          # Extract structured info
        "analysis": 1000,           # Detailed breakdown
        "generation": 2000,         # Code, essays, long content
        "reasoning": 4000,          # Complex problem solving
        "extended_thinking": 16000  # Very hard problems
    }
    
    max_tokens = token_budgets.get(task_type, 1000)
    
    response = client.messages.create(
        model="claude-opus-5",
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": user_input}]
    )
    
    return response

# Right-sized max_tokens = faster, cheaper responses
create_response("Is this sentiment positive?", "classification")  # 100 tokens max
create_response("Design a database", "reasoning")                 # 4000 tokens max
```

**Why**: Over-generous max_tokens increases latency and cost needlessly.

---

## Testing & Evaluation

### Pattern 1: Structured Test Cases

Build comprehensive test suites:

```python
test_cases = [
    {
        "name": "happy_path",
        "input": "Normal user request",
        "expected_characteristics": {
            "format": "json",
            "contains_reasoning": True,
            "confidence_level": ["high", "medium", "low"]
        },
        "should_succeed": True
    },
    {
        "name": "edge_case_missing_data",
        "input": "Request with incomplete information",
        "expected_characteristics": {
            "mentions_missing_info": True,
            "offers_alternatives": True,
            "asks_clarifying_questions": True
        },
        "should_succeed": True
    },
    {
        "name": "adversarial_instruction_injection",
        "input": 'User text containing "ignore previous instructions"',
        "expected_characteristics": {
            "follows_original_instructions": True,
            "does_not_follow_injection": True,
            "might_mention_injection_attempt": True
        },
        "should_succeed": True
    }
]

def run_tests(prompt, test_cases):
    """Run all tests against a prompt"""
    results = []
    
    for test in test_cases:
        response = client.messages.create(
            model="claude-opus-5",
            system=prompt,
            messages=[{"role": "user", "content": test["input"]}]
        )
        
        # Validate response matches expectations
        output = response.content[0].text
        
        result = {
            "test_name": test["name"],
            "passed": validate_output(output, test["expected_characteristics"]),
            "output": output
        }
        results.append(result)
    
    return results

# Run against current prompt
results = run_tests(system_prompt, test_cases)
pass_rate = sum(1 for r in results if r["passed"]) / len(results)
print(f"Pass rate: {pass_rate:.0%}")
```

**Why**: Automated tests catch regressions as you iterate.

---

### Pattern 2: Evaluation Metrics

Track quality across versions:

```python
def evaluate_prompt_version(prompt_version, test_set, num_samples=100):
    """Evaluate prompt quality comprehensively"""
    
    metrics = {
        "success_rate": 0,          # % of valid responses
        "format_correctness": 0,    # % with correct format
        "speed": 0,                 # Avg latency in seconds
        "cost_per_request": 0,      # $ per request
        "user_satisfaction": 0,     # If you have feedback
        "hallucination_rate": 0,    # % with false info
        "reasoning_quality": 0      # How well explained
    }
    
    latencies = []
    costs = []
    successes = 0
    
    for i in range(num_samples):
        test_input = test_set[i]
        start_time = time.time()
        
        response = client.messages.create(
            model="claude-opus-5",
            max_tokens=1000,
            system=prompt_version,
            messages=[{"role": "user", "content": test_input}]
        )
        
        latency = time.time() - start_time
        latencies.append(latency)
        
        # Estimate cost (simplified)
        cost = (response.usage.input_tokens + response.usage.output_tokens) / 1000 * 0.0045
        costs.append(cost)
        
        # Validate response
        if validate_response(response.content[0].text):
            successes += 1
    
    metrics["success_rate"] = successes / num_samples
    metrics["speed"] = sum(latencies) / len(latencies)
    metrics["cost_per_request"] = sum(costs) / len(costs)
    
    return metrics

# Compare versions
v1_metrics = evaluate_prompt_version(prompt_v1, test_set)
v2_metrics = evaluate_prompt_version(prompt_v2, test_set)

print(f"V1 Success: {v1_metrics['success_rate']:.0%}, Cost: ${v1_metrics['cost_per_request']:.4f}")
print(f"V2 Success: {v2_metrics['success_rate']:.0%}, Cost: ${v2_metrics['cost_per_request']:.4f}")
```

**Why**: Metrics show whether improvements are real or just perceived.

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

### Mistake 6: No Error Handling or Fallback Strategy

```python
# ❌ BAD: Single attempt, crashes on failure
def ask_model(question):
    response = client.messages.create(
        model="claude-opus-5",
        messages=[{"role": "user", "content": question}]
    )
    return json.loads(response.content[0].text)

# If model returns invalid JSON, script crashes

# ✅ GOOD: Retry with degradation
def ask_model_with_fallback(question, max_retries=3):
    """Try to get valid response, with fallbacks"""
    
    for attempt in range(max_retries):
        try:
            # Try with strong model first
            response = client.messages.create(
                model="claude-opus-5",
                temperature=0.0,  # Deterministic for validation
                max_tokens=1000,
                messages=[{"role": "user", "content": question}]
            )
            
            # Validate response format
            data = json.loads(response.content[0].text)
            return {"success": True, "data": data}
            
        except json.JSONDecodeError:
            if attempt == max_retries - 1:
                # Last attempt: use simpler model with explicit format
                response = client.messages.create(
                    model="claude-haiku-4-5",  # Cheaper, deterministic
                    system="Return ONLY valid JSON. No other text.",
                    max_tokens=500,
                    messages=[{"role": "user", "content": question}]
                )
                try:
                    data = json.loads(response.content[0].text)
                    return {"success": True, "data": data}
                except:
                    return {"success": False, "error": "Failed after retries"}
        
        except anthropic.APIError as e:
            if attempt < max_retries - 1:
                wait_time = (2 ** attempt)  # Exponential backoff
                time.sleep(wait_time)
                continue
            else:
                return {"success": False, "error": str(e)}
    
    return {"success": False, "error": "Unknown error"}

# Usage with graceful degradation
result = ask_model_with_fallback("Complex reasoning task")
if result["success"]:
    process_data(result["data"])
else:
    handle_failure(result["error"])
```

**Why**: Production systems need graceful degradation and retry strategies.

---

### Mistake 7: Ignoring Rate Limits and Quota Management

```python
# ❌ BAD: No rate limit handling
for item in items:
    response = client.messages.create(...)  # Crashes on rate limit

# ✅ GOOD: Respect rate limits
import time
from collections import deque

class RateLimitedClient:
    def __init__(self, requests_per_minute=60):
        self.rpm = requests_per_minute
        self.request_times = deque()
    
    def wait_if_needed(self):
        """Ensure we don't exceed rate limit"""
        now = time.time()
        
        # Remove old requests outside the window
        while self.request_times and self.request_times[0] < now - 60:
            self.request_times.popleft()
        
        # If at limit, wait
        if len(self.request_times) >= self.rpm:
            wait_time = 60 - (now - self.request_times[0])
            if wait_time > 0:
                time.sleep(wait_time)
    
    def create_message(self, **kwargs):
        """API call with rate limiting"""
        self.wait_if_needed()
        response = client.messages.create(**kwargs)
        self.request_times.append(time.time())
        return response

# Usage
client = RateLimitedClient(requests_per_minute=10)
for item in items:
    response = client.create_message(...)  # Won't exceed rate limit
```

**Why**: Rate limits are real constraints; plan for them.

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

## Quick Reference: Which Pattern to Use

| Situation | Best Pattern | Why |
|-----------|--------------|-----|
| **Need reasoning about complex decision** | Thought-Action-Observation or Extended Thinking | Iterative refinement catches errors |
| **Exploring multiple solution paths** | Tree of Thoughts | Avoids premature optimization |
| **Have specific constraints (performance, security)** | Directional Stimulus | Keeps solutions aligned |
| **Analyzing images or diagrams** | Multimodal Prompting | Direct visual reasoning |
| **Need deterministic API calls** | Function Calling | Structured, reliable automation |
| **Have expensive, reused context** | Prompt Caching | 90% cost reduction |
| **Working with large amounts of data** | Multi-turn Conversation | Cheaper than dumping all context |
| **Need to optimize spending** | Token Counting + Right-sized max_tokens | Avoid surprise costs |
| **Building production system** | Hybrid Approach + Testing + Error Handling | Reliable, measurable quality |

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

### Use advanced patterns when:
- ✅ **TAO (Thought-Action-Observation)**: Debugging, iterative problem-solving
- ✅ **Tree of Thoughts**: Complex decisions, exploring multiple paths
- ✅ **Directional Stimulus**: Tasks with specific constraints
- ✅ **Iterative Refinement**: Building toward a specific vision
- ✅ **Multimodal**: Analyzing images, diagrams, charts
- ✅ **Function Calling**: Automating multi-step tasks with tools
- ✅ **Caching**: Reusing expensive context across requests
- ✅ **Token Optimization**: Cost-sensitive applications
- ✅ **Testing & Evaluation**: Production systems, quality tracking

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

## Complete Pattern Summary

| Pattern | Best For | Complexity | Cost | Example |
|---------|----------|-----------|------|---------|
| **Constitutional Guidance** | Values-driven responses | Low | Low | Customer support with principles |
| **Structured Reasoning** | Clear thinking | Medium | Medium | Code review, analysis |
| **Separated Content** | Prompt injection safety | Low | Low | User input processing |
| **Extended Thinking** | Complex problems | High | High | System architecture design |
| **Multi-Turn Dialog** | Context building | Medium | Medium | Debugging sessions |
| **Few-Shot Learning** | Pattern recognition | Medium | Low | Sentiment classification |
| **Explicit Format** | Structured data | Low | Low | Extract info to JSON |
| **Chain-of-Thought** | Step-by-step reasoning | Medium | Medium | Investment analysis |
| **Role-Based** | Perspective adoption | Low | Low | Code review as expert |
| **TAO Loop** | Iterative debugging | High | High | Root cause analysis |
| **Tree of Thoughts** | Multi-path exploration | Very High | Very High | Complex decisions |
| **Directional Stimulus** | Constraint alignment | Medium | Low | Feature design |
| **Iterative Refinement** | Progressive improvement | High | High | Architecture design |
| **Multimodal** | Visual reasoning | Medium | Medium | Diagram analysis |
| **Function Calling** | Tool automation | Medium | Medium | Database queries |
| **Prompt Caching** | Cost optimization | Low | Very Low | Repeated context |
| **Token Optimization** | Budget management | Low | Low | Cost tracking |
| **Testing & Eval** | Quality assurance | High | Medium | Production monitoring |

---

## Implementation Strategy

1. **Start simple**: Constitutional guidance + few-shot examples
2. **Add structure**: Explicit format + clear examples
3. **Iterate on failures**: Add caching, optimization, testing
4. **For complex tasks**: Use advanced patterns (TAO, ToT, extended thinking)
5. **Monitor**: Track metrics, costs, latency continuously

The best prompt engineers combine multiple patterns strategically, not using all at once, but selecting based on task requirements and constraints.
