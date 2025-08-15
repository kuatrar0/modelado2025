import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import math

def calcular_cota_error_global(f_expr, nodos, intervalo, num_puntos=500):
    x = sp.symbols('x')
    n = len(nodos) - 1  # grado del polinomio

    # (n+1)-ésima derivada simbólica
    derivada = f_expr
    for _ in range(n + 1):
        derivada = sp.diff(derivada, x)

    # Convertimos a función numérica
    derivada_num = sp.lambdify(x, sp.Abs(derivada), 'numpy')
    
    # Buscamos el valor máximo de |f^{(n+1)}(x)| en el intervalo
    x_vals = np.linspace(intervalo[0], intervalo[1], num_puntos)
    max_derivada = np.max(derivada_num(x_vals))

    # Construimos el término |(x - x0)(x - x1)...|
    def producto_lagrange(x_val):
        prod = 1
        for xi in nodos:
            prod *= (x_val - xi)
        return np.abs(prod)

    prod_vals = np.array([producto_lagrange(val) for val in x_vals])
    error_vals = (max_derivada / math.factorial(n + 1)) * prod_vals

    max_error = np.max(error_vals)
    x_max_error = x_vals[np.argmax(error_vals)]

    # Mostrar resultados
    print(f"Máximo valor de la derivada |f^{n+1}(x)| ≈ {max_derivada:.6f}")
    print(f"Máximo valor estimado del error: {max_error:.6f}")
    print(f"Ocurre en x ≈ {x_max_error:.6f}")

    # Gráfico
    plt.plot(x_vals, error_vals, label='Cota de error global')
    plt.axvline(x_max_error, color='red', linestyle='--', label=f'Máximo en x ≈ {x_max_error:.2f}')
    plt.title(f'Cota de Error Global para interpolación de grado {n}')
    plt.xlabel('x')
    plt.ylabel('Error estimado')
    plt.grid(True)
    plt.legend()
    plt.show()

# Ejemplo con f(x) = sin(x)
if __name__ == "__main__":
    x = sp.symbols('x')
    f_expr = sp.sin(sp.pi*x)
    nodos = [0, 0.5, 1, 1.5]  # nodos simbólicos (usa sp.pi para mantener precisión)
    intervalo = (0, 1.5)  # intervalo en que evaluar la cota

    calcular_cota_error_global(f_expr, nodos, intervalo)