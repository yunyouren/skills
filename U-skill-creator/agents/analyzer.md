# Analyzer Agent

Analyze benchmark results to identify patterns and insights.

## Task

Given benchmark data, surface patterns that aggregate stats might hide.

## Input

- `benchmark.json` with per-eval results
- `benchmark.md` with formatted summary
- Timing and token data

## Analysis Areas

### 1. Non-Discriminating Assertions

Assertions that pass regardless of skill quality:

```
Assertion "output exists" passed 100% in both with_skill and baseline
→ This assertion doesn't measure skill quality
→ Consider removing or making stricter
```

### 2. High-Variance Evals

Evals with inconsistent results across runs:

```
Eval "complex-task" varies widely:
- Run 1: passed 3/5 assertions
- Run 2: passed 5/5 assertions
- Run 3: passed 2/5 assertions
→ Possibly flaky, consider stabilizing or splitting
```

### 3. Time/Token Tradeoffs

```
with_skill: 45s, 12k tokens
baseline: 23s, 8k tokens
→ Skill adds overhead but improves quality
→ Is the quality gain worth the cost?
```

### 4. Failure Patterns

Group failures by type:

```
Common failure modes:
- Missing error handling (3 evals)
- Incomplete output format (2 evals)
- Timeout on large inputs (1 eval)
```

### 5. Skill Strengths vs Weaknesses

```
Strengths:
- Handles edge cases well (passed 4/4 edge case evals)
- Output formatting consistent

Weaknesses:
- Struggles with multi-step reasoning (failed 3/5)
- Missing context for ambiguous inputs
```

## Output Format

```markdown
# Benchmark Analysis

## Executive Summary
[1-2 sentences on overall findings]

## Key Insights

### Non-Discriminating Tests
[List and recommendations]

### High-Variance Areas
[List and recommendations]

### Performance Tradeoffs
[Time/token analysis]

## Skill Quality Assessment

### Strengths
- [List]

### Weaknesses
- [List]

### Recommendations
1. [Specific improvement]
2. [Specific improvement]
```

## Guidelines

- Focus on actionable insights
- Use data to support claims
- Avoid restating the obvious
- Connect findings to skill improvement