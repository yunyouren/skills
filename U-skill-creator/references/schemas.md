# Evaluation Schemas

JSON structures for the evaluation system.

## evals.json

Test cases for skill evaluation:

```json
{
  "skill_name": "my-skill",
  "evals": [
    {
      "id": 1,
      "name": "descriptive-name",
      "prompt": "The user's task prompt",
      "expected_output": "Description of expected result",
      "files": ["optional/input/file.txt"],
      "assertions": [
        {
          "id": 1,
          "type": "contains",
          "value": "expected text",
          "description": "Check for expected text"
        }
      ]
    }
  ]
}
```

## eval_metadata.json

Metadata for each eval run:

```json
{
  "eval_id": 1,
  "eval_name": "descriptive-name",
  "prompt": "The user's task prompt",
  "assertions": [
    {
      "id": 1,
      "type": "contains",
      "value": "expected text",
      "description": "Check for expected text"
    }
  ]
}
```

## grading.json

Results of assertion evaluation:

```json
{
  "run_id": "eval-1-with_skill",
  "timestamp": "2024-01-15T10:30:00Z",
  "results": [
    {
      "assertion_id": 1,
      "text": "Check for expected text",
      "passed": true,
      "evidence": "Found 'expected text' in output.txt line 15"
    },
    {
      "assertion_id": 2,
      "text": "Check output format",
      "passed": false,
      "evidence": "Expected JSON array, got object"
    }
  ],
  "summary": {
    "total": 5,
    "passed": 3,
    "failed": 2,
    "pass_rate": 0.6
  }
}
```

## timing.json

Performance metrics for a run:

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3,
  "model": "claude-sonnet-4-6"
}
```

## benchmark.json

Aggregated benchmark results:

```json
{
  "skill_name": "my-skill",
  "iteration": 1,
  "timestamp": "2024-01-15T11:00:00Z",
  "configs": [
    {
      "name": "with_skill",
      "total_evals": 5,
      "total_assertions": 25,
      "passed": 20,
      "failed": 5,
      "pass_rate": 0.8,
      "mean_duration_seconds": 23.3,
      "stddev_duration_seconds": 5.2,
      "mean_tokens": 84852,
      "stddev_tokens": 12345
    },
    {
      "name": "without_skill",
      "total_evals": 5,
      "total_assertions": 25,
      "passed": 15,
      "failed": 10,
      "pass_rate": 0.6,
      "mean_duration_seconds": 18.5,
      "stddev_duration_seconds": 4.1,
      "mean_tokens": 65432,
      "stddev_tokens": 9876
    }
  ],
  "delta": {
    "pass_rate": 0.2,
    "duration_seconds": 4.8,
    "tokens": 19420
  },
  "per_eval": [
    {
      "eval_id": 1,
      "eval_name": "basic-task",
      "with_skill": {"passed": 5, "total": 5, "duration_seconds": 15.2},
      "without_skill": {"passed": 4, "total": 5, "duration_seconds": 12.1}
    }
  ]
}
```

## feedback.json

User feedback on eval results:

```json
{
  "reviews": [
    {
      "run_id": "eval-1-with_skill",
      "feedback": "The output is missing error handling for edge cases",
      "timestamp": "2024-01-15T11:30:00Z"
    },
    {
      "run_id": "eval-2-with_skill",
      "feedback": "",
      "timestamp": "2024-01-15T11:31:00Z"
    }
  ],
  "status": "complete"
}
```

## trigger_eval.json

Description optimization eval set:

```json
[
  {
    "query": "realistic user prompt with context",
    "should_trigger": true
  },
  {
    "query": "near-miss prompt that shouldn't trigger",
    "should_trigger": false
  }
]
```

## Assertion Types

| Type | Description | Value Format |
|------|-------------|--------------|
| `contains` | Output contains text | `"substring"` |
| `not_contains` | Output doesn't contain text | `"substring"` |
| `matches` | Regex match | `"pattern"` |
| `file_exists` | File was created | `"filename"` |
| `json_path` | JSON path exists | `"$.data.items"` |
| `json_value` | JSON path has value | `{"path": "$.status", "value": "success"}` |
| `custom` | Custom description | Description explains check |

## Directory Structure

```
<skill-name>-workspace/
├── evals/
│   └── evals.json
├── iteration-1/
│   ├── eval-0/
│   │   ├── eval_metadata.json
│   │   ├── with_skill/
│   │   │   ├── outputs/
│   │   │   ├── grading.json
│   │   │   └── timing.json
│   │   └── without_skill/
│   │       └── ...
│   ├── eval-1/
│   │   └── ...
│   ├── benchmark.json
│   ├── benchmark.md
│   └── feedback.json
└── iteration-2/
    └── ...
```