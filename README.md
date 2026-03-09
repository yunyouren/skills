# AI Skills Collection

A curated collection of AI assistant skills for Claude Code, Codex, and GitHub Copilot CLI platforms.

## Overview

This repository contains reusable skills that enhance AI coding assistants with specialized capabilities. Each skill follows a standardized format with YAML frontmatter and markdown instructions.

## Included Skills

### [U-skill-creator](U-skill-creator/)

A meta-skill for creating, testing, and optimizing AI assistant skills. It provides:

- **Interactive Creation** - Guided brainstorming with visual progress tracking
- **Multi-Platform Support** - Claude Code, Codex, GitHub Copilot CLI
- **Quality Validation** - YAML, content, and style checks
- **Evaluation System** - Evals, benchmarks, blind comparison
- **Description Optimization** - Iterative trigger accuracy improvement

### [U-neural-network-coder](U-neural-network-coder/)

Build, train, debug, and optimize neural networks with PyTorch. Features:

- Classification, regression, sequence modeling, and dynamical systems support
- Training loop templates with best practices
- Diagnosis and troubleshooting guides
- Model export and deployment patterns

### [U-matlab-simulink-coder](U-matlab-simulink-coder/)

Build, modify, and tune MATLAB/Simulink workflows for:

- Control systems design and simulation
- Circuit simulation
- Neural-ODE integration
- Python-MATLAB bridge automation

## Installation

### Claude Code

```bash
# Create skills directory if it doesn't exist
mkdir -p ~/.claude/skills

# Symlink a skill
ln -sf "$(pwd)/U-skill-creator" ~/.claude/skills/U-skill-creator
ln -sf "$(pwd)/U-neural-network-coder" ~/.claude/skills/U-neural-network-coder
ln -sf "$(pwd)/U-matlab-simulink-coder" ~/.claude/skills/U-matlab-simulink-coder
```

### Codex

```bash
mkdir -p ~/.codex/skills
ln -sf "$(pwd)/U-skill-creator" ~/.codex/skills/U-skill-creator
ln -sf "$(pwd)/U-neural-network-coder" ~/.codex/skills/U-neural-network-coder
ln -sf "$(pwd)/U-matlab-simulink-coder" ~/.codex/skills/U-matlab-simulink-coder
```

### GitHub Copilot CLI

```bash
mkdir -p ~/.copilot/skills
ln -sf "$(pwd)/U-skill-creator" ~/.copilot/skills/U-skill-creator
ln -sf "$(pwd)/U-neural-network-coder" ~/.copilot/skills/U-neural-network-coder
ln -sf "$(pwd)/U-matlab-simulink-coder" ~/.copilot/skills/U-matlab-simulink-coder
```

## Skill Structure

Each skill follows this structure:

```
skill-name/
├── SKILL.md              # Required: Main skill definition
│   ├── YAML frontmatter  # name, description, version, etc.
│   └── Markdown content  # Instructions and workflows
├── scripts/              # Optional: Executable utilities
├── references/           # Optional: Detailed documentation
├── agents/               # Optional: Subagent configurations
└── assets/               # Optional: Templates and static files
```

## Usage

Skills are automatically triggered by the AI assistant based on the `description` field in the frontmatter. Simply describe your task naturally, and the appropriate skill will be activated.

Example prompts:
- "Create a new skill for database migrations" → triggers U-skill-creator
- "Build a CNN for image classification" → triggers U-neural-network-coder
- "Tune a PID controller in Simulink" → triggers U-matlab-simulink-coder

## Creating New Skills

Use the U-skill-creator skill to create new skills:

```bash
# Initialize a new skill
python U-skill-creator/scripts/init_skill.py my-new-skill --path ./skills

# Validate the skill
python U-skill-creator/scripts/quick_validate.py ./my-new-skill
```

## License

MIT License