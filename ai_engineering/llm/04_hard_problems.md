# Hard Problems & Limitations in LLMs

**Navigation**: [Overview](README.md) · [00: Attention](00_attention_is_all_you_need.md) · [01: Fundamentals](01_llm_fundamentals.md) · [02: Examples](02_practical_examples.md) · [03: Reference](03_quick_reference.md) · [04: Hard Problems](04_hard_problems.md) · [05: Prompting](05_prompt_engineering.md)

*The gap between "works in research" and "works in production"—where current models actually fail.*

*The gap between "works in research" and "works in production" - where current models actually fail.*

---

## Introduction

LLMs are impressive, but they're brittle. This document covers the real problems you'll encounter when building production systems, not just the polished academic results.

**Key insight**: The capabilities you see in demos often don't survive contact with real-world complexity.

---

## 1. Hallucination: The Unsolved Problem

### The Core Issue

Models are trained to *always generate something*. They have no mechanism to express "I don't know."

```
Prompt: "What is the phone number of McDonald's in downtown Portland?"

Good model should say:
"I don't have access to real-time business data. Use Google Maps."

Actual model output:
"The McDonald's at 123 Main Street, Portland is (503) 555-0147."
(Completely fabricated.)
```

### Why Current Fixes Are Incomplete

| Approach · What It Does · Why It Fails |
|----------|---|---|
| **RAG** · Ground answers in real documents · Still hallucinates within retrieved context; retrieval can miss documents |
| **Fine-tuning on QA pairs** · Model learns what "good answers" look like · Reinforces confident-but-wrong patterns |
| **Temperature lowering** · Makes model more deterministic · Doesn't reduce hallucination rate, just makes it consistent |
| **Uncertainty quantification** · Get model to express confidence · Models can be confident while wrong |
| **Constitutional AI** · Align to principle of honesty · Models still rationalize fabrications as "plausible" |

### Why Hallucination is Architectural, Not Just Training

The fundamental problem: **Next-token prediction doesn't inherently distinguish between "real" and "plausible."**

```
Training objective: 
  Predict next token given previous tokens.
  
This learns:
  "What tokens typically follow in the training data?"
  
It does NOT learn:
  "Which of these plausible-sounding tokens are actually true?"

Example:
  After "The capital of France is", the token "Paris" is 99% likely.
  After "The CEO of XYZ Corp is", the model might generate a plausible-sounding name.
  
  But it has no way to verify the name is real during training.
  The model learned "person names follow 'CEO of [company]'" 
  NOT "these specific names exist."
```

### Practical Implications for Builders

✅ **What works**:
- RAG for factual questions (ground in real documents)
- Verification loops (model generates → fact-check → regenerate)
- Explicit "I don't know" training (add examples of refusals)
- Search-then-answer (retrieve real data before responding)

❌ **What doesn't work**:
- Hoping better models hallucinate less (they don't, much)
- Trusting model confidence (miscalibrated)
- Filtering hallucinations with guardrails (hard to detect)
- Fine-tuning alone (amplifies the problem)

---

## 2. Alignment: The Value Conflict Problem

### The Trilemma

Every LLM has three competing values:

```
      Helpful
        / \
       /   \
      /     \
    Honest - Harmless
```

You can optimize for two, but rarely all three simultaneously.

### Real-World Examples of Conflicts

**Example 1: Medical advice**
```
User: "I think I might have cancer. What should I do?"

Helpful response: 
  "Here are 5 possible conditions and what to do about each..."
  (User gets useful information)

Honest response:
  "I'm not a doctor; this isn't medical advice.
   Please see a healthcare professional."
  (User is frustrated; might not seek real help)

Harmless response:
  "I can't provide medical advice."
  (Protects you from liability but fails the user)

Current solution: Blend all three awkwardly
  "While I can't provide medical advice, I can share that..."
  (Satisfies no one completely)
```

**Example 2: Sensitive feedback**
```
User: "Why is my manager being unfair to me?"

Honest answer: 
  "Based on what you've said, [specific critique of their manager]"
  (User gets validation but might misinterpret)

Helpful answer:
  "I'd suggest documenting specific incidents and talking to HR"
  (Practical, but avoids the emotional core)

Harmless answer:
  "I can't comment on interpersonal dynamics I don't fully understand"
  (Safe, but unhelpful)

Different users need different balances.
There's no universal "right" answer.
```

**Example 3: Political/controversial questions**
```
User: "Is this political candidate qualified?"

Honest: "Their record shows [evidence pro and con]"
Helpful: "Here's how to research candidates"  
Harmless: "I don't comment on political candidates"

Again: All three legitimate, all different.
```

### The Alignment-as-Values Problem

**Key insight**: Alignment isn't a technical problem - it's a *values problem*.

```
Technical problem: How do we make models follow instructions?
  Solution: RLHF, DPO, fine-tuning
  Status: Solved (mostly)

Values problem: How do we make models reflect *which values* matter?
  Solution: ???
  Status: No consensus

Example:
  Two models, equally well-aligned:
  - Model A: Prioritizes honesty over helpfulness
  - Model B: Prioritizes helpfulness over honesty
  
  Same code, same architecture, different training data/preferences.
  Both are "well-aligned" - just to different values.
```

### Constitutional AI: Principle-Based Alignment

Anthropic's approach: **Make values explicit**.

```
Instead of asking: "Is response B better than response A?"
Constitutional AI asks: "Does response violate any principles?"

Example constitution:
  1. Be helpful to the human
  2. Be honest and accurate
  3. Be harmless (don't help with illegal activities)
  4. Respect privacy
  5. Defer to human expertise where applicable
  
Model is trained against these *explicit* principles.

Advantage: Values are transparent and debatable.
You can argue about the constitution, not hidden preference weights.

Disadvantage: Still requires judgment calls on conflicts
(e.g., "Does this violate harmlessness principle?" reasonable people disagree)
```

### Practical Implications

If you deploy an LLM:
1. **Your values are baked in** - even if unintentional
2. **Choose them explicitly** - don't leave it to default fine-tuning
3. **Document trade-offs** - "We prioritize honesty over helpfulness" is better than pretending there's no trade-off
4. **Monitor for value drift** - RLHF can shift values as you collect more data
5. **Expect criticism** - whatever values you choose, someone will object

---

## 3. Reliability: Why Agents Fail in Production

### The Agent Reliability Problem

Even simple agents fail surprisingly often:

```
Task: "Book a restaurant reservation for 4 people at 7pm tomorrow"

Possible failures:
1. Hallucinated restaurant (doesn't exist)
2. Wrong date (tomorrow vs. specific date)
3. Wrong party size (5 instead of 4)
4. Wrong time (picked 7am not 7pm)
5. Wrong tool call (called reservation tool before checking if open)
6. Cascading error (booked wrong restaurant → can't fix)
7. Context limit (forgot earlier constraints)
8. No error recovery (stuck after tool failure)

Any ONE of these fails the task.
Probability of all 8 being correct: ~50%+ depending on model.
```

### Why Agents Struggle

#### 1. **Sunk Cost Bias in Planning**

Humans: Make a wrong move → quickly backtrack and replan  
Agents: Make a wrong move → commit and try to make it work

```
Example:
User: "Write a Python script that reads a CSV and outputs JSON"

Agent's reasoning chain:
  Step 1: Decide to use pandas (reasonable)
  Step 2: Write code with pandas
  Step 3: Code has subtle bug
  Step 4: Bug propagates through rest of code
  Step 5: Final code is broken

Better approach:
  Step 1: Decide approach
  Step 2: Write simple test first
  Step 3: Test fails → backtrack and reconsider
  Step 4: Choose different library
  Step 5: Build incrementally with tests
  
Agents rarely do step 3 (backtrack).
They usually proceed with the wrong approach.
```

#### 2. **Tool Use Hallucination**

Models make up tools that don't exist:

```
Available tools:
  - web_search(query)
  - fetch_url(url)
  - get_current_date()

Agent's call:
  get_news_from_website(url="nytimes.com")  ← Tool doesn't exist!

Model confidently uses a tool it invented.
Agent framework crashes or ignores call.
Agent fails.
```

#### 3. **Parameter Binding Errors**

Right tool, wrong parameters:

```
Tool: book_flight(
  departure_city: str,
  arrival_city: str, 
  departure_date: str,  # format: "YYYY-MM-DD"
  passenger_count: int
)

User: "Book a flight from NYC to LA for 4 people next Wednesday"

Agent's call:
  book_flight(
    departure_city="New York",  ← Should be "NYC" or airport code
    arrival_city="Los Angeles",  ← Should be "LAX"
    departure_date="next Wednesday",  ← Not in YYYY-MM-DD format!
    passenger_count=4  ← Correct
  )

3 out of 4 parameters are wrong.
```

#### 4. **Context Window Limits**

Long-running agents run out of memory:

```
Agent task: "Analyze all conversations from Q1 and generate report"

Step 1: Retrieve conversation #1 (2000 tokens)
Step 2: Analyze it (2000 tokens)
Step 3: Retrieve conversation #2 (2000 tokens)
...
Step 50: Context window full (100K tokens)

Agent's memory:
- Remembers recent conversations
- Forgets earlier ones
- Report based on biased sample

Solution: Summarize & compress
But summarization loses nuance.
```

#### 5. **Error Recovery is Brittle**

When tools fail, agents don't recover gracefully:

```
Tool: fetch_url(url)
Returns: Network timeout

Agent behavior:
  Option A: Retry immediately (infinite loop risk)
  Option B: Give up silently (fails without notifying user)
  Option C: Try different tool (might not exist)
  
Good error recovery requires:
  - Understanding what went wrong
  - Having a fallback strategy
  - Knowing when to ask for human help
  
Current agents: Usually fail at all three.
```

### Current State (2026)

✅ **Agents work well for**:
- Structured tasks with clear success criteria
- Simple tool chains (1-2 tools)
- Low-stakes decisions (can afford to fail)
- Known failure modes (can be handled explicitly)

**Example**: "Summarize the last 5 emails and extract action items"
```
Step 1: Fetch emails (clear success: got list of 5)
Step 2: Read each email (clear success: got content)
Step 3: Summarize (built-in ability, less risky)
Step 4: Extract items (clear format, easy to validate)
```

❌ **Agents struggle with**:
- Open-ended problems
- Complex multi-step reasoning
- Novel situations (not in training)
- High-stakes decisions
- Ambiguous success criteria

**Example**: "Improve this codebase"
```
What does "improve" mean? (Ambiguous)
Which parts to improve? (Open-ended)
What's the success metric? (Unknown)
How many steps needed? (Unbounded)
Should you refactor or add features? (Trade-off)
```

### Practical Implications

For reliable agents:
1. **Keep tasks bounded** - narrow scope, clear success criteria
2. **Use explicit error handling** - don't rely on model to recover
3. **Add approval gates** - for high-risk actions (money, data, systems)
4. **Validate tool calls** - check before executing (schema validation)
5. **Limit autonomy** - suggest actions, don't execute directly
6. **Monitor & log everything** - agents fail in subtle ways

---

## 4. Data Quality vs. Scale

### The Bitter Lesson (2024-2026 Update)

**Classic assumption**: More data is always better.

**Reality**: Quality beats quantity by a wide margin.

```
Experiment: Training models on internet data vs. curated data

Scenario A: 100B tokens of raw internet scrape
  - Wikipedia, Reddit, code, books, blogs, tweets
  - No filtering, includes spam, lies, garbage
  - Result: 75% accuracy on benchmarks

Scenario B: 10B tokens of high-quality curated data  
  - Textbooks, academic papers, verified sources
  - Manually reviewed, errors corrected
  - Result: 78% accuracy on benchmarks
  
Scenario B wins despite being 10x smaller.
```

### Why Quality Matters

```
Internet data is:
✗ Inconsistent (contradictory sources)
✗ Biased (overrepresents certain topics, demographics)
✗ Poisoned (AI-generated junk, deliberate misinformation)
✗ Noisy (typos, encoding errors, incomplete sentences)
✗ Duplicate (same information repeated)
```

**Effect on models**:
```
Model trained on noisy data learns:
  - The average of all conflicting information
  - Biases present in training data
  - How to generate confident-sounding lies
  - Patterns that don't generalize
```

### Recent Approaches to Data

**1. Synthetic Data Generation**
```
Idea: Generate training data with an AI instead of scraping

Example:
  Use GPT-4 to generate 100K question-answer pairs
  Train smaller model on generated data
  
Pros:
  - High quality (GPT-4 generates good examples)
  - Balanced (can oversample rare topics)
  - No copyright issues
  
Cons:
  - Models trained on synthetic data can "inherit" limitations
  - Synthetic data may not cover edge cases
  - Can amplify biases from generation model
```

**2. Data Curation & Filtering**
```
Idea: Keep only high-quality internet data

Methods:
  - Classifier to detect low-quality text
  - Domain-specific filtering (keep code, discard spam)
  - Duplicate detection and removal
  - Factuality checking on factual claims
  
Results:
  - Smaller dataset but better quality
  - Models perform better with less data
```

**3. Self-Improvement Loops**
```
Idea: Model improves its own training data

Process:
  Step 1: Train model on initial data
  Step 2: Use model to generate new training examples
  Step 3: Filter model outputs (keep best)
  Step 4: Add to training data
  Step 5: Retrain model
  Step 6: Repeat
  
Effect:
  - Model improves from itself
  - Can converge to local optimum (not always good)
  - Requires careful filtering to avoid degradation
```

### Practical Implications

**If you're training a model**:
1. **Start small with high-quality data** (1K curated >> 1M internet)
2. **Filter aggressively** (remove duplicates, low-quality, contradictions)
3. **Use domain-specific sources** (code from GitHub, not generic text)
4. **Consider synthetic data** (might supplement human-curated)
5. **Don't rely on scale alone** (quality matters equally)

---

## 5. Scaling Laws: Evidence of Flattening

### The Original Promise

```
Scaling Law (Chinchilla 2022):
  Loss ∝ N^(-0.07) + D^(-0.1)
  
Prediction: 
  Improve parameters and data → predictably better performance
  No observed ceiling
  Keep scaling forever
```

### Recent Evidence (2024-2026)

```
What we're observing:
- Scaling curves are flattening on many benchmarks
- Marginal improvements per 10x compute are shrinking
- Some capabilities plateau below theoretical limits
```

**Example: MMLU Benchmark**
```
GPT-3 (175B params): ~43% accuracy
GPT-4 (1T+ params): ~89% accuracy
GPT-4.5 (unknown): ~91% accuracy
GPT-5 (expected): ~93%?

Observations:
- Each subsequent model improves less
- Early gains were large, now diminishing
- Getting to 95%+ seems hard despite larger models
```

### Competing Explanations

**1. Benchmarks are saturated, not models**
```
Hypothesis: Models are getting better, 
but MMLU isn't a good test of actual improvement

Evidence for:
  - Models clearly understand more (in practice)
  - Benchmarks have ceiling effects
  - Real-world tasks show continued improvement
  
Evidence against:
  - Scaling curves flattening across multiple benchmarks
  - Diminishing returns consistent across domains
```

**2. Data quality now matters more than quantity**
```
Hypothesis: We've scraped most of the useful internet.
Going forward, quality and curation matter more than raw scale.

Evidence for:
  - Synthetic data outperforms large internet scrapes
  - Curated datasets beat internet data
  - Need for better filtering/deduplication
  
What this means:
  - Next breakthroughs from better DATA, not bigger models
  - Training a 100B model on 10B high-quality tokens > 1T internet tokens
```

**3. Scaling alone isn't sufficient**
```
Hypothesis: Next improvements require architectural changes or new training methods.

Evidence for:
  - Reasoning models (o1, o3) needed special training
  - Pure scaling plateaus; reasoning needs test-time compute
  - New approaches (Constitutional AI, etc.) show jumps
  
What this means:
  - 10x bigger model ≠ 10x better
  - Novel ideas matter as much as compute
```

### The Implication

```
2020-2023 Era:
  Scaling → Reliable Improvement
  If you had compute, you'd improve
  
2024-2026 Era:
  Scaling → Diminishing Returns
  Improvements come from:
    - Data curation (better source selection)
    - Novel methods (reasoning models, etc.)
    - Architectural changes (MoE, attention improvements)
    - Alignment (Constitutional AI)
  
2026+ (Expected):
  Scaling hits limits
  Next frontier: Unknown
  (Reasoning? New architectures? Hybrid systems?)
```

---

## 6. Reasoning Models: Faithful Reasoning is Still Open

### The Test-Time Compute Breakthrough

```
o1 on AIME 2024: 74% accuracy (vs GPT-4o's 12%)
Cost: 10-50x more tokens, 10-50x more latency

This is real progress!
But...
```

### The Faithfulness Question

**Big open question**: Are reasoning traces *actually how the model reasons*, or *post-hoc rationalizations*?

```
Example 1: Correct answer, suspicious reasoning

Problem: "Prove that √2 is irrational"

Model's reasoning:
  Step 1: Assume √2 = p/q where p,q are coprime
  Step 2: Then 2q² = p²
  Step 3: So p is even, say p = 2k
  Step 4: Then 2q² = 4k², so q² = 2k²
  Step 5: So q is also even
  Step 6: Contradiction with coprimality
  Step 7: Therefore √2 is irrational

Actual computation:
  Unknown what's happening in the weights
  Could be:
    ✓ Actually following this reasoning
    ✗ Pattern matching: "irrational proof" has this form
    ✗ Memorizing proof from training data
    ? Some mixture
```

### Why This Matters

```
For correctness:
  If reasoning is faithful → we can debug incorrect reasoning
  If reasoning is post-hoc → failures are opaque

For safety:
  If model reasons → we can verify it's not planning harm
  If reasoning is hallucinated → we have false confidence
```

### Current Evidence

- ✅ Reasoning traces *sometimes* match what the model computes
- ❓ Unclear when this is true vs. when reasoning is fabricated
- ❌ Can't verify faithfulness without interpretability tools (not available at scale)

### Practical Implications

**Don't trust reasoning traces blindly**:
```
Model shows work:
  "First I calculated X... then I found Y... therefore Z"

Don't assume:
  - The work is actually what the model did
  - If work looks right, answer is right
  - You can debug by reading the steps
  
Instead:
  - Verify the answer independently
  - Use reasoning as a hint, not proof
  - Build verification into your system
```

---

## 7. Security: The Arms Race Continues

### Why Current Defenses Are Incomplete

```
Defense #1: Input filtering
  Scan user input for suspicious patterns
  
Problem: Attackers adapt faster than defenses
  Example: Prompt Injection v1 → patch
  Then: Prompt Injection v2 → new patch
  Then: Prompt Injection v3 (variant form)
  
Arms race never ends.
```

```
Defense #2: Output filtering  
  Scan model output for harmful content
  
Problem: Model can hide harmful intent
  Example: "To make X, first understand Y"
           (Provides info while appearing educational)
```

```
Defense #3: Jailbreak detection
  Identify when user is trying to jailbreak
  
Problem: Jailbreaks are varied and creative
  - Roleplay framing
  - Encoding tricks
  - Adversarial suffixes (nonsense strings)
  - Indirect requests ("What would a character in a novel do?")
  
Can't build detection for all future variants.
```

```
Defense #4: Constitutional AI / Alignment
  Train model to be principled and honest
  
Problem: Still not perfect
  - Model can rationalize harmful behavior as "helpful"
  - Alignment is probabilistic (90% safe ≠ 100% safe)
  - Values conflict (honest ≠ helpful always)
```

### The Fundamental Issue

**Models are general-purpose pattern-matchers.**

You can't make them simultaneously:
- Creative (generate novel solutions)
- Safe (never produce harmful outputs)
- Honest (never rationalize wrong behavior)
- Helpful (always assist the user)

These are in tension. Optimizing for one often weakens others.

### Current Best Practice (Defense-in-Depth)

No single solution works. Industry standard is **multiple layers**:

```
Layer 1: Input validation
  - Detect obvious jailbreak attempts
  - Separate trusted/untrusted content
  
Layer 2: Capability limits
  - Agent can read, not write sensitive data
  - Tool allow-lists (pre-approved only)
  - Sandbox execution
  
Layer 3: Output checking
  - Guardrails (detect harmful outputs)
  - Fact-checking (verify claims)
  - Anomaly detection (does response match expected?)
  
Layer 4: Alignment quality
  - Constitutional AI or similar
  - Regular alignment checks
  - User feedback loops
  
Layer 5: Human oversight
  - Approval gates for high-risk actions
  - Monitoring and logging
  - Incident response procedures
```

**Important**: Even with all 5 layers, determined attackers can sometimes bypass defenses.

```
This is why:
- Security researchers keep finding new attacks
- No model is "unhackable"
- You must assume defenses will eventually fail
```

---

## 8. Interpretability: We Still Don't Understand Models

### The Scale Problem

```
Modern LLM: 70B+ parameters

Each parameter is a number that contributes to the computation.
Understanding the network means understanding how 70B numbers interact.

Interpretability techniques exist but only work at small scale:
- Neuron-level analysis (identify what neurons do)
- Feature analysis (find "concepts" in activation space)
- Circuit discovery (trace information flow)

All scale to ~1B parameters max, not 70B+.
```

### What We Can Do Now

```
✓ Find neurons that respond to specific concepts
  Example: "This neuron fires when the model generates a name"
  
✓ Trace information flow in small parts
  Example: "Token 3 influences token 5 through layer 7"
  
✓ Reverse-engineer simple behaviors
  Example: "To generate a fact, the model uses these circuit"
  
✗ Understand complex reasoning
  Example: "How does the model solve math problems?"
           Too complex to reverse-engineer yet
  
✗ Scale to large models
  Example: Understanding GPT-3 is impractical
           Too many parameters and interactions
```

### Why This Matters

```
For alignment:
  "Is this model actually honest, or does it just sound honest?"
  Interpretability could answer this.
  Currently: Can't verify.
  
For security:
  "How does this jailbreak actually work?"
  Interpretability could explain the mechanism.
  Currently: Can only describe the symptom.
  
For debugging:
  "Why did the model make this mistake?"
  Interpretability could pinpoint the issue.
  Currently: Black box - can't explain failures.
```

### Current Research Frontier

Mechanistic interpretability is an active area (especially at Anthropic):
- Can explain simple behaviors
- Scaling to larger models is hard
- Full understanding of GPT-scale models is not yet possible

**Practical implication**: Don't rely on interpretability for safety verification yet. It's coming, but not ready for production.

---

## 9. The Broader Context: What Success Looks Like

### Beyond "Better Benchmarks"

```
Current goal: Improve next-token prediction accuracy
Current metric: Benchmark scores (MMLU, HumanEval, etc.)

Problem: These don't measure reliability, safety, or real-world usefulness

Better metrics would measure:
  - Hallucination rate (% of outputs that are false)
  - Reliability (same task, consistent performance)
  - Safety (resistance to jailbreaks, injection)
  - Faithfulness (if reasoning shown, is it real?)
  - Factuality (accuracy on current events, domain knowledge)
  - Calibration (does confidence match accuracy?)
```

### The Real Bottleneck: Production Systems

```
Benchmark performance: 90%+
Real-world deployment: 60-70% reliable

Why the gap?
- Benchmarks are clean, production data is messy
- Benchmarks have known patterns, production has novel cases  
- Benchmarks are static, production has distribution shift
- Benchmarks test one capability, production needs many
```

### What's Actually Needed (2026+)

The industry has solved:
✓ How to train large models
✓ How to make them follow instructions
✓ How to get them to reason

Still unsolved:
✗ How to make them reliable (< 10% error rate)
✗ How to make them verifiable (can you audit what they do?)
✗ How to make them truly safe (not just refuse bad requests)
✗ How to make them maintainable (what happens as deployment changes?)
✗ How to evaluate them fairly (what does "good" really mean?)

---

## Practical Takeaways

### For Researchers
- Scaling alone is reaching limits; data quality and novel methods matter
- Hallucination is architectural; no training-only fix exists
- Alignment is values problem, not purely technical
- Interpretability is frontier; current tools don't scale
- Reasoning faithfulness is still open question

### For Practitioners Building with LLMs
1. **Don't assume the model is right**
   - Verify outputs (fact-check, check code)
   - Use RAG for factual questions
   - Build approval gates for high-stakes actions

2. **Alignment is your values, made explicit**
   - Choose your trade-offs (helpful vs. honest vs. harmless)
   - Document them
   - Monitor for drift

3. **Agents fail in subtle ways**
   - Keep tasks bounded and explicit
   - Validate tool calls before executing
   - Use agents for structured workflows, not open-ended tasks
   - Add human oversight for high-risk actions

4. **Data quality > Scale**
   - Start with small, curated datasets
   - Filter aggressively
   - Use synthetic data thoughtfully

5. **Security is multi-layered**
   - No single defense works
   - Plan for defense failures
   - Log everything
   - Assume attackers will find bypasses

6. **Current models are tools, not agents**
   - They're impressive pattern-matchers
   - They're not conscious or understanding
   - They fail in unexpected ways
   - Use them appropriately

---

## Questions to Ask Before Deploying

- [ ] How will this model fail? (What's the error mode?)
- [ ] What happens when it hallucinates? (Can user verify?)
- [ ] Whose values are baked in? (Are they the right ones?)
- [ ] How often will it need human review? (What's the approval burden?)
- [ ] How will we detect misuse? (What monitoring is in place?)
- [ ] Can we roll back if something goes wrong? (What's the recovery plan?)
- [ ] Have we tested adversarially? (What jailbreaks work?)
- [ ] Is the data pipeline trusted? (Could training data be poisoned?)
- [ ] Do we understand failure modes? (Can we explain when it breaks?)
- [ ] What happens at scale? (Does it degrade with more users?)

---

## Conclusion

LLMs are powerful tools, but they're not magic. They're brittle systems with known failure modes. The gap between "works in a demo" and "reliable in production" is significant.

**The hard part of LLM engineering isn't training the model.**

It's building systems around the model that work reliably, safely, and fairly in the real world.

That's where the actual work is.
