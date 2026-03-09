# OpenAI YAML Interface Specification

UI-facing metadata for skill lists and chips.

## File Location

```
skill-name/
└── agents/
    └── openai.yaml
```

## Required Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `display_name` | string | Human-readable name | "PDF Editor" |
| `short_description` | string | Brief description (<100 chars) | "Create and edit PDF documents" |
| `default_prompt` | string | Suggested user prompt | "Help me rotate this PDF" |

## Optional Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `icon` | string | Emoji or icon identifier | "📄" |
| `brand_color` | string | Hex color for UI | "#4A90D9" |
| `tags` | array | Searchable tags | ["document", "pdf"] |
| `examples` | array | Usage examples | ["Rotate PDF", "Extract text"] |

## Example

```yaml
display_name: "PDF Editor"
short_description: "Create, edit, and analyze PDF documents"
default_prompt: "Help me work with this PDF file"
icon: "📄"
brand_color: "#D93025"
tags:
  - document
  - pdf
  - editing
examples:
  - "Rotate this PDF 90 degrees"
  - "Extract all text from this PDF"
  - "Merge these PDFs into one"
```

## Generation

Generate via script:

```bash
scripts/generate_openai_yaml.py <path/to/skill-folder> \
  --interface display_name="PDF Editor" \
  --interface short_description="Create and edit PDFs" \
  --interface default_prompt="Help me with this PDF"
```

Or via init:

```bash
scripts/init_skill.py my-skill --path ./skills \
  --interface display_name="My Skill" \
  --interface short_description="Brief description" \
  --interface default_prompt="Suggested prompt"
```

## Validation Rules

- `display_name`: 2-50 characters
- `short_description`: 10-100 characters
- `default_prompt`: 5-200 characters
- `icon`: Single emoji or icon identifier
- `brand_color`: Valid hex color (#RRGGBB)

## When to Update

Regenerate `openai.yaml` when:
- Skill description changes significantly
- New features added
- Target use cases evolve

Keep it in sync with SKILL.md frontmatter.