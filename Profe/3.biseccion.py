import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate

# Método de Bisección
def biseccion(f, a, b, iteraciones=100, tolerancia=1e-6, precision=5):
    if f(a) * f(b) >= 0:
        raise ValueError("La función debe tener signos opuestos en los extremos del intervalo [a, b].")
    results = []
    for i in range(iteraciones):
        c = round((a + b) / 2.0, precision)
        fc = round(f(c), precision)
        results.append([i+1, a, b, c, fc])
        print(tabulate(results, headers=["Iteración", "a", "b", "c", "f(c)"], tablefmt="grid"))
        if abs(fc) < tolerancia or (b - a) / 2.0 < tolerancia:
            return c
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
    raise ValueError("El método no convergió o faltan iteraciones.")

def graficar_biseccion(f, a, b, raiz):
    # Graficar la función
    x = np.linspace(a - 1, b + 1, 400)
    y = f(x)

    plt.plot(x, y, label='$f(x)$')
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(color='gray', linestyle='--', linewidth=0.5)
    
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
    return x**2 - 4

# Intervalo inicial
a = 0
b = 3

# Encontrar la raíz utilizando el método de bisección
raiz = biseccion(f, a, b)

# Imprimir la raíz encontrada
print(f"La raíz encontrada es: {raiz}")

# Graficar la función y la raíz
graficar_biseccion(f, a, b, raiz)
