import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import derivative
from tabulate import tabulate

# Método de Newton-Raphson
def newton_raphson(f, valor_inicial, iteraciones=100, tolerancia=1e-6, precision=5):
    x = valor_inicial
    results = []
    for i in range(iteraciones):
        fx = round(f(x), precision)
        dfx = round(derivative(f, x, dx=tolerancia), precision)
        if dfx == 0:
            raise ValueError("La derivada es cero. El método no puede continuar.")
        x_new = round(x - fx / dfx, precision)
        results.append([i+1, x, fx, dfx, x_new])
        print(tabulate(results, headers=["Iteración", "x", "f(x)", "f'(x)", "Resultado"], tablefmt="grid"))
        if abs(x_new - x) < tolerancia:
            return x_new
        x = x_new
    raise ValueError("El método no convergió o faltan iteraciones.")

def graficar(f, raiz):
    # Graficar la función
    x = np.linspace(0, 3, 400)
    y = f(x)

    plt.plot(x, y, label='$f(x)$')
    plt.axhline(0, color='black',linewidth=0.5)
    plt.axvline(0, color='black',linewidth=0.5)
    plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
    
    # Marcar la raíz encontrada
    plt.plot(raiz, f(raiz), 'ro', label=f'Raíz: x = {raiz:.5f}')
    
    # Añadir leyenda y mostrar la gráfica
    plt.legend()
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('Gráfica de la función y su raíz')
    plt.show()

# Definir la función para la cual quieres encontrar la raíz
def f(x):
    return x**3 - x-4

# Valor inicial
valor_inicial = 1.0

# Encontrar la raíz utilizando el método de Newton-Raphson
raiz = newton_raphson(f, valor_inicial)

# Imprimir la raíz encontrada
print(f"La raíz encontrada es: {raiz}")

# Graficar la función y la raíz
graficar(f, raiz)
