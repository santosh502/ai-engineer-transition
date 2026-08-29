# Assets for LLM Learning Path

This folder contains images and visual references for the LLM learning materials.

## Images Included

### 1. `transformer_architecture.png`
- **Source**: Figure 1 from "Attention Is All You Need" paper (Vaswani et al., 2017)
- **What it shows**: Complete Transformer architecture with encoder (left) and decoder (right) stacks
- **Used in**: `00_attention_is_all_you_need.md` - Section "The Complete Transformer Architecture"
- **Status**: ✅ Included

### 2. `attention_mechanism.png`
- **Source**: Figure 2 from "Attention Is All You Need" paper
- **What it shows**: 
  - Left: Scaled Dot-Product Attention mechanism
  - Right: Multi-Head Attention with h parallel heads
- **Used in**: `00_attention_is_all_you_need.md` - Section "The Attention Calculation"
- **Status**: ✅ Included

## How Images Are Used

The markdown document `00_attention_is_all_you_need.md` automatically references these images:
```markdown
![Transformer Architecture](./assets/transformer_architecture.png)
![Attention Mechanism](./assets/attention_mechanism.png)
```

When you view the document in a markdown viewer or IDE, these images will display inline with the text.

## Notes

- Both images are PNG format
- These are official figures from the original Transformer paper
- Freely distributable for educational purposes
