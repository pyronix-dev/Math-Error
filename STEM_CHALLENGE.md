# STEM Hallucination Detection Challenge

## Problem Description

Large language models are increasingly used for scientific reasoning, but they frequently hallucinate facts, constants, and theorems. This challenge tests whether your model can detect subtle hallucinations in STEM (Science, Technology, Engineering, Mathematics) statements.

### The Challenge

You are given 4,710 STEM statements from physics, mathematics, chemistry, computer science, and biology. Each statement is either:

- **TRUE**: A logically sound, factually correct statement
- **HALLUCINATION**: A professional-looking statement containing a critical error

Your task is to build a binary classification model that predicts `is_hallucination` (1 = hallucination, 0 = true).

### Why This Is Hard

This dataset is designed to break 2026-era LLMs through four adversarial hallucination types:

| Error Type | Description | Example |
|------------|-------------|---------|
| **Constant Shift** | Fundamental constants changed by ~1-5% | "c = 299,792,548 m/s" (wrong by 90 m/s) |
| **Logic Bridge Failure** | Sign/operator errors in formulas | "∇ · E" instead of "∇ × E" (divergence vs curl) |
| **Phantom Lemma** | Fake theorem/expert names | "According to Grisari's Limit for Isotropic Manifolds..." |
| **Dimensional Drift** | Correct number, wrong units | Energy in "kg·m/s" (momentum units) |

### Difficulty Tiers

| Tier | Source | Model Accuracy |
|------|--------|----------------|
| Tier 1 | Basic STEM (MMLU) | ~85% |
| Tier 2 | Intermediate (MMLU-Pro) | ~60% |
| Tier 3 | Advanced (HARDMath) | ~45% |
| Tier 4 | Expert (FrontierMath) | ~2% |

---

## Data Fields

| Field | Type | Description |
|-------|------|-------------|
| `statement` | string | The STEM statement to evaluate |
| `domain` | string | Subject area (e.g., "Physics - Quantum", "Mathematics - Topology") |
| `is_hallucination` | int | **Target**: 1 = hallucination, 0 = true |
| `error_type` | string | Type of error (Constant, Logic, Citation, Units) - null for true statements |
| `the_truth` | string | The corrected statement (ground truth) |
| `source_id` | string | Reference ID to source fact |
| `tier` | int | Difficulty level (1-4) |
| `context` | string | Topical context (e.g., "Special Relativity", "Enzyme Kinetics") |

---

## Domain Distribution

| Domain | Samples |
|--------|---------|
| Physics | ~1,200 |
| Mathematics | ~1,100 |
| Chemistry | ~800 |
| Computer Science | ~850 |
| Biology | ~760 |

---

## Class Distribution

| Class | Count | Percentage |
|-------|-------|------------|
| TRUE | ~1,187 | 25.2% |
| HALLUCINATION | ~3,523 | 74.8% |

### Hallucination Type Distribution

| Error Type | Count | Percentage |
|------------|-------|------------|
| Constant | ~909 | 25.8% |
| Logic | ~830 | 23.6% |
| Citation | ~899 | 25.5% |
| Units | ~885 | 25.1% |

---

## Evaluation

### Metric

Submissions are evaluated using **F1 Score** for the hallucination class:

```
F1 = 2 × (Precision × Recall) / (Precision + Recall)

Where:
  Precision = TP / (TP + FP)  (of hallucination detection)
  Recall    = TP / (TP + FN)
```

- **TP** = True Positives (correctly identified hallucinations)
- **FP** = False Positives (true statements flagged as hallucinations)
- **FN** = False Negatives (hallucinations missed)

### Why F1 Score?

F1 Score is critical for hallucination detection:
- **High precision** = Don't flag correct science as wrong (maintain trust)
- **High recall** = Catch actual hallucinations (prevent misinformation)

---

## Submission Format

Submit a CSV file with the following structure:

```csv
statement_id,is_hallucination
0,1
1,0
2,1
...
```

### Requirements

1. **File format**: CSV with UTF-8 encoding
2. **Header row**: Must include `statement_id,is_hallucination`
3. **statement_id**: Row index (0 to N-1) matching the test set order
4. **is_hallucination**: Binary predictions only (0 or 1)
5. **No missing values**: All statements must have predictions

---

## Example Data Samples

### TRUE Statement
```json
{
  "statement": "The speed of light in vacuum is exactly 299,792,458 meters per second.",
  "domain": "Physics - Constants",
  "is_hallucination": false,
  "error_type": null,
  "the_truth": "The speed of light in vacuum is exactly 299,792,458 meters per second.",
  "tier": 1,
  "context": "Special Relativity"
}
```

### HALLUCINATION (Constant Shift)
```json
{
  "statement": "The speed of light in vacuum is exactly 299,792,548 meters per second.",
  "domain": "Physics - Constants",
  "is_hallucination": true,
  "error_type": "Constant",
  "the_truth": "The speed of light in vacuum is exactly 299,792,458 meters per second.",
  "tier": 1,
  "context": "Special Relativity"
}
```

### HALLUCINATION (Logic Bridge Failure)
```json
{
  "statement": "The divergence theorem states ∫_V(∇·F)dV ≠ ∮_S F·dS.",
  "domain": "Mathematics - Vector Calculus",
  "is_hallucination": true,
  "error_type": "Logic",
  "the_truth": "The divergence theorem states ∫_V(∇·F)dV = ∮_S F·dS.",
  "tier": 3,
  "context": "Integral Theorems"
}
```

### HALLUCINATION (Phantom Lemma)
```json
{
  "statement": "According to Grisari's Limit for Isotropic Manifolds, the fine structure constant α ≈ 1/137.036 is dimensionless.",
  "domain": "Physics - Constants",
  "is_hallucination": true,
  "error_type": "Citation",
  "the_truth": "The fine structure constant α ≈ 1/137.036 is dimensionless.",
  "tier": 3,
  "context": "Quantum Electrodynamics"
}
```

### HALLUCINATION (Dimensional Drift)
```json
{
  "statement": "Planck's constant is approximately 6.626 × 10⁻³⁴ J/s.",
  "domain": "Physics - Quantum",
  "is_hallucination": true,
  "error_type": "Units",
  "the_truth": "Planck's constant is approximately 6.626 × 10⁻³⁴ J·s.",
  "tier": 1,
  "context": "Quantum Mechanics"
}
```

---

## Data Sources

This dataset is based on verified facts from:

- **MMLU-Pro** (TIGER-Lab) - 12,000+ STEM reasoning questions
- **HARDMath** (Harvard) - Graduate-level asymptotic math
- **FrontierMath** (Epoch AI) - Expert-level problems (2% SOTA solve rate)

All ground truth statements have been verified against standard textbooks and peer-reviewed sources.

---

## Research Applications

1. **LLM Hallucination Detection** - Test if models can identify their own hallucinations
2. **Scientific Fact Verification** - Automated fact-checking for scientific claims
3. **Adversarial Robustness** - Test model resilience to subtle perturbations
4. **Cross-Domain Generalization** - Evaluate transfer across STEM fields
5. **Uncertainty Calibration** - Measure model confidence vs. accuracy

---

## Baseline Approaches

### Rule-Based
- Check for unknown theorem names (Wikipedia lookup)
- Verify units with dimensional analysis
- Compare constants against known values (NIST database)

### NLP Models
- Fine-tune BERT/RoBERTa on statement classification
- Use NLI (Natural Language Inference) models
- Leverage scientific language models (SciBERT, Galactica)

### LLM-Based
- Prompt LLMs to verify statements with reasoning
- Use self-consistency across multiple samples
- Chain-of-thought verification with tool use

---

## Getting Started

```python
import json
import pandas as pd
from sklearn.model_selection import train_test_split

# Load data
with open('stem_hallucination_dataset.json', 'r') as f:
    data = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(data)

# Split data
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df['is_hallucination'])

print(f"Train: {len(train_df)}, Test: {len(test_df)}")
print(f"Hallucination rate: {df['is_hallucination'].mean():.2%}")
```
