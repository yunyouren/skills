# Skill Workflows

Detailed workflow guides for different use cases.

## Creating a New Skill

### Quick Path (Simple Skill)

```
1. Brainstorm (5 min)
   └── What does it do? When does it trigger?

2. Initialize (1 min)
   └── scripts/init_skill.py my-skill --path ./skills

3. Edit SKILL.md (15 min)
   └── Write purpose, workflow, resources

4. Validate (1 min)
   └── scripts/quick_validate.py ./skills/my-skill

5. Install (1 min)
   └── Symlink to ~/.claude/skills/
```

### Full Path (Production Skill)

```
1. Discovery & Planning
   ├── Understand requirements
   ├── Identify reusable resources
   └── Define success criteria

2. Implementation
   ├── Initialize structure
   ├── Write SKILL.md
   ├── Create scripts/references/assets
   └── Validate

3. Evaluation
   ├── Create test cases
   ├── Run evals (with-skill + baseline)
   ├── Grade and benchmark
   └── Iterate based on feedback

4. Optimization
   ├── Optimize description
   ├── Run trigger evals
   └── Apply best description

5. Distribution
   ├── Package as .skill file
   └── Install globally
```

## Improving an Existing Skill

### Step 1: Snapshot Current Version

```bash
cp -r ./skills/my-skill ./workspace/skill-snapshot/
```

### Step 2: Make Improvements

Edit SKILL.md and resources based on:
- User feedback
- Failed test cases
- New requirements

### Step 3: Compare

Run evals with both versions:
- `with_skill`: New version
- `old_skill`: Snapshot

### Step 4: Analyze

Use blind comparison if changes are significant:
- Anonymize outputs
- Let independent agent judge
- Analyze patterns

### Step 5: Deploy

If improvement confirmed:
- Update skill
- Reinstall symlink
- Archive old version

## Debugging a Skill

### Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Doesn't trigger | Description unclear | Add trigger phrases |
| Triggers too often | Description too broad | Add constraints |
| Wrong behavior | Instructions ambiguous | Be more specific |
| Slow performance | Too much in SKILL.md | Move to references |
| Inconsistent results | Missing edge cases | Add examples |

### Debugging Process

```
1. Check triggering
   └── Is description clear about when to use?

2. Check instructions
   └── Does SKILL.md have unambiguous steps?

3. Check resources
   └── Are scripts/references accessible?

4. Test with evals
   └── Create test cases for failing scenarios

5. Iterate
   └── Fix and re-test
```

## Evaluating Skill Quality

### Quantitative Metrics

| Metric | Good | Acceptable | Needs Work |
|--------|------|------------|------------|
| Pass rate | >90% | 70-90% | <70% |
| Time overhead | <50% | 50-100% | >100% |
| Token overhead | <30% | 30-60% | >60% |

### Qualitative Assessment

1. **Clarity**: Are instructions easy to follow?
2. **Completeness**: Does it handle edge cases?
3. **Consistency**: Same input → same output?
4. **Utility**: Does it actually help?

### Blind Comparison

When to use:
- Major skill revision
- Comparing two approaches
- Validating improvement claim

Process:
1. Run both versions on same evals
2. Anonymize outputs (A/B labels)
3. Independent agent judges quality
4. Analyze why winner won
5. Apply learnings

## Maintenance Workflow

### Regular Checks

```
Monthly:
├── Review trigger accuracy
├── Check for outdated references
└── Validate against new examples

Quarterly:
├── Run full evaluation suite
├── Compare with baseline
└── Update based on new best practices
```

### Version Management

```
skill-name/
├── CHANGELOG.md (optional, for user-facing skills)
└── versions/
    ├── v1.0.0/
    └── v1.1.0/
```

### Deprecation

When a skill is no longer maintained:
1. Add deprecation notice to SKILL.md
2. Suggest replacement if available
3. Keep available for 6 months
4. Remove after grace period