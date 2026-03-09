#!/usr/bin/env python3
"""
Package a skill into a distributable .skill file (zip).
Usage: python package_skill.py <path/to/skill-folder> [output-directory]
"""

import argparse
import shutil
import sys
import zipfile
from pathlib import Path


def package_skill(skill_path: Path, output_dir: Path = None) -> Path:
    """Package skill into a .skill file."""

    # Validate skill exists
    if not skill_path.exists():
        raise FileNotFoundError(f"Skill folder not found: {skill_path}")

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        raise FileNotFoundError(f"SKILL.md not found in {skill_path}")

    # Determine output
    if output_dir is None:
        output_dir = skill_path.parent

    output_dir.mkdir(parents=True, exist_ok=True)

    # Create .skill file (zip)
    skill_name = skill_path.name
    output_file = output_dir / f"{skill_name}.skill"

    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file_path in skill_path.rglob('*'):
            if file_path.is_file():
                # Skip hidden files and common excludes
                if file_path.name.startswith('.'):
                    continue
                if file_path.name in ['__pycache__', 'node_modules', '.git']:
                    continue

                arcname = file_path.relative_to(skill_path)
                zf.write(file_path, arcname)

    return output_file


def main():
    parser = argparse.ArgumentParser(description="Package a skill")
    parser.add_argument("skill_path", help="Path to skill folder")
    parser.add_argument("output_dir", nargs="?", help="Output directory (default: same as skill)")
    parser.add_argument("--no-validate", action="store_true", help="Skip validation")

    args = parser.parse_args()

    skill_path = Path(args.skill_path).resolve()
    output_dir = Path(args.output_dir).resolve() if args.output_dir else None

    print(f"📦 Packaging skill: {skill_path.name}")

    # Run validation first (unless skipped)
    if not args.no_validate:
        import subprocess
        print("🔍 Running validation...")
        result = subprocess.run(
            [sys.executable, "quick_validate.py", str(skill_path)],
            cwd=Path(__file__).parent,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(result.stdout)
            if "FAILED" in result.stdout:
                print("❌ Validation failed. Fix errors or use --no-validate to skip.")
                sys.exit(1)
        else:
            print("✅ Validation passed")

    # Package
    try:
        output_file = package_skill(skill_path, output_dir)
        file_size = output_file.stat().st_size
        print(f"\n✅ Created: {output_file}")
        print(f"   Size: {file_size:,} bytes")
        print(f"\n💡 Install with:")
        print(f"   unzip {output_file.name} -d ~/.claude/skills/{skill_path.name}/")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()