# Training Diagnosis Guide

Troubleshooting neural network training issues.

## Loss Not Decreasing

### Symptoms
- Loss stays flat or increases
- Gradients near zero or NaN

### Causes & Solutions

| Cause | Solution |
|-------|----------|
| Wrong label format | Check `y.shape` matches `pred.shape` |
| Loss function mismatch | Classification → CrossEntropy, Regression → MSELoss |
| Learning rate too high | Reduce by 10x: `lr = 1e-4` |
| Learning rate too low | Increase: `lr = 1e-3` |
| Bad initialization | Use `nn.init.xavier_uniform_` or `kaiming` |

### Verify Pipeline

```python
# Overfit on tiny subset to verify pipeline
tiny_subset = train_dataset[:10]
tiny_loader = DataLoader(tiny_subset, batch_size=10)

# Should reach near-zero loss quickly
for epoch in range(100):
    for batch in tiny_loader:
        loss = train_step(model, batch, optimizer, loss_fn, device)
    print(f"Epoch {epoch}: {loss:.6f}")
```

---

## Overfitting

### Symptoms
- Training loss decreases, validation loss increases
- Large gap between train and val metrics

### Solutions

```python
# 1. Add dropout
nn.Dropout(p=0.3)

# 2. Add weight decay
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-4)

# 3. Reduce model size
hidden = 64  # Instead of 256

# 4. Data augmentation (for images)
transforms.RandomHorizontalFlip()
transforms.RandomRotation(10)

# 5. Early stopping
patience = 10
if val_loss < best_val_loss:
    best_val_loss = val_loss
    counter = 0
else:
    counter += 1
    if counter >= patience:
        print("Early stopping")
        break
```

---

## Training Unstable

### Symptoms
- Loss spikes or oscillates
- NaN values appear

### Solutions

```python
# 1. Lower learning rate
optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)

# 2. Gradient clipping
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

# 3. Normalize inputs
mean = X_train.mean()
std = X_train.std()
X_normalized = (X - mean) / std

# 4. Use learning rate scheduler
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
    optimizer, mode='min', factor=0.5, patience=5
)
scheduler.step(val_loss)

# 5. Batch normalization
nn.BatchNorm1d(hidden_dim)
```

---

## Slow Training

### Diagnosis

```python
# Profile data loading
import time

start = time.time()
for batch in train_loader:
    pass
print(f"Data loading time: {time.time() - start:.2f}s")

# Profile forward pass
start = time.time()
with torch.no_grad():
    model(batch[0])
print(f"Forward pass time: {time.time() - start:.2f}s")
```

### Solutions

```python
# 1. Increase batch size
batch_size = 128  # Or max that fits in GPU memory

# 2. Enable num_workers
train_loader = DataLoader(
    train_dataset,
    batch_size=64,
    shuffle=True,
    num_workers=4,  # CPU cores
    pin_memory=True  # Faster GPU transfer
)

# 3. Mixed precision training
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()

with autocast():
    pred = model(x)
    loss = loss_fn(pred, y)

scaler.scale(loss).backward()
scaler.step(optimizer)
scaler.update()

# 4. Use .to(device) efficiently
# Move to GPU once, not repeatedly
```

---

## Gradient Issues

### Vanishing Gradients

```python
# Check gradient magnitudes
for name, param in model.named_parameters():
    if param.grad is not None:
        print(f"{name}: {param.grad.abs().mean():.6f}")

# Solutions:
# 1. Use residual connections
class ResidualBlock(nn.Module):
    def forward(self, x):
        return x + self.layers(x)

# 2. Use appropriate activation (ReLU, GELU)
# 3. Use LayerNorm or BatchNorm
```

### Exploding Gradients

```python
# Clip gradients
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

# Or clip by value
torch.nn.utils.clip_grad_value_(model.parameters(), clip_value=0.5)
```

---

## Memory Issues

### Out of Memory

```python
# 1. Reduce batch size
batch_size = 16

# 2. Use gradient accumulation
accumulation_steps = 4
optimizer.zero_grad()

for i, batch in enumerate(train_loader):
    loss = train_step_no_optimizer_step(batch)
    loss = loss / accumulation_steps
    loss.backward()

    if (i + 1) % accumulation_steps == 0:
        optimizer.step()
        optimizer.zero_grad()

# 3. Clear cache
torch.cuda.empty_cache()

# 4. Use .detach() on tensors you don't need gradients for
```

---

## Common Error Messages

| Error | Cause | Fix |
|-------|-------|-----|
| `mat1 and mat2 shapes cannot be multiplied` | Dimension mismatch | Check `x.shape` and layer input dim |
| `Expected input batch_size (X) to match target batch_size (Y)` | Batch mismatch | Check data loader output |
| `CUDA out of memory` | GPU memory full | Reduce batch size |
| `RuntimeError: CUDA error: device-side assert triggered` | Index out of bounds | Check label range |