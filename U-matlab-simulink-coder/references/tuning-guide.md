# Tuning Guide

Parameter tuning strategies for MATLAB/Simulink simulations.

## Data Quality Issues

### Data Nearly Static

**Symptoms:** Output doesn't change across simulation runs

**Solutions:**
1. Disable unwanted steady-state initial state loading
2. Shorten horizon to focus on transient dynamics
3. Widen parameter sampling range

```matlab
% Disable steady-state loading
set_param('model/InitialState', 'Value', '[]');

% Shorten simulation time
set_param('model', 'StopTime', '2');
```

### Simulation Unstable

**Symptoms:** Output diverges, NaN values, or crashes

**Solutions:**
1. Reduce step size
2. Adjust solver type and tolerances
3. Verify parameter units and scaling

```matlab
% Reduce step size
set_param('model', 'Solver', 'ode45');
set_param('model', 'MaxStep', '0.001');

% Tighten tolerances
set_param('model', 'RelTol', '1e-6');
set_param('model', 'AbsTol', '1e-8');
```

## Neural Network Integration

### Shape Mismatch in MATLAB Function Block

**Symptoms:** Error like "Inner matrix dimensions must agree"

**Debugging:**
```matlab
% Print input dimensions
function y = f_neural(x)
    disp(['Input size: ' num2str(size(x))]);
    % ... rest of function
end
```

**Common causes:**
- Weight matrix orientation wrong (transpose needed)
- Bias vector shape mismatch
- Normalization vector dimensions

### Neural ODE Mismatch Between Python and Simulink

**Checklist:**
1. Verify activation function parity (e.g., Tanh vs tanh)
2. Verify normalization constants from exported `.mat` files
3. Verify feature order parity between training and deployment

```python
# Python: Check exported values
import scipy.io
data = scipy.io.loadmat('node_weights.mat')
print('norm_state:', data['norm_state'].shape)
print('norm_param:', data['norm_param'].shape)
```

## Parameter Sweeps

### Basic Sweep Pattern

```matlab
params = [0.1, 0.5, 1.0, 2.0];
results = cell(length(params), 1);

for i = 1:length(params)
    set_param('model/gain', 'Value', num2str(params(i)));
    simOut = sim('model');
    results{i} = simOut.yout;
end
```

### Parallel Sweep with Python

```python
import matlab.engine
from concurrent.futures import ThreadPoolExecutor

def run_sim(params):
    eng = matlab.engine.start_matlab()
    eng.workspace['p'] = matlab.double([params])
    eng.sim('model', nargout=0)
    result = eng.workspace['yout']
    eng.quit()
    return result

with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(run_sim, p) for p in param_list]
    results = [f.result() for f in futures]
```

## Solver Selection Guide

| Solver | Best For | Configuration |
|--------|----------|---------------|
| ode45 | General purpose | Default, moderate accuracy |
| ode15s | Stiff systems | Variable step, higher order |
| ode1 | Fixed step | Real-time, code generation |
| ode4 | Fixed step, 4th order | Balance of accuracy and speed |

```matlab
% For stiff systems
set_param('model', 'Solver', 'ode15s');
set_param('model', 'MaxOrder', '5');
```

## Normalization Best Practices

### Keep Normalization in One Place

```matlab
% normalization.m - Single source of truth
function [normed, params] = normalize_state(state, param)
    persistent norm_state norm_param

    if isempty(norm_state)
        data = load('node_weights.mat');
        norm_state = data.norm_state;
        norm_param = data.norm_param;
    end

    normed = (state - norm_state(1,:)) ./ norm_state(2,:);
    params = (param - norm_param(1,:)) ./ norm_param(2,:);
end
```

### De-normalization for Output

```matlab
function state = denormalize_output(normed)
    persistent norm_state
    if isempty(norm_state)
        data = load('node_weights.mat');
        norm_state = data.norm_state;
    end
    state = normed .* norm_state(2,:) + norm_state(1,:);
end
```