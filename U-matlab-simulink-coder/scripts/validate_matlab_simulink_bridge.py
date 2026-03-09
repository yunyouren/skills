import argparse
import re
import sys
from pathlib import Path

import numpy as np
import scipy.io


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mat", required=True, help="Path to node_weights.mat")
    parser.add_argument("--expected-input-dim", type=int, default=7)
    parser.add_argument("--expected-state-dim", type=int, default=2)
    parser.add_argument("--expected-param-dim", type=int, default=4)
    return parser.parse_args()


def normalize_name(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]", "", name).lower()


def flatten_numeric_fields(obj, prefix=""):
    items = {}
    if isinstance(obj, np.ndarray) and obj.dtype.names:
        for field in obj.dtype.names:
            value = obj[field]
            key = f"{prefix}_{field}" if prefix else field
            items.update(flatten_numeric_fields(value, key))
        return items
    if isinstance(obj, np.ndarray) and obj.dtype == object:
        for idx, value in enumerate(obj.flat):
            key = f"{prefix}_{idx}" if prefix else str(idx)
            items.update(flatten_numeric_fields(value, key))
        return items
    if hasattr(obj, "_fieldnames"):
        for field in obj._fieldnames:
            value = getattr(obj, field)
            key = f"{prefix}_{field}" if prefix else field
            items.update(flatten_numeric_fields(value, key))
        return items
    if isinstance(obj, dict):
        for key0, value in obj.items():
            key = f"{prefix}_{key0}" if prefix else str(key0)
            items.update(flatten_numeric_fields(value, key))
        return items
    if isinstance(obj, np.ndarray) and np.issubdtype(obj.dtype, np.number):
        items[prefix] = np.asarray(obj)
        return items
    if np.isscalar(obj) and isinstance(obj, (int, float, np.number)):
        items[prefix] = np.asarray([obj], dtype=float)
        return items
    return items


def detect_layers(flat_weights):
    normalized = {normalize_name(k): v for k, v in flat_weights.items()}
    layer_map = {}
    for key, value in normalized.items():
        m_w = re.search(r"net(\d+)weight", key)
        m_b = re.search(r"net(\d+)bias", key)
        if m_w:
            lid = int(m_w.group(1))
            layer_map.setdefault(lid, {})["weight"] = np.asarray(value)
        if m_b:
            lid = int(m_b.group(1))
            layer_map.setdefault(lid, {})["bias"] = np.asarray(value)
    return layer_map


def fail(msg):
    print(f"[FAIL] {msg}")
    return False


def ok(msg):
    print(f"[OK] {msg}")
    return True


def validate(mat_path: Path, expected_input_dim: int, expected_state_dim: int, expected_param_dim: int):
    if not mat_path.exists():
        print(f"[FAIL] File not found: {mat_path}")
        return 1
    data = scipy.io.loadmat(str(mat_path), squeeze_me=True, struct_as_record=False)
    if "weights" not in data:
        print("[FAIL] Missing 'weights' field in .mat")
        return 1
    all_ok = True
    flat_weights = flatten_numeric_fields(data["weights"], "")
    flat_weights = {k: v for k, v in flat_weights.items() if k}
    if not flat_weights:
        print("[FAIL] No numeric weights found under 'weights'")
        return 1
    layer_map = detect_layers(flat_weights)
    if not layer_map:
        print("[FAIL] No layer weights detected with pattern net{n}_weight/net{n}_bias")
        return 1
    layer_ids = sorted(layer_map.keys())
    print(f"[INFO] Detected layer ids: {layer_ids}")
    for lid in layer_ids:
        part = layer_map[lid]
        if "weight" not in part:
            all_ok = fail(f"Layer net_{lid} missing weight") and all_ok
            continue
        if "bias" not in part:
            all_ok = fail(f"Layer net_{lid} missing bias") and all_ok
            continue
        w = np.asarray(part["weight"])
        b = np.asarray(part["bias"]).reshape(-1)
        if w.ndim != 2:
            all_ok = fail(f"Layer net_{lid} weight is not 2D, got shape {w.shape}") and all_ok
        else:
            ok(f"Layer net_{lid} weight shape {tuple(w.shape)}")
        if b.ndim != 1:
            all_ok = fail(f"Layer net_{lid} bias is not 1D after reshape") and all_ok
        if w.ndim == 2 and w.shape[0] != b.shape[0]:
            all_ok = fail(f"Layer net_{lid} bias length {b.shape[0]} != weight out dim {w.shape[0]}") and all_ok
    ordered = sorted([(lid, layer_map[lid]["weight"]) for lid in layer_ids if "weight" in layer_map[lid]], key=lambda x: x[0])
    if ordered:
        first_w = np.asarray(ordered[0][1])
        last_w = np.asarray(ordered[-1][1])
        if first_w.ndim == 2 and first_w.shape[1] == expected_input_dim:
            ok(f"First layer input dim matches expected {expected_input_dim}")
        else:
            all_ok = fail(
                f"First layer input dim mismatch, expected {expected_input_dim}, got {first_w.shape[1] if first_w.ndim == 2 else 'non-2d'}"
            ) and all_ok
        if last_w.ndim == 2 and last_w.shape[0] == expected_state_dim:
            ok(f"Last layer output dim matches expected state dim {expected_state_dim}")
        else:
            all_ok = fail(
                f"Last layer output dim mismatch, expected {expected_state_dim}, got {last_w.shape[0] if last_w.ndim == 2 else 'non-2d'}"
            ) and all_ok
    for i in range(len(ordered) - 1):
        current_w = np.asarray(ordered[i][1])
        next_w = np.asarray(ordered[i + 1][1])
        if current_w.ndim == 2 and next_w.ndim == 2 and current_w.shape[0] != next_w.shape[1]:
            all_ok = fail(
                f"Layer chain mismatch between net_{ordered[i][0]} out {current_w.shape[0]} and net_{ordered[i + 1][0]} in {next_w.shape[1]}"
            ) and all_ok
    if "norm_state" not in data:
        all_ok = fail("Missing norm_state in .mat") and all_ok
    else:
        norm_state = np.asarray(data["norm_state"]).reshape(-1)
        if norm_state.shape[0] < expected_state_dim:
            all_ok = fail(f"norm_state length {norm_state.shape[0]} < expected {expected_state_dim}") and all_ok
        else:
            ok(f"norm_state length {norm_state.shape[0]}")
    if "norm_param" not in data:
        all_ok = fail("Missing norm_param in .mat") and all_ok
    else:
        norm_param = np.asarray(data["norm_param"]).reshape(-1)
        if norm_param.shape[0] < expected_param_dim:
            all_ok = fail(f"norm_param length {norm_param.shape[0]} < expected {expected_param_dim}") and all_ok
        else:
            ok(f"norm_param length {norm_param.shape[0]}")
    if all_ok:
        print("[PASS] Validation succeeded")
        return 0
    print("[FAIL] Validation failed")
    return 2


def main():
    args = parse_args()
    exit_code = validate(
        mat_path=Path(args.mat),
        expected_input_dim=args.expected_input_dim,
        expected_state_dim=args.expected_state_dim,
        expected_param_dim=args.expected_param_dim,
    )
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
