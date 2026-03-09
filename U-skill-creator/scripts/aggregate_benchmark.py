#!/usr/bin/env python3
"""
Aggregate evaluation results into benchmark data.
Usage: python -m aggregate_benchmark <workspace>/iteration-N --skill-name <name>
"""

import argparse
import json
import statistics
from pathlib import Path
from datetime import datetime


def load_json(path: Path) -> dict:
    """Load JSON file."""
    if path.exists():
        return json.loads(path.read_text(encoding='utf-8'))
    return {}


def save_json(path: Path, data: dict):
    """Save JSON file."""
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')


def aggregate_benchmark(workspace: Path, skill_name: str) -> dict:
    """Aggregate all eval results into benchmark data."""

    configs = {}
    per_eval = []

    # Find all eval directories
    eval_dirs = sorted([d for d in workspace.iterdir() if d.is_dir() and d.name.startswith('eval-')])

    for eval_dir in eval_dirs:
        eval_name = eval_dir.name
        eval_metadata = load_json(eval_dir / "eval_metadata.json")
        eval_id = eval_metadata.get("eval_id", eval_name)

        eval_result = {
            "eval_id": eval_id,
            "eval_name": eval_metadata.get("eval_name", eval_name),
        }

        # Process each config (with_skill, without_skill, old_skill, etc.)
        for config_dir in eval_dir.iterdir():
            if not config_dir.is_dir():
                continue

            config_name = config_dir.name

            grading = load_json(config_dir / "grading.json")
            timing = load_json(config_dir / "timing.json")

            if config_name not in configs:
                configs[config_name] = {
                    "name": config_name,
                    "total_evals": 0,
                    "total_assertions": 0,
                    "passed": 0,
                    "failed": 0,
                    "durations": [],
                    "tokens": []
                }

            if grading:
                summary = grading.get("summary", {})
                passed = summary.get("passed", 0)
                failed = summary.get("failed", 0)
                total = summary.get("total", 0)

                configs[config_name]["total_evals"] += 1
                configs[config_name]["total_assertions"] += total
                configs[config_name]["passed"] += passed
                configs[config_name]["failed"] += failed

            if timing:
                configs[config_name]["durations"].append(timing.get("total_duration_seconds", 0))
                configs[config_name]["tokens"].append(timing.get("total_tokens", 0))

            # Add to per_eval
            eval_result[config_name] = {
                "passed": grading.get("summary", {}).get("passed", 0),
                "total": grading.get("summary", {}).get("total", 0),
                "duration_seconds": timing.get("total_duration_seconds", 0)
            }

        per_eval.append(eval_result)

    # Calculate stats for each config
    for config in configs.values():
        total = config["total_assertions"]
        config["pass_rate"] = config["passed"] / total if total > 0 else 0

        durations = config.pop("durations", [])
        tokens = config.pop("tokens", [])

        if durations:
            config["mean_duration_seconds"] = statistics.mean(durations)
            config["stddev_duration_seconds"] = statistics.stdev(durations) if len(durations) > 1 else 0
        else:
            config["mean_duration_seconds"] = 0
            config["stddev_duration_seconds"] = 0

        if tokens:
            config["mean_tokens"] = statistics.mean(tokens)
            config["stddev_tokens"] = statistics.stdev(tokens) if len(tokens) > 1 else 0
        else:
            config["mean_tokens"] = 0
            config["stddev_tokens"] = 0

    # Calculate delta (first config vs second)
    config_list = list(configs.values())
    delta = {}
    if len(config_list) >= 2:
        c1, c2 = config_list[0], config_list[1]
        delta = {
            "pass_rate": c1["pass_rate"] - c2["pass_rate"],
            "duration_seconds": c1["mean_duration_seconds"] - c2["mean_duration_seconds"],
            "tokens": c1["mean_tokens"] - c2["mean_tokens"]
        }

    # Build benchmark
    benchmark = {
        "skill_name": skill_name,
        "iteration": int(workspace.name.split('-')[-1]) if '-' in workspace.name else 1,
        "timestamp": datetime.now().isoformat(),
        "configs": config_list,
        "delta": delta,
        "per_eval": per_eval
    }

    return benchmark


def format_markdown(benchmark: dict) -> str:
    """Format benchmark as markdown."""

    lines = [
        f"# Benchmark: {benchmark['skill_name']}",
        f"",
        f"**Iteration:** {benchmark['iteration']}",
        f"**Timestamp:** {benchmark['timestamp']}",
        f"",
        "## Summary",
        "",
        "| Config | Pass Rate | Passed/Total | Time (s) | Tokens |",
        "|--------|-----------|--------------|----------|--------|",
    ]

    for config in benchmark['configs']:
        lines.append(
            f"| {config['name']} | {config['pass_rate']:.1%} | "
            f"{config['passed']}/{config['total_assertions']} | "
            f"{config['mean_duration_seconds']:.1f} ± {config['stddev_duration_seconds']:.1f} | "
            f"{config['mean_tokens']:.0f} |"
        )

    if benchmark.get('delta'):
        delta = benchmark['delta']
        lines.extend([
            "",
            "## Delta",
            "",
            f"- **Pass Rate:** {delta['pass_rate']:+.1%}",
            f"- **Time:** {delta['duration_seconds']:+.1f}s",
            f"- **Tokens:** {delta['tokens']:+,.0f}",
        ])

    lines.extend([
        "",
        "## Per-Eval Results",
        "",
        "| Eval | Config | Passed | Total | Time |",
        "|------|--------|--------|-------|------|",
    ])

    for eval_result in benchmark['per_eval']:
        for config_name in ['with_skill', 'without_skill', 'old_skill']:
            if config_name in eval_result:
                r = eval_result[config_name]
                lines.append(
                    f"| {eval_result['eval_name']} | {config_name} | "
                    f"{r['passed']} | {r['total']} | {r['duration_seconds']:.1f}s |"
                )

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description="Aggregate benchmark results")
    parser.add_argument("workspace", help="Path to iteration workspace")
    parser.add_argument("--skill-name", required=True, help="Skill name")

    args = parser.parse_args()

    workspace = Path(args.workspace)

    if not workspace.exists():
        print(f"❌ Error: Workspace not found: {workspace}")
        return 1

    benchmark = aggregate_benchmark(workspace, args.skill_name)

    # Save results
    save_json(workspace / "benchmark.json", benchmark)
    (workspace / "benchmark.md").write_text(format_markdown(benchmark), encoding='utf-8')

    print(f"✅ Created benchmark.json and benchmark.md")
    print(f"\n{format_markdown(benchmark)}")

    return 0


if __name__ == "__main__":
    exit(main())