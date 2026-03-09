---
name: U-matlab-simulink-coder
description: Build, modify, and tune MATLAB and Simulink workflows for control systems, circuit simulation, and neural-ODE integration. Use when requests mention MATLAB scripts (.m), Simulink models (.slx), MATLAB Engine automation, set_param/load_system, simulation data collection, parameter tuning, solver configuration, or Python-MATLAB bridge integration.
version: 1.1.0
author: Integrated
platforms: [claude-code, codex]
category: engineering
tags: [matlab, simulink, control-systems, simulation, neural-ode, code-generation]
---

# U-MATLAB Simulink Coder

Build, modify, and tune MATLAB/Simulink workflows for control systems, circuit simulation, and neural-ODE integration.

## Core Workflow

```
Identify → Setup → Implement → Validate → Tune → Export
```

### Phase 1: Identify Target

Determine the artifact type:
- **MATLAB script** (`.m`) - Data processing, algorithm implementation
- **Simulink model** (`.slx`) - System simulation, control design
- **Python-MATLAB bridge** - Cross-platform integration

### Phase 2: Setup Environment

1. Confirm MATLAB version and required toolboxes
2. Verify Simulink model paths
3. Check workspace variable dependencies
4. Validate `.mat` weight files (if neural network)

### Phase 3: Implement

Create minimal runnable path first:
```matlab
load_system('model_name');      % Load model
set_param('model_name', ...);   % Set parameters
sim('model_name');              % Run simulation
```

### Phase 4: Validate

Run validation script before simulation:
```bash
python scripts/validate_matlab_simulink_bridge.py \
  --mat path/to/weights.mat \
  --expected-input-dim 7 \
  --expected-state-dim 2 \
  --expected-param-dim 4
```

### Phase 5: Tune

Iterate on parameters with repeatable sweeps. See [Tuning Guide](references/tuning-guide.md).

### Phase 6: Export

Save reproducible outputs with consistent naming across Python/MATLAB/Simulink.

---

## Implementation Patterns

### MATLAB Script Pattern

```matlab
% Resolve paths from script directory
scriptPath = fileparts(mfilename('fullpath'));
addpath(fullfile(scriptPath, 'lib'));

% Check required fields before use
requiredFields = {'weights', 'norm_state', 'norm_param'};
for f = requiredFields
    if ~isfield(data, f{1})
        error('Missing required field: %s', f{1});
    end
end
```

### Simulink Integration Pattern

- Ensure MATLAB Function block input dimension matches model design
- Keep feature concatenation order fixed: `[state; params; control]`
- Use scalar or column-vector conventions for block ports
- Align block variable names with workspace variables

### Python MATLAB Engine Pattern

```python
import matlab.engine

# Start engine once, reuse for batch simulations
eng = matlab.engine.start_matlab()

# Push parameters to workspace
eng.workspace['param1'] = matlab.double([value])

# Run simulation
eng.set_param('model', 'StopTime', '10', nargout=0)
eng.sim('model', nargout=0)

# Read outputs
result = eng.workspace['yout']
```

---

## Validation

Use the bundled validation script to check `.mat` weight files:

```bash
python scripts/validate_matlab_simulink_bridge.py \
  --mat weights.mat \
  --expected-input-dim 7 \
  --expected-state-dim 2 \
  --expected-param-dim 4
```

**Validation checks:**
- Layer weight/bias dimensions
- Layer chain consistency
- `norm_state` and `norm_param` presence
- Input/output dimension matching

---

## Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Simulation unstable | Step size too large | Reduce solver step size |
| Shape mismatch in MATLAB Function | Dimension mismatch | Print input shapes before matrix multiply |
| Missing workspace variable | Variable not loaded | Add explicit `assignin` or load step |
| Neural ODE output wrong | Normalization mismatch | Verify norm constants from export |

See [Troubleshooting Guide](references/troubleshooting.md) for detailed solutions.

---

## Output Standards

- Return runnable `.m` or `.py` code (not pseudocode)
- Keep variable naming compatible with existing model files
- Include explicit checks for required workspace variables
- Ensure scripts run from command line without GUI steps

---

## References

- [Tuning Guide](references/tuning-guide.md) - Parameter tuning strategies
- [Troubleshooting](references/troubleshooting.md) - Common issues and solutions
- [Examples](references/examples.md) - Code templates

---

## Bundled Scripts

| Script | Purpose |
|--------|---------|
| `scripts/validate_matlab_simulink_bridge.py` | Validate `.mat` weight files for Neural ODE integration |