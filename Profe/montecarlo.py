import numpy as np
from scipy.stats import norm
from tabulate import tabulate

# Semilla fija para reproducibilidad
semilla = 0
np.random.seed(semilla)

# Definición de la función a integrar
def f(x, y):
    return np.exp(2*x-y)

# Dominio de integración
a, b = 0, 1
c, d = 1, 2
area = (b - a) * (d - c)

# Muestra aleatoria
n = 40000
x_rand = np.random.uniform(a, b, n)
y_rand = np.random.uniform(c, d, n)

# Evaluación de la función
valores = f(x_rand, y_rand)

# Estadísticas
media_muestral = np.mean(valores)
varianza_muestral = np.var(valores, ddof=1)
desviacion_std = np.std(valores, ddof=1)
error_estandar = desviacion_std / np.sqrt(n)

# Intervalo de confianza del 95% para la media
z = norm.ppf(0.975)
li = media_muestral - z * error_estandar
ls = media_muestral + z * error_estandar

# Estimación final de la integral (área)
integral_estimacion = area * media_muestral
ic_area_inf = li * area
ic_area_sup = ls * area

# Tabla resumen
tabla = [
    ["Tamaño de muestra (n)", n],
    ["Media muestral (X̄)", media_muestral],
    ["Varianza muestral", varianza_muestral],
    ["Desviación estándar", desviacion_std],
    ["Error estándar", error_estandar],
    ["IC 95% media - inferior", li],
    ["IC 95% media - superior", ls],
    ["Integral estimada (área)", integral_estimacion],
    ["IC 95% área - inferior", ic_area_inf],
    ["IC 95% área - superior", ic_area_sup]
]

print(tabulate(tabla, headers=["Estadístico", "Valor"], tablefmt="fancy_grid", floatfmt=".10f"))
