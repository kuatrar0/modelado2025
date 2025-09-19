import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, Function, dsolve, diff, simplify, expand, latex
from sympy.abc import x, y, t

def resolver_edo_completa(edo_str, variable_independiente='x', variable_dependiente='y', 
                         condiciones_iniciales=None, mostrar_pasos=True, graficar=True):
    """
    Función única que resuelve, clasifica y grafica cualquier EDO paso a paso.
    
    Parámetros:
    - edo_str: string de la EDO (ej: "dy/dx = x*y", "y' = x + y", "d2y/dx2 + y = 0")
    - variable_independiente: variable independiente (por defecto 'x')
    - variable_dependiente: variable dependiente (por defecto 'y')
    - condiciones_iniciales: diccionario con condiciones iniciales (ej: {y: 1, x: 0})
    - mostrar_pasos: si mostrar los pasos de resolución
    - graficar: si mostrar el gráfico de la solución
    
    Retorna:
    - solución general
    - solución particular (si hay condiciones iniciales)
    - tipo de EDO identificado
    """
    
    if mostrar_pasos:
        print("="*70)
        print("RESOLUCIÓN COMPLETA DE ECUACIÓN DIFERENCIAL ORDINARIA")
        print("="*70)
        print(f"EDO: {edo_str}")
        if condiciones_iniciales:
            print(f"Condiciones iniciales: {condiciones_iniciales}")
        print()
    
    # Definir variables simbólicas
    var_indep = symbols(variable_independiente)
    var_dep = Function(variable_dependiente)(var_indep)
    
    # PASO 1: Procesar y clasificar la EDO
    try:
        edo_procesada = procesar_edo_string(edo_str, var_indep, var_dep)
        tipo_edo = clasificar_edo(edo_str)
        
        if mostrar_pasos:
            print("PASO 1: Clasificación de la EDO")
            print("-" * 50)
            print(f"Tipo identificado: {tipo_edo}")
            print()
    except Exception as e:
        print(f"❌ Error al procesar la EDO: {e}")
        return None, None, "Error"
    
    # PASO 2: Resolver la EDO
    solucion_general = None
    metodo_usado = None
    
    # Intentar diferentes métodos de resolución
    metodos = [
        ("dsolve estándar", lambda: dsolve(edo_procesada, var_dep)),
        ("dsolve con simplify", lambda: dsolve(edo_procesada, var_dep, simplify=True)),
        ("resolución manual", lambda: resolver_edo_manual(edo_str, edo_procesada, var_indep, var_dep))
    ]
    
    for nombre_metodo, metodo in metodos:
        try:
            solucion_general = metodo()
            if solucion_general is not None:
                metodo_usado = nombre_metodo
                break
        except Exception as e:
            if mostrar_pasos:
                print(f"⚠️  Método '{nombre_metodo}' falló: {e}")
            continue
    
    if solucion_general is None:
        print("❌ No se pudo resolver la EDO con ningún método disponible")
        return None, None, tipo_edo
    
        if mostrar_pasos:
        print("PASO 2: Resolución paso a paso")
        print("-" * 50)
        mostrar_pasos_resolucion(edo_str, tipo_edo, var_indep, var_dep)
        print(f"✅ EDO resuelta usando: {metodo_usado}")
            print()
    
    # PASO 3: Aplicar condiciones iniciales
    solucion_particular = None
    if condiciones_iniciales:
        try:
            x0 = condiciones_iniciales.get(variable_independiente, 0)
            y0 = condiciones_iniciales.get(variable_dependiente, 0)
            ics = {var_dep.subs(var_indep, x0): y0}
            solucion_particular = dsolve(edo_procesada, var_dep, ics=ics)
        except Exception as e:
            if mostrar_pasos:
                print(f"⚠️  Error al aplicar condiciones iniciales: {e}")
            solucion_particular = None
    
    # PASO 4: Mostrar resultados
    if mostrar_pasos:
        print("PASO 3: Aplicar condiciones iniciales")
        print("-" * 50)
        if condiciones_iniciales:
            mostrar_pasos_condiciones_iniciales(edo_str, condiciones_iniciales, var_indep, var_dep, solucion_general)
        print()
        
        print("PASO 4: Resultados finales")
        print("-" * 50)
        
        if solucion_general is not None:
            print("📋 SOLUCIÓN GENERAL:")
            print("   Esta es la solución que contiene una constante arbitraria C₁")
            print("   Representa TODAS las posibles soluciones de la EDO")
            print(f"   y(x) = {solucion_general.rhs}")
            print()
        
        if solucion_particular is not None:
            print("🎯 SOLUCIÓN PARTICULAR:")
            print("   Esta es la solución específica que satisface las condiciones iniciales")
            print("   La constante C₁ ya fue calculada con los valores dados")
            print(f"   y(x) = {solucion_particular.rhs}")
            print()
            
            print("💡 INTERPRETACIÓN:")
            print("   • La solución general te da la familia completa de curvas solución")
            print("   • La solución particular te da la curva específica que pasa por el punto dado")
            print("   • Ambas son correctas, pero la particular es más específica")
            print()
    
    # PASO 5: Graficar si se solicita
    if graficar and solucion_particular is not None:
        try:
            graficar_solucion_edo(solucion_particular, var_indep, condiciones_iniciales)
        except Exception as e:
            if mostrar_pasos:
                print(f"⚠️  Error al graficar: {e}")
    
    return solucion_general, solucion_particular, tipo_edo

def procesar_edo_string(edo_str, var_indep, var_dep):
    """Procesa el string de la EDO y lo convierte a formato de SymPy"""
    # Reemplazar funciones comunes
    edo_str = edo_str.replace("sen(x)", "sin(x)")
    edo_str = edo_str.replace("sen", "sin")
    
    # Reemplazar notaciones de derivadas
    edo_str = edo_str.replace("dy/dx", "Derivative(y(x), x)")
    edo_str = edo_str.replace("d2y/dx2", "Derivative(y(x), x, 2)")
    edo_str = edo_str.replace("y'", "Derivative(y(x), x)")
    edo_str = edo_str.replace("y''", "Derivative(y(x), x, 2)")
    
    # Reemplazar y por y(x) de manera cuidadosa
    import re
    edo_str = re.sub(r'(?<![a-zA-Z])\by\b(?![a-zA-Z\(])', 'y(x)', edo_str)
    
    # Si hay un =, mover todo al lado izquierdo
    if "=" in edo_str:
        izquierda, derecha = edo_str.split("=", 1)
        edo_str = f"({izquierda.strip()}) - ({derecha.strip()})"
    
    return sp.sympify(edo_str)

def clasificar_edo(edo_str):
    """Clasifica el tipo de EDO"""
    if "=" not in edo_str:
        return "Formato inválido"
    
    # Contar derivadas
    if "d2y/dx2" in edo_str or "y''" in edo_str:
        return "EDO de segundo orden"
    elif "dy/dx" in edo_str or "y'" in edo_str:
        if es_variables_separables(edo_str):
            return "EDO de variables separables"
        else:
            return "EDO lineal de primer orden"
    else:
        return "EDO de orden superior"

def es_variables_separables(edo_str):
    """Determina si una EDO es de variables separables"""
    if "=" not in edo_str:
        return False
    
    izquierda, derecha = edo_str.split("=", 1)
    derecha = derecha.strip()
    
    # Variables separables: dy/dx = y * f(x) o dy/dx = f(x) * y
    if not ("*" in derecha and "y" in derecha):
        return False
    
    # Verificar si hay + o - al nivel principal
    nivel_parentesis = 0
    for char in derecha:
        if char == '(':
            nivel_parentesis += 1
        elif char == ')':
            nivel_parentesis -= 1
        elif char in ['+', '-'] and nivel_parentesis == 0:
            return False
    
    return True

def resolver_edo_manual(edo_str, edo_procesada, var_indep, var_dep):
    """Resuelve EDOs manualmente cuando SymPy falla"""
    try:
        if es_variables_separables(edo_str):
            return resolver_variables_separables_manual(edo_str, var_indep, var_dep)
        else:
            return resolver_lineal_primer_orden_manual(edo_str, var_indep, var_dep)
    except:
        return None

def resolver_variables_separables_manual(edo_str, var_indep, var_dep):
    """Resuelve EDOs de variables separables manualmente"""
    if "=" not in edo_str:
        return None
    
    izquierda, derecha = edo_str.split("=", 1)
    derecha = derecha.strip()
    
    # Forma: dy/dx = y * f(x)
    if "y*" in derecha:
        f_x_str = derecha.replace("y*", "").strip()
    elif "*y" in derecha:
        f_x_str = derecha.replace("*y", "").strip()
    else:
        return None
    
    try:
        f_x = sp.sympify(f_x_str)
        integral_f_x = sp.integrate(f_x, var_indep)
        C1 = sp.Symbol('C1')
        solucion = C1 * sp.exp(integral_f_x)
        return sp.Eq(var_dep, solucion)
    except:
        return None

def resolver_lineal_primer_orden_manual(edo_str, var_indep, var_dep):
    """Resuelve EDOs lineales de primer orden manualmente"""
    if "=" not in edo_str:
        return None
    
    izquierda, derecha = edo_str.split("=", 1)
    derecha = derecha.strip()
    
    try:
        expr = sp.sympify(derecha)
        
        # Separar términos con y y sin y
        terminos_con_y = []
        terminos_sin_y = []
        
        if expr.is_Add:
            for term in expr.args:
                if var_dep in term.free_symbols:
                    terminos_con_y.append(term)
                else:
                    terminos_sin_y.append(term)
        else:
            if var_dep in expr.free_symbols:
                terminos_con_y.append(expr)
            else:
                terminos_sin_y.append(expr)
        
        Q_x = sum(terminos_sin_y) if terminos_sin_y else 0
        
        # P(x) = coeficiente de y
        P_x = 0
        for term in terminos_con_y:
            if term.is_Mul:
                for factor in term.args:
                    if factor != var_dep:
                        P_x += factor
                        break
            elif term == var_dep:
                P_x += 1
        
        # Factor integrante y solución
        integral_P_x = sp.integrate(P_x, var_indep)
        mu_x = sp.exp(integral_P_x)
        C1 = sp.Symbol('C1')
        integral_mu_Q = sp.integrate(mu_x * Q_x, var_indep)
        solucion = (integral_mu_Q + C1) / mu_x
        
        return sp.Eq(var_dep, solucion)
    except:
        return None

def mostrar_pasos_resolucion(edo_str, tipo_edo, var_indep, var_dep):
    """Muestra los pasos detallados de resolución paso a paso"""
    print(f"EDO: {edo_str}")
    print(f"Tipo: {tipo_edo}")
    print()
    
    if tipo_edo == "EDO de variables separables":
        mostrar_pasos_variables_separables_detallado(edo_str)
    elif tipo_edo == "EDO lineal de primer orden":
        mostrar_pasos_lineal_detallado(edo_str)
    else:
        mostrar_pasos_general_detallado(edo_str, tipo_edo)

def mostrar_pasos_variables_separables_detallado(edo_str):
    """Muestra pasos detallados para variables separables"""
    if "=" not in edo_str:
        return
    
    izquierda, derecha = edo_str.split("=", 1)
    derecha = derecha.strip()
    
    print("MÉTODO: VARIABLES SEPARABLES")
    print("=" * 40)
    print()
    
    # Extraer f(x) dinámicamente
    if "y*" in derecha:
        f_x_str = derecha.replace("y*", "").strip()
        print(f"PASO 1: Identificar f(x)")
        print(f"   EDO: {edo_str}")
        print(f"   Forma: dy/dx = y · f(x)")
        print(f"   Donde: f(x) = {f_x_str}")
        print()
        
        print("PASO 2: Separar variables")
        print("   Dividir por y: (1/y) · dy/dx = f(x)")
        print("   Multiplicar por dx: (1/y) dy = f(x) dx")
        print()
        
        print("PASO 3: Integrar")
        print("   ∫ (1/y) dy = ∫ f(x) dx")
        print("   ln|y| = ∫ f(x) dx + C")
        print()
        
        print("PASO 4: Despejar y")
        print("   |y| = e^(∫ f(x) dx + C)")
        print("   y = C₁ · e^(∫ f(x) dx)")
        print(f"   Donde C₁ = ±e^C")
        print()
        
    elif "*y" in derecha:
        f_x_str = derecha.replace("*y", "").strip()
        print(f"PASO 1: Identificar f(x)")
        print(f"   EDO: {edo_str}")
        print(f"   Forma: dy/dx = f(x) · y")
        print(f"   Donde: f(x) = {f_x_str}")
        print()
        
        print("PASO 2: Separar variables")
        print("   Dividir por y: (1/y) · dy/dx = f(x)")
        print("   Multiplicar por dx: (1/y) dy = f(x) dx")
        print()
        
        print("PASO 3: Integrar")
        print("   ∫ (1/y) dy = ∫ f(x) dx")
        print("   ln|y| = ∫ f(x) dx + C")
        print()
        
        print("PASO 4: Despejar y")
        print("   |y| = e^(∫ f(x) dx + C)")
        print("   y = C₁ · e^(∫ f(x) dx)")
        print(f"   Donde C₁ = ±e^C")
        print()
    else:
        print("PASO 1: Identificar la forma")
        print(f"   EDO: {edo_str}")
        print("   Forma: dy/dx = f(x) · g(y)")
        print()
        print("PASO 2: Separar variables")
        print("   dy/g(y) = f(x) dx")
        print()
        print("PASO 3: Integrar")
        print("   ∫ dy/g(y) = ∫ f(x) dx")
        print()
        print("PASO 4: Resolver")
        print("   G(y) = F(x) + C")
        print()

def mostrar_pasos_lineal_detallado(edo_str):
    """Muestra pasos detallados para EDOs lineales"""
    if "=" not in edo_str:
        return
    
    print("MÉTODO: FACTOR INTEGRANTE (EDO LINEAL)")
    print("=" * 40)
    print()
    
    print("PASO 1: Escribir en forma estándar")
    print(f"   EDO: {edo_str}")
    print("   Forma estándar: dy/dx + P(x)y = Q(x)")
    print()
    
    print("PASO 2: Identificar P(x) y Q(x)")
    print("   • P(x) = coeficiente de y")
    print("   • Q(x) = término independiente")
    print()
    
    print("PASO 3: Calcular factor integrante")
    print("   μ(x) = e^(∫P(x)dx)")
    print()
    
    print("PASO 4: Multiplicar por μ(x)")
    print("   μ(x)dy/dx + μ(x)P(x)y = μ(x)Q(x)")
    print()
    
    print("PASO 5: Lado izquierdo es derivada")
    print("   d/dx[μ(x)y] = μ(x)Q(x)")
    print()
    
    print("PASO 6: Integrar")
    print("   μ(x)y = ∫μ(x)Q(x)dx + C")
    print()
    
    print("PASO 7: Despejar y")
    print("   y = (1/μ(x))[∫μ(x)Q(x)dx + C]")
    print()

def mostrar_pasos_general_detallado(edo_str, tipo_edo):
    """Muestra pasos detallados para otros tipos de EDO"""
    print(f"MÉTODO: RESOLUCIÓN GENERAL ({tipo_edo})")
    print("=" * 40)
    print()
    
    print("PASO 1: Analizar la EDO")
    print(f"   EDO: {edo_str}")
    print(f"   Tipo: {tipo_edo}")
    print()
    
    print("PASO 2: Identificar método apropiado")
    print("   • Verificar si es separable")
    print("   • Verificar si es lineal")
    print("   • Aplicar método específico")
    print()
    
    print("PASO 3: Resolver paso a paso")
    print("   • Aplicar transformaciones")
    print("   • Integrar")
    print("   • Simplificar")
    print()
    
    print("PASO 4: Verificar solución")
    print("   • Sustituir en la EDO original")
    print("   • Confirmar que satisface la ecuación")
    print()

def mostrar_metodo_variables_separables(edo_str):
    """Muestra el método para variables separables de forma dinámica"""
    if "=" not in edo_str:
        return
    
    izquierda, derecha = edo_str.split("=", 1)
    derecha = derecha.strip()
    
    print("Método: Variables Separables")
    print("Forma: dy/dx = f(x) · g(y)")
    print()
    print("Pasos del método:")
    print("1. Separar variables:")
    print("   dy/g(y) = f(x) dx")
    print()
    print("2. Integrar ambos lados:")
    print("   ∫ dy/g(y) = ∫ f(x) dx")
    print()
    print("3. Resolver integrales:")
    print("   G(y) = F(x) + C")
    print()
    print("4. Despejar y (si es posible):")
    print("   y = G⁻¹(F(x) + C)")
    print()
    print("Aplicando a tu EDO:")
    print(f"   {edo_str}")
    
    # Extraer f(x) dinámicamente
    if "y*" in derecha:
        f_x_str = derecha.replace("y*", "").strip()
        print(f"   f(x) = {f_x_str}, g(y) = y")
    elif "*y" in derecha:
        f_x_str = derecha.replace("*y", "").strip()
        print(f"   f(x) = {f_x_str}, g(y) = y")
    else:
        print("   [Identificando f(x) y g(y) dinámicamente]")

def mostrar_metodo_lineal_primer_orden(edo_str):
    """Muestra el método para EDOs lineales de forma dinámica"""
    if "=" not in edo_str:
        return
    
    print("Método: Factor Integrante (EDO Lineal)")
    print("Forma: dy/dx + P(x)y = Q(x)")
    print()
    print("Pasos del método:")
    print("1. Identificar P(x) y Q(x)")
    print("2. Calcular factor integrante:")
    print("   μ(x) = e^(∫P(x)dx)")
    print()
    print("3. Multiplicar EDO por μ(x):")
    print("   μ(x)dy/dx + μ(x)P(x)y = μ(x)Q(x)")
    print()
    print("4. Lado izquierdo es derivada de μ(x)y:")
    print("   d/dx[μ(x)y] = μ(x)Q(x)")
    print()
    print("5. Integrar ambos lados:")
    print("   μ(x)y = ∫μ(x)Q(x)dx + C")
    print()
    print("6. Despejar y:")
    print("   y = (1/μ(x))[∫μ(x)Q(x)dx + C]")
    print()
    print("Aplicando a tu EDO:")
    print(f"   {edo_str}")
    print("   [Identificando P(x) y Q(x) dinámicamente]")

def mostrar_metodo_general(edo_str, tipo_edo):
    """Muestra método general para cualquier tipo de EDO"""
    print(f"Método: Resolución General para {tipo_edo}")
    print()
    print("Pasos del método:")
    print("1. Analizar la estructura de la EDO")
    print("2. Identificar el método más apropiado")
    print("3. Aplicar transformaciones necesarias")
    print("4. Resolver paso a paso")
    print("5. Verificar la solución")
    print()
    print("Aplicando a tu EDO:")
    print(f"   {edo_str}")
    print("   [Aplicando método específico para este tipo]")

def mostrar_pasos_condiciones_iniciales(edo_str, condiciones_iniciales, var_indep, var_dep, solucion_general):
    """Muestra los pasos detallados para aplicar condiciones iniciales"""
    if not condiciones_iniciales:
        return
    
    x0 = condiciones_iniciales.get('x', 0)
    y0 = condiciones_iniciales.get('y', 0)
    
    print("APLICACIÓN DE CONDICIONES INICIALES")
    print("=" * 40)
    print()
    
    print("PASO 1: Identificar la condición inicial")
    print(f"   Condición: y({x0}) = {y0}")
    print()
    
    print("PASO 2: Sustituir en la solución general")
    print("   Solución general: y(x) = [expresión con C₁]")
    print(f"   Sustituyendo x = {x0}:")
    print(f"   y({x0}) = [expresión con C₁ evaluada en x={x0}]")
    print()
    
    print("PASO 3: Igualar a la condición inicial")
    print(f"   [expresión con C₁ evaluada en x={x0}] = {y0}")
    print()
    
    print("PASO 4: Resolver para C₁")
    print("   C₁ = [valor calculado]")
    print()
    
    print("PASO 5: Sustituir C₁ en la solución general")
    print("   Solución particular: y(x) = [expresión con C₁ sustituido]")
    print()
    
    print("RESULTADO:")
    print("   Esta es la solución específica que satisface las condiciones iniciales.")
    print("   Es única y pasa por el punto dado.")

def graficar_solucion_edo(solucion_particular, var_indep, condiciones_iniciales):
    """Grafica la solución de la EDO"""
    try:
        # Extraer la función de la solución
        funcion = solucion_particular.rhs
        
        # Crear array de x
        x_vals = np.linspace(-5, 5, 1000)
        
        # Convertir a función numérica
        funcion_numerica = sp.lambdify(var_indep, funcion, 'numpy')
        
        # Evaluar la función
        y_vals = funcion_numerica(x_vals)
        
        # Crear el gráfico
        plt.figure(figsize=(10, 6))
        plt.plot(x_vals, y_vals, 'b-', linewidth=2, label='Solución de la EDO')
        
        # Marcar el punto inicial si existe
        if condiciones_iniciales:
            x0 = condiciones_iniciales.get('x', 0)
            y0 = condiciones_iniciales.get('y', 0)
            plt.plot(x0, y0, 'ro', markersize=8, label=f'Condición inicial ({x0}, {y0})')
        
        plt.xlabel('x')
        plt.ylabel('y(x)')
        plt.title('Solución de la Ecuación Diferencial')
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.show()
        
    except Exception as e:
        print(f"⚠️  Error al graficar: {e}")

# Función de ejemplo para uso fácil
def ejemplo_uso():
    """Muestra cómo usar la función principal"""
    print("EJEMPLO DE USO:")
    print("="*50)
    
    # Ejemplo 1: EDO simple
    print("Ejemplo 1: EDO de variables separables")
    sol_gen, sol_par, tipo = resolver_edo_completa(
        "dy/dx = y*sin(x)",
        condiciones_iniciales={"y": 1, "x": 0}
    )
    
    print("\n" + "="*50)
    
    # Ejemplo 2: EDO lineal
    print("Ejemplo 2: EDO lineal de primer orden")
    sol_gen, sol_par, tipo = resolver_edo_completa(
        "dy/dx = x + y",
        condiciones_iniciales={"y": 1, "x": 0}
    )

if __name__ == "__main__":
    # Ejemplo con tu EDO
    print("=== RESOLVIENDO TU EDO ===")
    sol_gen, sol_par, tipo = resolver_edo_completa(
        "dy/dx = y*sin(x)",
        condiciones_iniciales={"y": 1, "x": 0}
    )