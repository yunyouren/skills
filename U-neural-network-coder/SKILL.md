---
name: U-neural-network-coder
description: Build, train, debug, and optimize neural networks with PyTorch. Use when requests mention neural networks, deep learning, model architecture, training loops, loss functions, dataloaders, overfitting diagnosis, hyperparameter tuning, model export, or inference deployment.
version: 1.1.0
author: Integrated
platforms: [claude-code, codex]
category: machine-learning
tags: [pytorch, neural-network, deep-learning, training, model-export]
---

# U-Neural Network Coder

Build, train, debug, and optimize neural networks with PyTorch for research and engineering tasks.

## Core Workflow

```
Identify → Prepare → Build → Train → Diagnose → Export
```

### Phase 1: Identify Task Type

Determine the problem category:
- **Classification** - Image, text, tabular categories
- **Regression** - Continuous value prediction
- **Sequence Modeling** - Time series, language
- **Dynamical Systems** - ODE/DAE modeling

### Phase 2: Prepare Data

1. Confirm data shape and target shape
2. Create train/validation/test splits
3. Build DataLoader with appropriate settings
4. Normalize inputs and targets

### Phase 3: Build Model

1. Start with a baseline architecture
2. Ensure end-to-end training works first
3. Then increase complexity

### Phase 4: Train

Implement stable training with:
- Deterministic seeds
- Metric tracking
- Checkpointing

### Phase 5: Diagnose

Analyze training curves and adjust. See [Diagnosis Guide](references/diagnosis-guide.md).

### Phase 6: Export

Save artifacts for deployment. See [Export Guide](references/export-guide.md).

---

## Implementation Defaults

| Default | Reason |
|---------|--------|
| PyTorch first | Unless user requests otherwise |
| Deterministic seeds | Reproducibility |
| Single initialization block | Model, optimizer, scheduler, loss together |
| One forward/loss path | Easy debugging |
| Separated modules | Data, model, training, evaluation, export |

---

## Training Checklist

- [ ] DataLoader with shuffle (train) / no shuffle (eval)
- [ ] Device handling with CUDA fallback
- [ ] `model.train()` / `model.eval()` states
- [ ] `optimizer.zero_grad()` → forward → loss → backward → step
- [ ] Gradient clipping (optional)
- [ ] Validation metrics per epoch
- [ ] Best model checkpointing
- [ ] Early stopping on plateau

---

## Quick Templates

### Minimal Model

```python
import torch
import torch.nn as nn

class Net(nn.Module):
    def __init__(self, in_dim: int, hidden: int, out_dim: int):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(in_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, hidden),
            nn.ReLU(),
            nn.Linear(hidden, out_dim),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.layers(x)
```

### Training Step

```python
def train_step(model, batch, optimizer, loss_fn, device):
    x, y = batch
    x, y = x.to(device), y.to(device)
    model.train()
    optimizer.zero_grad()
    pred = model(x)
    loss = loss_fn(pred, y)
    loss.backward()
    optimizer.step()
    return loss.item()
```

More templates in [Code Examples](references/examples.md).

---

## Common Issues

| Issue | Quick Fix |
|-------|-----------|
| Loss not decreasing | Check labels, reduce LR 10x |
| Overfitting | Add dropout, weight decay |
| Unstable training | Lower LR, gradient clipping |
| Slow training | Increase batch, enable mixed precision |

See [Diagnosis Guide](references/diagnosis-guide.md) for detailed solutions.

---

## Output Standards

- Return runnable code (not pseudocode)
- Include complete imports
- Ensure CLI executable with arguments
- Use explicit, readable variable names

---

## References

- [Diagnosis Guide](references/diagnosis-guide.md) - Training troubleshooting
- [Export Guide](references/export-guide.md) - Model export and deployment
- [Examples](references/examples.md) - Complete code templates