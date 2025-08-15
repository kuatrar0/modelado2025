import numpy as np
import matplotlib.pyplot as plt

# Datos para carga
t_carga = np.array([0, 10, 20, 30, 40, 60, 90, 120, 240, 300, 500])
Vc_carga = np.array([0, 1.4, 1.679, 2.44, 3.1, 4.17, 5.41, 6.57, 8.27, 8.61, 9.03])
V_final_carga = 9.03  # Voltaje final medido (cuando el capacitor está cargado completamente)

# Datos para descarga
t_descarga = np.array([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
Vc_descarga = np.array([9.2, 8.34, 7.56, 6.86, 6.23, 5.63, 5.09, 4.62, 4.18, 3.77, 3.41])
V0_descarga = 9.2  # Voltaje inicial de descarga

# Función teórica para ajuste
def carga_teorica(t, V, tau):
    return V * (1 - np.exp(-t / tau))

def descarga_teorica(t, V, tau):
    return V * np.exp(-t / tau)

# ---- Cálculo de tau para cada punto (Carga) ----
tau_carga_list = []
for t, Vc in zip(t_carga[1:], Vc_carga[1:]):  # Excluimos t=0 porque Vc=0
    if Vc < V_final_carga:
        tau_i = -t / np.log(1 - Vc / V_final_carga)
        tau_carga_list.append(tau_i)
tau_carga_list = np.array(tau_carga_list)
tau_carga = np.mean(tau_carga_list)
tau_carga_error = (np.max(tau_carga_list) - np.min(tau_carga_list)) / 2

# ---- Cálculo de tau para cada punto (Descarga) ----
tau_descarga_list = []
for t, Vc in zip(t_descarga[1:], Vc_descarga[1:]):  # Excluimos t=0
    if Vc > 0:
        tau_i = -t / np.log(Vc / V0_descarga)
        tau_descarga_list.append(tau_i)
tau_descarga_list = np.array(tau_descarga_list)
tau_descarga = np.mean(tau_descarga_list)
tau_descarga_error = (np.max(tau_descarga_list) - np.min(tau_descarga_list)) / 2

# ---- Graficar Carga ----
t_fit = np.linspace(0, 520, 300)
plt.plot(t_carga, Vc_carga, 'o-', color='orange', label='Datos experimentales (carga)')
plt.plot(t_fit, carga_teorica(t_fit, V_final_carga, tau_carga), 'k--', label='Ajuste teórico')
plt.xlabel('Tiempo (s)')
plt.ylabel('Vc (V)')
plt.title('Carga del capacitor')
plt.grid(True)
plt.legend()
plt.show()

# ---- Graficar Descarga ----
t_fit = np.linspace(0, 120, 300)
plt.plot(t_descarga, Vc_descarga, 'o-', color='orange', label='Datos experimentales (descarga)')
plt.plot(t_fit, descarga_teorica(t_fit, V0_descarga, tau_descarga), 'k--', label='Ajuste teórico')
plt.xlabel('Tiempo (s)')
plt.ylabel('Vc (V)')
plt.title('Descarga del capacitor')
plt.grid(True)
plt.legend()
plt.show()

# ---- Imprimir Resultados ----
print(f"τ carga experimental = {tau_carga:.2f} ± {tau_carga_error:.2f} s")
print(f"τ descarga experimental = {tau_descarga:.2f} ± {tau_descarga_error:.2f} s")
