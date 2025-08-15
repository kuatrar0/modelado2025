import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate
import sympy as sp

def euler_method(f, x_vals, y0):
    y_vals = [y0]
    for i in range(1, len(x_vals)):
        h = x_vals[i] - x_vals[i - 1]
        y_new = y_vals[-1] + h * f(x_vals[i - 1], y_vals[-1])
        y_vals.append(y_new)
    return y_vals

def rk4_method(f, x_vals, y0):
    y_vals = [y0]
    for i in range(1, len(x_vals)):
        h = x_vals[i] - x_vals[i - 1]
        x_i = x_vals[i - 1]
        y_i = y_vals[-1]
        k1 = f(x_i, y_i)
        k2 = f(x_i + h/2, y_i + h * k1 / 2)
        k3 = f(x_i + h/2, y_i + h * k2 / 2)
        k4 = f(x_i + h, y_i + h * k3)
        y_new = y_i + h * (k1 + 2*k2 + 2*k3 + k4) / 6
        y_vals.append(y_new)
    return y_vals

def solve_and_compare(f_numeric, exact_sol, x_vals, y0):
    exact_vals = [exact_sol(x) for x in x_vals]
    euler_vals = euler_method(f_numeric, x_vals, y0)
    rk4_vals = rk4_method(f_numeric, x_vals, y0)

    table = [["k", "x", "Exacta", "Euler", "RK4"]]
    for i in range(len(x_vals)):
        x_label = f"{x_vals[i]:.4f}"
        table.append([
            i,
            x_label,
            round(exact_vals[i], 6),
            round(euler_vals[i], 6),
            round(rk4_vals[i], 6)
        ])

    print(tabulate(table, headers="firstrow", tablefmt="grid"))
    
    # Graficar soluciones
    plt.plot(x_vals, exact_vals, label='Exacta', linewidth=2)
    plt.plot(x_vals, euler_vals, 'o--', label='Euler')
    plt.plot(x_vals, rk4_vals, 's--', label='RK4')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Soluciones de la EDO')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    # EDO: dy/dx = cos(x) + x, y(0) = 1
    y0 = 1
    h = np.pi / 8
    x_vals = np.arange(0, np.pi / 2 + h, h)

    # Definición numérica de f(x, y)
    def f_numeric(x, y):
        return np.cos(x) + x

    # Solución exacta: y(x) = sin(x) + x**2 / 2 + 1
    def exact_sol(x):
        return np.sin(x) + 0.5 * x**2 + 1

    solve_and_compare(f_numeric, exact_sol, x_vals, y0)

if __name__ == "__main__":
    main()
