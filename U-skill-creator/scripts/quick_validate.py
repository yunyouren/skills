#!/usr/bin/env python3
"""
Validate skill structure and content.
Usage: python quick_validate.py <path/to/skill-folder>
"""

import argparse
import re
import sys
from pathlib import Path
from typing import NamedTuple


class ValidationIssue(NamedTuple):
    level: str  # ERROR, WARNING, INFO
    message: str
    suggestion: str = ""


def validate_yaml_frontmatter(content: str) -> list[ValidationIssue]:
    """Validate YAML frontmatter in SKILL.md."""
    issues = []

    # Check for frontmatter
    if not content.startswith("---"):
        issues.append(ValidationIssue(
            "ERROR",
            "Missing YAML frontmatter",
            "Add frontmatter with name and description fields"
        ))
        return issues

    # Extract frontmatter
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not match:
        issues.append(ValidationIssue(
            "ERROR",
            "Invalid YAML frontmatter format",
            "Ensure frontmatter is enclosed by --- lines"
        ))
        return issues

    frontmatter = match.group(1)

    # Check required fields
    if "name:" not in frontmatter:
        issues.append(ValidationIssue(
            "ERROR",
            "Missing 'name' field in frontmatter",
            "Add 'name: your-skill-name'"
        ))

    if "description:" not in frontmatter:
        issues.append(ValidationIssue(
            "ERROR",
            "Missing 'description' field in frontmatter",
            "Add 'description: What the skill does and when to trigger'"
        ))

    # Check description quality
    desc_match = re.search(r'description:\s*["\']?(.+?)["\']?\s*$', frontmatter, re.MULTILINE)
    if desc_match:
        description = desc_match.group(1).strip('"\'')
        if len(description) < 20:
            issues.append(ValidationIssue(
                "WARNING",
                f"Description too short ({len(description)} chars)",
                "Include what the skill does AND when to trigger"
            ))
        if "when" not in description.lower() and "trigger" not in description.lower():
            issues.append(ValidationIssue(
                "INFO",
                "Description may lack trigger context",
                "Consider adding 'Use when...' or 'This skill should be used when...'"
            ))

    return issues


def validate_name(skill_name: str) -> list[ValidationIssue]:
    """Validate skill name format."""
    issues = []

    if skill_name != skill_name.lower():
        issues.append(ValidationIssue(
            "ERROR",
            f"Skill name '{skill_name}' should be lowercase",
            f"Use '{skill_name.lower()}'"
        ))

    if " " in skill_name:
        issues.append(ValidationIssue(
            "ERROR",
            f"Skill name '{skill_name}' contains spaces",
            f"Use hyphens: '{skill_name.replace(' ', '-')}'"
        ))

    if len(skill_name) > 64:
        issues.append(ValidationIssue(
            "WARNING",
            f"Skill name is long ({len(skill_name)} chars)",
            "Consider a shorter name"
        ))

    if not re.match(r'^[a-z0-9-]+$', skill_name):
        issues.append(ValidationIssue(
            "ERROR",
            f"Skill name '{skill_name}' contains invalid characters",
            "Use only lowercase letters, numbers, and hyphens"
        ))

    return issues


def validate_content(content: str) -> list[ValidationIssue]:
    """Validate SKILL.md content."""
    issues = []

    # Count words (approximate)
    words = len(content.split())

    if words > 5000:
        issues.append(ValidationIssue(
            "WARNING",
            f"SKILL.md is long ({words} words)",
            "Consider moving detailed content to references/"
        ))
    elif words < 100:
        issues.append(ValidationIssue(
            "WARNING",
            f"SKILL.md is short ({words} words)",
            "Add more detail about workflow and resources"
        ))
    elif 1500 <= words <= 2500:
        issues.append(ValidationIssue(
            "INFO",
            f"Word count looks good ({words} words)"
        ))

    # Check for second person
    second_person_patterns = [
        r'\byou should\b',
        r'\byou can\b',
        r'\byou will\b',
        r'\byour\b',
    ]

    for pattern in second_person_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            issues.append(ValidationIssue(
                "INFO",
                f"Found {len(matches)} second-person reference(s) ('{matches[0]}')",
                "Consider using imperative form (e.g., 'Do X' instead of 'You should do X')"
            ))
            break  # Only report once

    # Check for MUST/ALWAYS overuse
    must_count = len(re.findall(r'\bMUST\b|\bALWAYS\b|\bNEVER\b', content))
    if must_count > 5:
        issues.append(ValidationIssue(
            "INFO",
            f"Found {must_count} MUST/ALWAYS/NEVER directives",
            "Consider explaining the 'why' instead of using directives"
        ))

    return issues


def validate_structure(skill_path: Path) -> list[ValidationIssue]:
    """Validate skill directory structure."""
    issues = []

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        issues.append(ValidationIssue(
            "ERROR",
            "SKILL.md not found",
            "Create SKILL.md with required frontmatter"
        ))

    # Check for common extra files that shouldn't exist
    extra_files = ["README.md", "CHANGELOG.md", "INSTALLATION.md"]
    for extra in extra_files:
        if (skill_path / extra).exists():
            issues.append(ValidationIssue(
                "INFO",
                f"Found {extra} (usually not needed)",
                "Skills typically don't need user-facing docs"
            ))

    return issues


def main():
    parser = argparse.ArgumentParser(description="Validate a skill")
    parser.add_argument("skill_path", help="Path to skill folder")
    args = parser.parse_args()

    skill_path = Path(args.skill_path)

    if not skill_path.exists():
        print(f"❌ Error: Path '{skill_path}' does not exist")
        sys.exit(1)

    print(f"🔍 Validating skill at {skill_path}\n")

    all_issues = []

    # Validate structure
    all_issues.extend(validate_structure(skill_path))

    # Validate name
    skill_name = skill_path.name
    all_issues.extend(validate_name(skill_name))

    # Validate SKILL.md
    skill_md = skill_path / "SKILL.md"
    if skill_md.exists():
        content = skill_md.read_text(encoding='utf-8')
        all_issues.extend(validate_yaml_frontmatter(content))
        all_issues.extend(validate_content(content))

    # Report results
    errors = [i for i in all_issues if i.level == "ERROR"]
    warnings = [i for i in all_issues if i.level == "WARNING"]
    infos = [i for i in all_issues if i.level == "INFO"]

    for issue in all_issues:
        icon = {"ERROR": "❌", "WARNING": "⚠️", "INFO": "ℹ️"}.get(issue.level, "•")
        print(f"{icon} [{issue.level}] {issue.message}")
        if issue.suggestion:
            print(f"   💡 {issue.suggestion}")

    print(f"\n{'='*50}")
    print(f"Summary: {len(errors)} errors, {len(warnings)} warnings, {len(infos)} info")

    if errors:
        print("❌ Validation FAILED - fix errors before packaging")
        sys.exit(1)
    elif warnings:
        print("⚠️  Validation passed with warnings")
        sys.exit(0)
    else:
        print("✅ Validation passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()