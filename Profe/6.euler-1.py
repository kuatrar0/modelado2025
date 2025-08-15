import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
 
def euler(f, y0, t0, tf, h):
    t_values = np.arange(t0, tf + h, h)
    y_values = np.zeros(len(t_values))
    y_values[0] = y0
    for i in range(1, len(t_values)):
        y_values[i] = y_values[i - 1] + h * f(t_values[i - 1], y_values[i - 1])
    return t_values, y_values
 
def euler_mejorado(f, y0, t0, tf, h):
    t_values = np.arange(t0, tf + h, h)
    y_values = np.zeros(len(t_values))
    y_values[0] = y0
    for i in range(1, len(t_values)):
        k1 = f(t_values[i - 1], y_values[i - 1])
        k2 = f(t_values[i - 1] + h, y_values[i - 1] + h * k1)
        y_values[i] = y_values[i - 1] + h * (k1 + k2) / 2
    return t_values, y_values
 
def f(t, y):
    return t * np.exp(-np.sin(t)) - y * np.cos(t)
 
def solucion_particular(t):
    return (((t**2)/2)*np.exp(-np.sin(t))+np.exp(-np.sin(t)))
 
# Condiciones iniciales y parámetros
y0 = np.pi
t0 = 0
tf = np.pi
h = np.pi / 4
 
# Soluciones
t_euler, y_euler = euler(f, y0, t0, tf, h)
t_euler_mejorado, y_euler_mejorado = euler_mejorado(f, y0, t0, tf, h)
y_real = solucion_particular(t_euler)
 
# Crear DataFrame
resultados = pd.DataFrame({
    'Tiempo': t_euler,
    'Euler': y_euler,
    'Euler Mejorado': y_euler_mejorado,
    'Solución Real': y_real
})
 
print(resultados)
 
# Graficar resultados
plt.plot(t_euler, y_euler, label='Euler')
plt.plot(t_euler_mejorado, y_euler_mejorado, label='Euler Mejorado')
plt.plot(t_euler, y_real, label='Solución Real')
plt.xlabel('Tiempo')
plt.ylabel('Valor de y')
plt.legend()
plt.title('Métodos de Euler, Euler Mejorado y Solución Real')
plt.show()

