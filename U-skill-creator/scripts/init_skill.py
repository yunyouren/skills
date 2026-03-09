#!/usr/bin/env python3
"""
Initialize a new skill with template structure.
Usage: python init_skill.py <skill-name> --path <output-directory> [--resources scripts,references,assets]
"""

import argparse
import os
import sys
from pathlib import Path
from datetime import datetime


SKILL_TEMPLATE = '''---
name: {skill_name}
description: {description}
---

# {skill_name}

## Purpose

{purpose}

## When to Use This Skill

This skill should be used when:
- [Add trigger scenarios]

## Workflow

### Step 1: [First Step]

[Instructions]

### Step 2: [Second Step]

[Instructions]

## Resources

[Describe bundled resources if any]

## Examples

[Add usage examples]
'''


def create_skill(skill_name: str, output_path: Path, resources: list[str], description: str = ""):
    """Create skill directory structure."""

    skill_dir = output_path / skill_name
    skill_dir.mkdir(parents=True, exist_ok=True)

    # Create SKILL.md
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        content = SKILL_TEMPLATE.format(
            skill_name=skill_name,
            description=description or f"TODO: Add description for {skill_name}",
            purpose=f"TODO: Define purpose of {skill_name}"
        )
        skill_md.write_text(content, encoding='utf-8')
        print(f"✓ Created {skill_md}")
    else:
        print(f"  Skipped {skill_md} (already exists)")

    # Create agents directory
    agents_dir = skill_dir / "agents"
    agents_dir.mkdir(exist_ok=True)
    print(f"✓ Created {agents_dir}/")

    # Create resource directories
    for resource in resources:
        resource_dir = skill_dir / resource
        resource_dir.mkdir(exist_ok=True)
        print(f"✓ Created {resource_dir}/")

    print(f"\n✅ Skill '{skill_name}' initialized at {skill_dir}")
    print("\nNext steps:")
    print(f"  1. Edit {skill_dir / 'SKILL.md'}")
    print(f"  2. Add resources to {skill_dir}/")
    print(f"  3. Run: python quick_validate.py {skill_dir}")


def main():
    parser = argparse.ArgumentParser(description="Initialize a new skill")
    parser.add_argument("skill_name", help="Name of the skill (lowercase, hyphens)")
    parser.add_argument("--path", required=True, help="Output directory")
    parser.add_argument("--resources", default="scripts,references,assets",
                       help="Comma-separated list of resource directories")
    parser.add_argument("--description", default="", help="Skill description")
    parser.add_argument("--interface", action="append", default=[],
                       help="Interface metadata (key=value)")

    args = parser.parse_args()

    # Validate skill name
    if not args.skill_name.replace("-", "").replace("_", "").isalnum():
        print(f"Error: Invalid skill name '{args.skill_name}'. Use lowercase letters, numbers, and hyphens only.")
        sys.exit(1)

    output_path = Path(args.path)
    resources = [r.strip() for r in args.resources.split(",") if r.strip()]

    create_skill(args.skill_name, output_path, resources, args.description)


if __name__ == "__main__":
    main()