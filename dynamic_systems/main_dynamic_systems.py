import sympy as sp
from dynamic_system import DynamicSystem

def main():
    x, y, a = sp.symbols('x y a')
    f_x = 16 * sp.sin(x)
    g_x = 13 * sp.cos(x) - 5*sp.cos(2*x) - 2*sp.cos(3*x) - sp.cos(4*x)

    system = DynamicSystem(
        f_sym=f_x,
        g_sym=g_x
    )
    system.run_full_analysis()


if __name__ == "__main__":
    main()
