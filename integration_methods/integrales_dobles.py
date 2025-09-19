import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, integrate, latex, simplify, expand

def resolver_integral_doble_paso_a_paso(funcion_str, variable1, variable2, 
                                       lim_inf1, lim_sup1, lim_inf2, lim_sup2, 
                                       orden_integracion='xy'):
    """
    Resuelve una integral doble definida paso a paso analíticamente.
    
    Parámetros:
    - funcion_str: string de la función a integrar (ej: "x*y", "x**2 + y**2")
    - variable1, variable2: variables de integración (ej: 'x', 'y')
    - lim_inf1, lim_sup1: límites de integración para la primera variable
    - lim_inf2, lim_sup2: límites de integración para la segunda variable
    - orden_integracion: 'xy' (primero x, luego y) o 'yx' (primero y, luego x)
    
    Retorna:
    - resultado final
    - pasos intermedios
    """
    
    # Definir variables simbólicas
    x, y = symbols(variable1 + ' ' + variable2)
    
    # Convertir string a expresión simbólica
    funcion = sp.sympify(funcion_str)
    
    print("="*60)
    print("RESOLUCIÓN DE INTEGRAL DOBLE PASO A PASO")
    print("="*60)
    print(f"Función: {funcion}")
    print(f"Límites: ∫∫ {funcion} d{orden_integracion}")
    print(f"Región: {lim_inf1} ≤ {variable1} ≤ {lim_sup1}, {lim_inf2} ≤ {variable2} ≤ {lim_sup2}")
    print()
    
    pasos = []
    
    if orden_integracion == 'xy':
        print("PASO 1: Integración respecto a x")
        print("-" * 40)
        
        # Primera integración (respecto a x)
        integral_x = integrate(funcion, x)
        print(f"∫ {funcion} dx = {integral_x}")
        
        # Evaluar en los límites de x
        integral_x_evaluada = integral_x.subs(x, lim_sup1) - integral_x.subs(x, lim_inf1)
        print(f"Evaluando en x = {lim_sup1} y x = {lim_inf1}:")
        print(f"= [{integral_x.subs(x, lim_sup1)}] - [{integral_x.subs(x, lim_inf1)}]")
        print(f"= {integral_x_evaluada}")
        
        # Simplificar si es posible
        integral_x_simplificada = simplify(integral_x_evaluada)
        if integral_x_simplificada != integral_x_evaluada:
            print(f"Simplificando: {integral_x_simplificada}")
        
        pasos.append({
            'paso': 1,
            'descripcion': 'Integración respecto a x',
            'integral': integral_x,
            'evaluada': integral_x_simplificada
        })
        
        print()
        print("PASO 2: Integración respecto a y")
        print("-" * 40)
        
        # Segunda integración (respecto a y)
        integral_final = integrate(integral_x_simplificada, y)
        print(f"∫ {integral_x_simplificada} dy = {integral_final}")
        
        # Evaluar en los límites de y
        resultado = integral_final.subs(y, lim_sup2) - integral_final.subs(y, lim_inf2)
        print(f"Evaluando en y = {lim_sup2} y y = {lim_inf2}:")
        print(f"= [{integral_final.subs(y, lim_sup2)}] - [{integral_final.subs(y, lim_inf2)}]")
        print(f"= {resultado}")
        
        # Simplificar resultado final
        resultado_final = simplify(resultado)
        if resultado_final != resultado:
            print(f"Simplificando resultado final: {resultado_final}")
        
        pasos.append({
            'paso': 2,
            'descripcion': 'Integración respecto a y',
            'integral': integral_final,
            'evaluada': resultado_final
        })
        
    else:  # orden_integracion == 'yx'
        print("PASO 1: Integración respecto a y")
        print("-" * 40)
        
        # Primera integración (respecto a y)
        integral_y = integrate(funcion, y)
        print(f"∫ {funcion} dy = {integral_y}")
        
        # Evaluar en los límites de y
        integral_y_evaluada = integral_y.subs(y, lim_sup2) - integral_y.subs(y, lim_inf2)
        print(f"Evaluando en y = {lim_sup2} y y = {lim_inf2}:")
        print(f"= [{integral_y.subs(y, lim_sup2)}] - [{integral_y.subs(y, lim_inf2)}]")
        print(f"= {integral_y_evaluada}")
        
        # Simplificar si es posible
        integral_y_simplificada = simplify(integral_y_evaluada)
        if integral_y_simplificada != integral_y_evaluada:
            print(f"Simplificando: {integral_y_simplificada}")
        
        pasos.append({
            'paso': 1,
            'descripcion': 'Integración respecto a y',
            'integral': integral_y,
            'evaluada': integral_y_simplificada
        })
        
        print()
        print("PASO 2: Integración respecto a x")
        print("-" * 40)
        
        # Segunda integración (respecto a x)
        integral_final = integrate(integral_y_simplificada, x)
        print(f"∫ {integral_y_simplificada} dx = {integral_final}")
        
        # Evaluar en los límites de x
        resultado = integral_final.subs(x, lim_sup1) - integral_final.subs(x, lim_inf1)
        print(f"Evaluando en x = {lim_sup1} y x = {lim_inf1}:")
        print(f"= [{integral_final.subs(x, lim_sup1)}] - [{integral_final.subs(x, lim_inf1)}]")
        print(f"= {resultado}")
        
        # Simplificar resultado final
        resultado_final = simplify(resultado)
        if resultado_final != resultado:
            print(f"Simplificando resultado final: {resultado_final}")
        
        pasos.append({
            'paso': 2,
            'descripcion': 'Integración respecto a x',
            'integral': integral_final,
            'evaluada': resultado_final
        })
    
    print()
    print("="*60)
    print("RESULTADO FINAL")
    print("="*60)
    print(f"∫∫ {funcion} d{orden_integracion} = {resultado_final}")
    
    # Convertir a número si es posible
    try:
        valor_numerico = float(resultado_final.evalf())
        print(f"Valor numérico: {valor_numerico}")
    except:
        print("No se puede convertir a valor numérico")
    
    return resultado_final, pasos

def resolver_integral_doble_rectangular(funcion_str, variable1, variable2,
                                      lim_inf1, lim_sup1, lim_inf2, lim_sup2):
    """
    Resuelve integral doble en región rectangular usando ambos órdenes de integración
    para verificar el resultado.
    """
    print("RESOLVIENDO CON ORDEN XY (primero x, luego y):")
    resultado1, pasos1 = resolver_integral_doble_paso_a_paso(
        funcion_str, variable1, variable2, 
        lim_inf1, lim_sup1, lim_inf2, lim_sup2, 'xy'
    )
    
    print("\n" + "="*80 + "\n")
    
    print("RESOLVIENDO CON ORDEN YX (primero y, luego x):")
    resultado2, pasos2 = resolver_integral_doble_paso_a_paso(
        funcion_str, variable1, variable2, 
        lim_inf1, lim_sup1, lim_inf2, lim_sup2, 'yx'
    )
    
    print("\n" + "="*80)
    print("VERIFICACIÓN:")
    print(f"Resultado con orden XY: {resultado1}")
    print(f"Resultado con orden YX: {resultado2}")
    
    if simplify(resultado1 - resultado2) == 0:
        print("✓ Los resultados coinciden (verificación exitosa)")
    else:
        print("⚠ Los resultados no coinciden - revisar límites o función")
    
    return resultado1, resultado2

def graficar_region_integracion(lim_inf1, lim_sup1, lim_inf2, lim_sup2, titulo="Región de Integración"):
    """
    Grafica la región rectangular de integración
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Crear rectángulo
    x_rect = [lim_inf1, lim_sup1, lim_sup1, lim_inf1, lim_inf1]
    y_rect = [lim_inf2, lim_inf2, lim_sup2, lim_sup2, lim_inf2]
    
    ax.plot(x_rect, y_rect, 'b-', linewidth=2, label='Región de integración')
    ax.fill(x_rect, y_rect, alpha=0.3, color='blue')
    
    # Configurar ejes
    ax.set_xlim(lim_inf1 - 0.5, lim_sup1 + 0.5)
    ax.set_ylim(lim_inf2 - 0.5, lim_sup2 + 0.5)
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(titulo)
    ax.legend()
    
    # Agregar etiquetas de límites
    ax.text(lim_inf1, lim_inf2 - 0.2, f'({lim_inf1}, {lim_inf2})', ha='center')
    ax.text(lim_sup1, lim_sup2 + 0.2, f'({lim_sup1}, {lim_sup2})', ha='center')
    
    plt.tight_layout()
    plt.show()


resultado, pasos = resolver_integral_doble_paso_a_paso(
    "exp(2*x-y)",           # función como string (ej: "x*y", "x**2 + y**2", "exp(x+y)")
    "x", "y",        # variables de integración
    0, 1,            # límites inferior y superior de la primera variable
    1, 2,            # límites inferior y superior de la segunda variable
    "yx"             # orden: "xy" (primero x, luego y) o "yx" (primero y, luego x)
)
# CÓMO USAR ESTE CÓDIGO:
# =====================
# 
# 1. Para resolver una integral doble paso a paso:
#    resultado, pasos = resolver_integral_doble_paso_a_paso(
#        "x*y",           # función como string (ej: "x*y", "x**2 + y**2", "exp(x+y)")
#        "x", "y",        # variables de integración
#        0, 1,            # límites inferior y superior de la primera variable
#        0, 2,            # límites inferior y superior de la segunda variable
#        "xy"             # orden: "xy" (primero x, luego y) o "yx" (primero y, luego x)
#    )
#
# 2. Para resolver con verificación automática (ambos órdenes):
#    resultado1, resultado2 = resolver_integral_doble_rectangular(
#        "x**2 + y**2",   # función
#        "x", "y",        # variables
#        0, 1,            # límites de x
#        0, 1             # límites de y
#    )
#
# 3. Para graficar la región de integración:
#    graficar_region_integracion(0, 1, 0, 2, "Mi región")
#
# NOTAS SOBRE LA SINTAXIS DE FUNCIONES:
# - Usar ** para potencias: x**2, y**3
# - Usar * para multiplicación: x*y, 2*x
# - Usar + y - para suma y resta: x + y, x - y
# - Usar exp() para exponencial: exp(x), exp(x+y)
# - Usar sin(), cos(), tan() para trigonométricas: sin(x), cos(x*y)
# - Usar sqrt() para raíz cuadrada: sqrt(x), sqrt(x**2 + y**2)
# - Usar log() para logaritmo natural: log(x), log(x*y)
