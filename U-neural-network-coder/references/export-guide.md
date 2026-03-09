# Model Export Guide

Export neural networks for deployment and inference.

## Export Formats

| Format | Use Case | File Extension |
|--------|----------|----------------|
| PyTorch `.pt` | Python deployment | `.pt`, `.pth` |
| TorchScript | Production, C++ | `.pt` |
| ONNX | Cross-platform | `.onnx` |
| TensorFlow | TF ecosystem | `.h5`, `.pb` |
| MATLAB | Simulink integration | `.mat` |

---

## PyTorch Native

### Save/Load Checkpoint

```python
# Save
torch.save({
    'epoch': epoch,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'loss': loss,
}, 'checkpoint.pt')

# Load
checkpoint = torch.load('checkpoint.pt')
model.load_state_dict(checkpoint['model_state_dict'])
optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
epoch = checkpoint['epoch']
```

### Save Model Only

```python
# Save
torch.save(model.state_dict(), 'model_weights.pt')

# Load
model = Net(in_dim, hidden, out_dim)
model.load_state_dict(torch.load('model_weights.pt'))
model.eval()
```

---

## TorchScript

### Trace Mode (Recommended for Simple Models)

```python
# Trace with example input
example_input = torch.randn(1, in_dim)
traced_model = torch.jit.trace(model, example_input)

# Save
traced_model.save('model_traced.pt')

# Load
loaded_model = torch.jit.load('model_traced.pt')
output = loaded_model(example_input)
```

### Script Mode (For Complex Control Flow)

```python
# Script the model
scripted_model = torch.jit.script(model)

# Save
scripted_model.save('model_scripted.pt')

# Load
loaded_model = torch.jit.load('model_scripted.pt')
```

---

## ONNX

### Export to ONNX

```python
# Set to eval mode
model.eval()

# Create example input
dummy_input = torch.randn(1, in_dim)

# Export
torch.onnx.export(
    model,
    dummy_input,
    "model.onnx",
    input_names=['input'],
    output_names=['output'],
    dynamic_axes={
        'input': {0: 'batch_size'},
        'output': {0: 'batch_size'}
    },
    opset_version=11
)

# Verify
import onnx
onnx_model = onnx.load("model.onnx")
onnx.checker.check_model(onnx_model)
```

### Run ONNX Inference

```python
import onnxruntime as ort
import numpy as np

# Create session
session = ort.InferenceSession("model.onnx")

# Run inference
input_name = session.get_inputs()[0].name
output = session.run(None, {input_name: np_array_input})
```

---

## MATLAB Export

### Export Weights for Simulink

```python
import scipy.io
import numpy as np

def export_to_matlab(model, output_path):
    """Export PyTorch model weights to MATLAB .mat file."""

    weights_dict = {}
    layer_idx = 1

    for name, param in model.named_parameters():
        if 'weight' in name:
            key = f'net{layer_idx}_weight'
            weights_dict[key] = param.detach().numpy()
        elif 'bias' in name:
            key = f'net{layer_idx}_bias'
            weights_dict[key] = param.detach().numpy().reshape(-1)
            layer_idx += 1

    # Add normalization constants (adjust for your use case)
    norm_state = np.array([
        [0.0, 0.0],    # mean
        [1.0, 1.0]     # std
    ])

    norm_param = np.array([
        [0.0, 0.0, 0.0, 0.0],
        [1.0, 1.0, 1.0, 1.0]
    ])

    scipy.io.savemat(output_path, {
        'weights': weights_dict,
        'norm_state': norm_state,
        'norm_param': norm_param
    })

    print(f"Exported {layer_idx - 1} layers to {output_path}")

# Usage
export_to_matlab(model, 'node_weights.mat')
```

---

## Quantization

### Dynamic Quantization

```python
import torch.quantization

# Quantize model
quantized_model = torch.quantization.quantize_dynamic(
    model,
    {nn.Linear},
    dtype=torch.qint8
)

# Save
torch.save(quantized_model.state_dict(), 'model_quantized.pt')

# Check size reduction
original_size = sum(p.numel() * p.element_size() for p in model.parameters())
quantized_size = sum(p.numel() * p.element_size() for p in quantized_model.parameters())
print(f"Size reduction: {original_size / quantized_size:.2f}x")
```

---

## Export Checklist

- [ ] Model in `eval()` mode
- [ ] Correct input shape documented
- [ ] Test inference with exported model
- [ ] Include preprocessing/postprocessing code
- [ ] Document input/output format
- [ ] Version the exported model