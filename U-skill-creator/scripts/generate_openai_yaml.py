#!/usr/bin/env python3
"""
Generate openai.yaml for a skill.
Usage: python generate_openai_yaml.py <path/to/skill-folder> --interface key=value
"""

import argparse
import re
import yaml
from pathlib import Path


def extract_from_skill_md(skill_md_path: Path) -> dict:
    """Extract basic info from SKILL.md."""
    content = skill_md_path.read_text(encoding='utf-8')

    # Extract name from frontmatter
    name_match = re.search(r'^name:\s*(.+)$', content, re.MULTILINE)
    name = name_match.group(1).strip() if name_match else skill_md_path.parent.name

    # Extract description from frontmatter
    desc_match = re.search(r'^description:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE)
    description = desc_match.group(1).strip() if desc_match else ""

    return {
        "name": name,
        "description": description
    }


def generate_openai_yaml(skill_path: Path, interface_args: list[str]) -> dict:
    """Generate openai.yaml content."""

    skill_md = skill_path / "SKILL.md"
    info = extract_from_skill_md(skill_md) if skill_md.exists() else {}

    # Parse interface args
    interface = {}
    for arg in interface_args:
        if "=" in arg:
            key, value = arg.split("=", 1)
            interface[key.strip()] = value.strip()

    # Build YAML structure
    yaml_content = {
        "display_name": interface.get("display_name", info.get("name", skill_path.name).replace("-", " ").title()),
        "short_description": interface.get("short_description", info.get("description", "")[:100]),
        "default_prompt": interface.get("default_prompt", f"Help me with {info.get('name', skill_path.name)}"),
    }

    # Add optional fields if provided
    if "icon" in interface:
        yaml_content["icon"] = interface["icon"]
    if "brand_color" in interface:
        yaml_content["brand_color"] = interface["brand_color"]
    if "tags" in interface:
        yaml_content["tags"] = [t.strip() for t in interface["tags"].split(",")]

    return yaml_content


def main():
    parser = argparse.ArgumentParser(description="Generate openai.yaml")
    parser.add_argument("skill_path", help="Path to skill folder")
    parser.add_argument("--interface", action="append", default=[],
                       help="Interface metadata (key=value)")

    args = parser.parse_args()

    skill_path = Path(args.skill_path)

    if not skill_path.exists():
        print(f"❌ Error: Skill folder not found: {skill_path}")
        return 1

    # Generate YAML content
    yaml_content = generate_openai_yaml(skill_path, args.interface)

    # Create agents directory if needed
    agents_dir = skill_path / "agents"
    agents_dir.mkdir(exist_ok=True)

    # Write openai.yaml
    yaml_path = agents_dir / "openai.yaml"
    with open(yaml_path, 'w', encoding='utf-8') as f:
        yaml.dump(yaml_content, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print(f"✅ Generated {yaml_path}")
    print(f"\nContent:")
    print(yaml.dump(yaml_content, default_flow_style=False, sort_keys=False, allow_unicode=True))

    return 0


if __name__ == "__main__":
    exit(main())