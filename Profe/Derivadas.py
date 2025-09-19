import sympy as sp
import numpy as np

def calcular_derivada_n_en_punto(funcion_str, variable_str, n, punto):
    # Definir la variable simbólica
    x = sp.Symbol(variable_str)
    
    # Convertir el string de la función a una expresión simbólica
    funcion = sp.sympify(funcion_str)
    
    # Calcular la n-ésima derivada
    derivada_n = sp.diff(funcion, x, n)
    
    # Evaluar la derivada en el punto usando sympy
    valor_evaluado = derivada_n.evalf(subs={x: punto})
    
    return derivada_n, valor_evaluado

# Ejemplo de uso
if __name__ == "__main__":
    funcion = "sqrt(2) * exp(x**2)"   # Función que quieras
    variable = "x"
    n = 2                        # Orden de la derivada
    punto = 0.5                  # Punto en el que se evalúa

    derivada, valor = calcular_derivada_n_en_punto(funcion, variable, n, punto)
    
    print(f"La {n}-ésima derivada de {funcion} es:\n{derivada}")
    print(f"Evaluada en x = {punto} ≈ {valor}")