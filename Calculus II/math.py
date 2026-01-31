import pandas as pd
import numpy as np

# Define parameters
a = 1
b = 6
n = 5  # Must be even for Simpson's Rule
h = (b - a) / n

# Generate x values
x_values = np.linspace(a, b, n + 1)

# Prepare list for DataFrame
data = []

# Trapezoidal Rule calculations
trapezoidal_sum = 0
simpson_sum = 0

for i, x in enumerate(x_values):
    fx = np.cos(x)/x # Function f(x) = 1/x
    
    # Trapezoidal Rule
    factor_trap = 1 if i == 0 or i == n else 2
    trapezoidal_calc = factor_trap * fx
    trapezoidal_sum += trapezoidal_calc
    
    # Simpson's Rule
    if i == 0 or i == n:
        factor_simp = 1
    elif i % 2 == 1:
        factor_simp = 4
    else:
        factor_simp = 2
    simpson_calc = factor_simp * fx
    simpson_sum += simpson_calc
    
    # Append results to data list
    data.append([x, fx, factor_trap, trapezoidal_calc, factor_simp, simpson_calc])

# Create DataFrame
df = pd.DataFrame(data, columns=['x', 'f(x)', 'Trap Factor', 'Trap Calc', 'Simp Factor', 'Simp Calc'])
print(df)

# Compute final results
trapezoidal_result = (h / 2) * trapezoidal_sum
simpson_result = (h / 3) * simpson_sum

# Display results
print(f"\nh = {h}")
print(f"Trapezoidal Rule Sum = {trapezoidal_sum}, Result = {trapezoidal_result}")
print(f"Simpson's Rule Sum = {simpson_sum}, Result = {simpson_result}")

