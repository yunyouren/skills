# Troubleshooting Guide

Common issues and solutions for MATLAB/Simulink workflows.

## Simulation Errors

### Model Not Found

```
Error: Unable to open file 'model_name.slx'
```

**Solutions:**
1. Check current working directory
2. Add model directory to path
3. Use full path

```matlab
% Add to path
addpath('/path/to/models');

% Or use full path
load_system('/full/path/to/model.slx');
```

### Variable Not in Workspace

```
Error: Undefined function or variable 'param_name'
```

**Solutions:**
```matlab
% Check if variable exists
if ~exist('param_name', 'var')
    error('param_name not found in workspace');
end

% Load from file
load('params.mat', 'param_name');

% Or assign directly
assignin('base', 'param_name', value);
```

### Solver Step Size Issues

```
Warning: Unable to reduce step size without violating minimum step size
```

**Solutions:**
```matlab
% Increase minimum step
set_param('model', 'MinStep', '1e-6');

% Or use different solver
set_param('model', 'Solver', 'ode15s');
```

## Neural Network Integration

### Weight File Validation Fails

**Error:** `[FAIL] Layer chain mismatch`

**Cause:** Layer dimensions don't chain properly

**Solution:**
```bash
# Re-export weights from Python with correct dimensions
python export_weights.py --verify-chain
```

**Error:** `[FAIL] Missing norm_state`

**Cause:** Normalization constants not exported

**Solution:**
```python
# Add to export script
scipy.io.savemat('node_weights.mat', {
    'weights': weights_dict,
    'norm_state': norm_state,  # Add this
    'norm_param': norm_param,  # Add this
})
```

### MATLAB Function Block Errors

**Error:** `Input port width mismatch`

**Diagnosis:**
```matlab
% In MATLAB Function block, add debug output
function y = f_neural(x, weights)
    coder.extrinsic('disp');
    disp(['Input width: ', num2str(size(x, 2))]);
    % Continue with function
end
```

**Solutions:**
- Adjust Mux block output width
- Check concatenation order: `[state; params; control]`
- Verify weight matrix dimensions

## Python-MATLAB Bridge

### Engine Won't Start

```
matlab.engine.EngineError: MATLAB engine failed to start
```

**Solutions:**
1. Verify MATLAB is installed
2. Check PATH includes MATLAB bin directory
3. Install MATLAB Engine API

```bash
# Install MATLAB Engine
cd /path/to/matlab/extern/engines/python
python setup.py install
```

### Session Timeout

```
matlab.engine.EngineError: Session timeout
```

**Solutions:**
```python
# Increase timeout
eng = matlab.engine.start_matlab(background=True)
eng.wait(timeout=60)  # 60 seconds

# Or run async
future = eng.sim('model', async=True, nargout=0)
future.result(timeout=120)  # Wait up to 2 minutes
```

### Data Type Mismatch

```
TypeError: unsupported data type
```

**Solutions:**
```python
# Convert to MATLAB double explicitly
import matlab
data = matlab.double([[1.0, 2.0], [3.0, 4.0]])
eng.workspace['matrix'] = data

# For strings
eng.workspace['str'] = 'model_name'
```

## Code Generation Issues

### Incompatible Block

```
Error: Block 'model/block_name' is not supported for code generation
```

**Solutions:**
1. Check block compatibility list
2. Use supported alternative
3. Replace with MATLAB Function block

### Data Store Memory

```
Error: Data Store Memory block not found
```

**Solution:**
```matlab
% Define data store
set_param('model', 'DataStoreMemory', 'store_name');
```

## Performance Issues

### Slow Simulation

**Diagnosis:**
```matlab
% Profile simulation
profile on;
sim('model');
profile viewer;
```

**Solutions:**
- Use fixed-step solver for faster execution
- Reduce logging overhead
- Preallocate output arrays

```matlab
% Use fixed step
set_param('model', 'SolverType', 'Fixed-step');
set_param('model', 'FixedStep', '0.01');
```

### Memory Exhaustion

**Solutions:**
```matlab
% Clear large variables
clear large_matrix

% Use sparse matrices
A = sparse(A_dense);

% Limit output logging
set_param('model', 'SaveOutput', 'off');
```