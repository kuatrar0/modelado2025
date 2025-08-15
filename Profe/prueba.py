import sympy as sp

x = sp.symbols('x')
p = x*(x - 0.5)*(x - 1)*(x - 1.5)
dp = sp.diff(p, x)

print(f"p(x) = {p}")
print(f"p'(x) = {dp}")