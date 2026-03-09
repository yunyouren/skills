---
name: U-skill-creator
description: Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit or optimize an existing skill, run evals to test a skill, benchmark skill performance, or optimize a skill's description for better triggering accuracy. Supports Claude Code, Codex, and GitHub Copilot CLI platforms.
version: 2.0.0
author: Integrated
platforms: [claude-code, codex, github-copilot-cli]
category: meta
tags: [automation, scaffolding, skill-creation, meta-skill, evaluation]
---

# U-skill-creator

A comprehensive skill for creating, testing, and optimizing AI assistant skills. Integrates the best practices from multiple skill-creator implementations with full evaluation capabilities.

## Overview

This skill automates the entire workflow of creating new CLI skills:
- **Interactive Creation** - Guided brainstorming with visual progress tracking
- **Multi-Platform Support** - Claude Code, Codex, GitHub Copilot CLI
- **Quality Validation** - YAML, content, and style checks
- **Evaluation System** - Evals, benchmarks, blind comparison
- **Description Optimization** - Iterative trigger accuracy improvement

## Progress Tracking

Throughout the workflow, display visual progress:

```
╔══════════════════════════════════════════════════════════════╗
║     🛠️  SKILL CREATOR - Creating New Skill                   ║
╠══════════════════════════════════════════════════════════════╣
║ ✓ Phase 1: Discovery                                         ║
║ → Phase 2: Brainstorming                [30%]                ║
║ ○ Phase 3: Implementation                                     ║
║ ○ Phase 4: Validation                                        ║
║ ○ Phase 5: Evaluation (optional)                             ║
║ ○ Phase 6: Installation                                      ║
╠══════════════════════════════════════════════════════════════╣
║ Progress: ████████░░░░░░░░░░░░░░░░░░░░░░  30%               ║
╚══════════════════════════════════════════════════════════════╝
```

---

## Phase 1: Discovery

Before starting, gather runtime information:

```bash
# Detect available platforms
CLAUDE_INSTALLED=false
CODEX_INSTALLED=false
COPILOT_INSTALLED=false

[[ -d "$HOME/.claude" ]] && CLAUDE_INSTALLED=true
[[ -d "$HOME/.codex" ]] && CODEX_INSTALLED=true
command -v gh &>/dev/null && gh copilot --version &>/dev/null 2>&1 && COPILOT_INSTALLED=true

# Get user info from git config
AUTHOR=$(git config user.name 2>/dev/null || echo "Unknown")
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
```

**Detect and confirm target platforms:**
- [ ] Claude Code (`~/.claude/skills/`)
- [ ] Codex (`~/.codex/skills/`)
- [ ] GitHub Copilot CLI (`~/.copilot/skills/`)
- [ ] All available platforms (recommended)

---

## Phase 2: Brainstorming & Planning

### Capture Intent

Understand what the skill should do:

1. **What should this skill enable the AI to do?**
   - Example: "Help users debug Python code by analyzing stack traces"

2. **When should this skill trigger?** (Provide 3-5 phrases)
   - Example: "debug Python error", "analyze stack trace", "fix Python exception"

3. **What type of skill is this?**
   - [ ] General purpose (default)
   - [ ] Code generation/modification
   - [ ] Documentation creation
   - [ ] Analysis/investigation
   - [ ] Tool integration

4. **Expected output format?**
   - Files, reports, code, structured data

5. **Need test cases?**
   - Skills with objective outputs benefit from test cases
   - Skills with subjective outputs (writing style) often don't

### Plan Resources

Identify what reusable resources would help:

| Resource Type | When to Include | Example |
|---------------|-----------------|---------|
| `scripts/` | Repeated code, deterministic tasks | `rotate_pdf.py` |
| `references/` | Domain knowledge, schemas | `api_docs.md` |
| `assets/` | Output templates, brand files | `template.html` |

---

## Phase 3: Implementation

### Step 3.1: Initialize Skill Structure

Create the skill directory:

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description required)
│   └── Markdown instructions
├── agents/ (optional, for subagents)
│   └── openai.yaml
└── Bundled Resources (optional)
    ├── scripts/    - Executable code
    ├── references/ - Documentation loaded as needed
    └── assets/     - Files used in output
```

### Step 3.2: Write SKILL.md

**Frontmatter requirements:**

```yaml
---
name: skill-name
description: What the skill does AND when to trigger. Include specific trigger contexts.
---
```

**Key principles:**
- `description` is the primary triggering mechanism - include both what AND when
- All "when to use" info goes in description, not body
- Body only loads after skill triggers

**Body structure:**

```markdown
# Skill Name

## Purpose
Brief description of what this skill enables.

## When to Use
(Skip this section - put in description instead)

## Workflow
Step-by-step instructions.

## Resources
How to use bundled scripts/references/assets.
```

### Step 3.3: Progressive Disclosure Pattern

Keep SKILL.md under 500 lines. Split content when approaching limit:

```
skill-name/
├── SKILL.md (core workflow + navigation)
└── references/
    ├── advanced-features.md
    ├── api-reference.md
    └── examples.md
```

Reference clearly from SKILL.md:
```markdown
## Advanced Features
See [advanced-features.md](references/advanced-features.md) for detailed configuration.
```

---

## Phase 4: Validation

Run validation to catch issues early:

```bash
scripts/quick_validate.py <path/to/skill-folder>
```

**Validation checks:**

| Check | Requirement |
|-------|-------------|
| YAML format | Valid frontmatter with name, description |
| Name format | Lowercase, hyphens only, <64 chars |
| Description quality | Includes trigger contexts |
| Word count | SKILL.md under 5k words |
| Writing style | Imperative form, no second-person |

**Common fixes:**
- Convert "You should..." to "Do..."
- Add trigger phrases to description
- Move detailed content to references/

---

## Phase 5: Evaluation (Optional)

For skills that benefit from objective testing, use the evaluation system.

### 5.1 Create Test Cases

Generate 2-3 realistic test prompts and save to `evals/evals.json`:

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "Realistic user task prompt",
      "expected_output": "Description of expected result",
      "files": []
    }
  ]
}
```

### 5.2 Run Tests

Spawn subagents in parallel - one with skill, one baseline:

**With-skill run:**
```
Execute this task:
- Skill path: <path-to-skill>
- Task: <eval prompt>
- Save outputs to: <workspace>/iteration-1/eval-0/with_skill/outputs/
```

**Baseline run:**
- New skill: No skill at all
- Improving existing: Old version snapshot

### 5.3 Grade & Benchmark

1. **Grade each run** against assertions
2. **Aggregate results:**
   ```bash
   python -m scripts.aggregate_benchmark <workspace>/iteration-1 --skill-name <name>
   ```
3. **Launch reviewer:**
   ```bash
   python eval-viewer/generate_review.py <workspace>/iteration-1 --skill-name "my-skill"
   ```

### 5.4 Iterate

Based on feedback:
1. Improve the skill
2. Rerun tests into new iteration directory
3. Compare with previous iteration
4. Repeat until satisfied

### 5.5 Blind Comparison (Advanced)

For rigorous A/B testing between two versions:
- Give outputs to independent agent without labels
- Let it judge quality blindly
- Analyze why winner won

---

## Phase 6: Description Optimization

Optimize the description for better triggering accuracy.

### Step 1: Generate Trigger Evals

Create 20 eval queries - mix of should-trigger and should-not-trigger:

```json
[
  {"query": "realistic user prompt", "should_trigger": true},
  {"query": "near-miss prompt", "should_trigger": false}
]
```

**Good eval queries:**
- Realistic and specific (file paths, context, details)
- Mix of formal and casual language
- Edge cases and near-misses

**Bad eval queries:**
- Too abstract: "Format this data"
- Obviously irrelevant: "Write fibonacci"

### Step 2: Run Optimization Loop

```bash
python -m scripts.run_loop \
  --eval-set <trigger-eval.json> \
  --skill-path <path-to-skill> \
  --max-iterations 5
```

This automatically:
- Splits into train/test sets
- Evaluates current description
- Proposes improvements
- Selects best by test score

### Step 3: Apply Result

Update SKILL.md frontmatter with `best_description`.

---

## Phase 7: Installation

### Installation Options

| Option | Description | Use Case |
|--------|-------------|----------|
| Repository only | Files in project | Team sharing via git |
| Global symlink | `~/.claude/skills/` | Works everywhere |
| Both | Repo + symlink | Recommended |

### Install Commands

```bash
# Claude Code
ln -sf "$REPO_ROOT/.claude/skills/$SKILL_NAME" "$HOME/.claude/skills/$SKILL_NAME"

# Codex
ln -sf "$REPO_ROOT/.codex/skills/$SKILL_NAME" "$HOME/.codex/skills/$SKILL_NAME"

# GitHub Copilot CLI
ln -sf "$REPO_ROOT/.github/skills/$SKILL_NAME" "$HOME/.copilot/skills/$SKILL_NAME"
```

### Install from GitHub

```bash
# From curated list
scripts/install-skill-from-github.py --repo openai/skills --path skills/.curated/<name>

# From any repo
scripts/install-skill-from-github.py --url https://github.com/<owner>/<repo>/tree/<ref>/<path>
```

---

## Error Handling

### Platform Detection Issues

```
⚠️  Unable to detect installed platforms

Options:
1. Install for repository only
2. Specify platform manually
3. Skip installation
```

### Validation Failures

```
⚠️  Validation Issues Found:

1. Description not in third-person format
   Expected: "This skill should be used when..."
   Found: "Use this skill when..."

2. Word count too high (5,342 words, max 5,000)
   Suggestion: Move detailed sections to references/

Fix automatically? [Y/n]
```

### Installation Conflicts

```
⚠️  Skill already installed at ~/.claude/skills/your-skill-name

Options:
1. Overwrite existing installation
2. Rename new skill
3. Skip installation
```

---

## Writing Style Guidelines

### DO

- Use imperative form: "Create the file", "Run the script"
- Explain the why: "Use ListView.builder for long lists to avoid memory issues"
- Keep SKILL.md lean: Reference detailed content in separate files
- Include concrete examples with context

### DON'T

- Use second person: "You should..."
- Add unnecessary MUST/ALWAYS directives
- Duplicate information between SKILL.md and references
- Create extraneous files (README.md, CHANGELOG.md) unless needed

---

## Bundled Resources

### scripts/

Executable utilities for skill operations:

| Script | Purpose |
|--------|---------|
| `init_skill.py` | Initialize new skill with template |
| `quick_validate.py` | Validate skill structure |
| `package_skill.py` | Create distributable .skill file |
| `aggregate_benchmark.py` | Aggregate evaluation results |
| `run_loop.py` | Description optimization loop |

### agents/

Subagent instructions for evaluation:

| Agent | Purpose |
|-------|---------|
| `grader.md` | Evaluate assertions against outputs |
| `analyzer.md` | Analyze benchmark patterns |
| `comparator.md` | Blind A/B comparison |

### references/

Detailed documentation:

| File | Content |
|------|---------|
| `schemas.md` | JSON structures for evals |
| `openai_yaml.md` | UI metadata specifications |
| `output-patterns.md` | Report templates |
| `workflows.md` | Detailed workflow guides |

---

## Quality Standards Summary

| Metric | Requirement |
|--------|-------------|
| SKILL.md word count | 1,500-2,000 ideal, <5,000 max |
| Description | Includes what + when to trigger |
| Writing style | Imperative, no second-person |
| Progressive disclosure | <500 lines, split to references |
| Test coverage | Objective skills need evals |

---

## Quick Reference

### Creation Flow

```
Discovery → Brainstorming → Implementation → Validation → Evaluation → Installation
```

### Key Commands

```bash
# Initialize
scripts/init_skill.py my-skill --path ./skills

# Validate
scripts/quick_validate.py ./skills/my-skill

# Package
scripts/package_skill.py ./skills/my-skill

# Run evals
python -m scripts.aggregate_benchmark workspace/iteration-1

# Optimize description
python -m scripts.run_loop --eval-set evals.json --skill-path ./skills/my-skill
```

---

## Platform-Specific Notes

### Claude Code

- Subagents available for parallel testing
- Browser viewer for evaluation results
- Full evaluation workflow supported

### Codex

- Uses `~/.codex/skills/` directory
- Follows OpenAI skill conventions
- May need sandbox escalation for network scripts

### GitHub Copilot CLI

- Uses `~/.copilot/skills/` directory
- Integration with gh CLI
- Similar structure to Codex

---

Good luck creating amazing skills!