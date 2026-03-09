#!/usr/bin/env python3
"""
Validate PyTorch model weights and architecture.
Usage: python validate_model.py --model model.pt --config config.json
"""

import argparse
import json
import sys
from pathlib import Path

import torch
import torch.nn as nn


def parse_args():
    parser = argparse.ArgumentParser(description="Validate PyTorch model")
    parser.add_argument("--model", required=True, help="Path to model weights (.pt)")
    parser.add_argument("--config", help="Path to config JSON with expected dimensions")
    parser.add_argument("--input-dim", type=int, help="Expected input dimension")
    parser.add_argument("--output-dim", type=int, help="Expected output dimension")
    return parser.parse_args()


def validate_weights(model_path: Path):
    """Validate model weights file."""
    if not model_path.exists():
        print(f"[FAIL] Model file not found: {model_path}")
        return None

    try:
        checkpoint = torch.load(model_path, map_location='cpu')
        print(f"[OK] Loaded model from {model_path}")
        return checkpoint
    except Exception as e:
        print(f"[FAIL] Error loading model: {e}")
        return None


def analyze_checkpoint(checkpoint):
    """Analyze checkpoint structure."""
    print("\n--- Checkpoint Analysis ---")

    if isinstance(checkpoint, dict):
        print(f"Keys: {list(checkpoint.keys())}")

        if 'model_state_dict' in checkpoint:
            state_dict = checkpoint['model_state_dict']
        elif 'state_dict' in checkpoint:
            state_dict = checkpoint['state_dict']
        else:
            state_dict = checkpoint
    else:
        state_dict = checkpoint

    if hasattr(state_dict, 'items'):
        print("\nLayer shapes:")
        for name, param in state_dict.items():
            if hasattr(param, 'shape'):
                print(f"  {name}: {tuple(param.shape)}")

    return state_dict


def check_dimensions(state_dict, expected_input_dim=None, expected_output_dim=None):
    """Check if dimensions match expectations."""
    all_ok = True

    # Find input dimension (first layer weight shape[1])
    # Find output dimension (last layer weight shape[0])

    weight_keys = [k for k in state_dict.keys() if 'weight' in k]

    if weight_keys:
        first_weight = state_dict[weight_keys[0]]
        last_weight = state_dict[weight_keys[-1]]

        if hasattr(first_weight, 'shape'):
            input_dim = first_weight.shape[1]
            print(f"[INFO] Input dimension: {input_dim}")

            if expected_input_dim is not None:
                if input_dim == expected_input_dim:
                    print(f"[OK] Input dimension matches expected {expected_input_dim}")
                else:
                    print(f"[FAIL] Input dimension mismatch: got {input_dim}, expected {expected_input_dim}")
                    all_ok = False

        if hasattr(last_weight, 'shape'):
            output_dim = last_weight.shape[0]
            print(f"[INFO] Output dimension: {output_dim}")

            if expected_output_dim is not None:
                if output_dim == expected_output_dim:
                    print(f"[OK] Output dimension matches expected {expected_output_dim}")
                else:
                    print(f"[FAIL] Output dimension mismatch: got {output_dim}, expected {expected_output_dim}")
                    all_ok = False

    return all_ok


def check_layer_consistency(state_dict):
    """Check if layer dimensions are consistent."""
    all_ok = True

    # Group weights and biases by layer
    layers = {}
    for name, param in state_dict.items():
        if 'weight' in name:
            layer_name = name.replace('.weight', '')
            if layer_name not in layers:
                layers[layer_name] = {}
            layers[layer_name]['weight'] = param
        elif 'bias' in name:
            layer_name = name.replace('.bias', '')
            if layer_name not in layers:
                layers[layer_name] = {}
            layers[layer_name]['bias'] = param

    # Check weight-bias consistency
    for layer_name, layer_data in layers.items():
        if 'weight' in layer_data and 'bias' in layer_data:
            w = layer_data['weight']
            b = layer_data['bias']
            if hasattr(w, 'shape') and hasattr(b, 'shape'):
                if w.shape[0] == b.shape[0]:
                    print(f"[OK] {layer_name}: weight {w.shape} matches bias {b.shape}")
                else:
                    print(f"[FAIL] {layer_name}: weight out_dim {w.shape[0]} != bias dim {b.shape[0]}")
                    all_ok = False

    return all_ok


def main():
    args = parse_args()

    model_path = Path(args.model)

    print(f"=== Validating Model: {model_path.name} ===\n")

    # Load checkpoint
    checkpoint = validate_weights(model_path)
    if checkpoint is None:
        return 1

    # Analyze structure
    state_dict = analyze_checkpoint(checkpoint)

    # Check dimensions
    all_ok = True

    if hasattr(state_dict, 'items'):
        all_ok &= check_dimensions(
            state_dict,
            args.input_dim,
            args.output_dim
        )
        all_ok &= check_layer_consistency(state_dict)

    # Summary
    print("\n=== Summary ===")
    if all_ok:
        print("[PASS] All validations passed")
        return 0
    else:
        print("[FAIL] Some validations failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())