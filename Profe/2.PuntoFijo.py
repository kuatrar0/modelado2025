import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate

# Método de punto fijo
def punto_fijo(g, valor_inicial, iteraciones=100, tolerancia=1e-6, precision=5):
    x = valor_inicial
    results = []
    for i in range(iteraciones):
        x_new = round(g(x), precision)
        results.append([i+1, x, x_new])
        print(tabulate(results, headers=["Iteración", "x", "Resultado"], tablefmt="grid"))
        if abs(x_new - x) < tolerancia:
            return x_new
        x = x_new
    raise ValueError("El método no convergió o faltan iteraciones.")

def graficar_fijo(g, valor_inicial, raiz):
    # Graficar las funciones
    x = np.linspace(-0.5, 1.5, 400)
    y = g(x)

    plt.plot(x, y, label='$g(x)=\\sqrt{x + 1}$')
    plt.plot(x, x, 'r--', label='$y=x$')
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(color='gray', linestyle='--', linewidth=0.5)
    
    # Marcar la raíz encontrada
    plt.plot(raiz, g(raiz), 'ro', label=f'Punto Fijo: x = {raiz:.5f}')
    
    # Añadir leyenda y mostrar la gráfica
    plt.legend()
    plt.xlabel('x')
    plt.ylabel('g(x)')
    plt.title('Gráfica de la función de punto fijo y su raíz')
    plt.show()

# Definir la función g(x)
def g(x):
    return np.sqrt(x + 1)

# Valor inicial
valor_inicial = 0.5

# Encontrar el punto fijo utilizando el método del punto fijo
raiz = punto_fijo(g, valor_inicial)

# Imprimir el punto fijo encontrado
print(f"El punto fijo encontrado es: {raiz}")

# Graficar la función g(x) y el punto fijo
graficar_fijo(g, valor_inicial, raiz)
