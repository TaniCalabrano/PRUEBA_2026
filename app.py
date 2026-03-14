import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt


# -------- FUNCION QUE EXPLICA LA DERIVADA --------

def explicar_derivada(expr, x):

    pasos = []

    if expr.is_Add:
        pasos.append("La función es una **suma**. Derivamos cada término:")

        for termino in expr.args:
            d = sp.diff(termino, x)
            pasos.append(f"$\\frac{{d}}{{dx}}({sp.latex(termino)}) = {sp.latex(d)}$")

    elif expr.is_Mul:
        pasos.append("La función es un **producto**. Aplicamos la regla del producto:")

        pasos.append(r"$ (uv)' = u'v + uv'$")

        d = sp.diff(expr, x)
        pasos.append(f"Resultado: ${sp.latex(d)}$")

    elif expr.is_Pow:

        base, exp = expr.args

        if base == x:

            pasos.append("Aplicamos la **regla de la potencia**")

            pasos.append(r"$\frac{d}{dx}(x^n)=nx^{n-1}$")

            d = sp.diff(expr, x)

            pasos.append(f"$\\frac{{d}}{{dx}}({sp.latex(expr)}) = {sp.latex(d)}$")

    else:

        d = sp.diff(expr, x)

        pasos.append("Derivamos directamente:")

        pasos.append(f"$\\frac{{d}}{{dx}}({sp.latex(expr)}) = {sp.latex(d)}$")

    return pasos


# -------- INTERFAZ --------

st.title("Explorador Matemático")

x = sp.symbols('x')

expr_text = st.text_input("Escribe una función en x", "x**2 + 3*x + 1")

col1, col2 = st.columns(2)

try:

    expr = sp.sympify(expr_text)

    derivada = sp.diff(expr, x)
    integral = sp.integrate(expr, x)

    # -------- BUSCAR RAICES --------

    try:
        raices = sp.solve(expr, x)

    except Exception:
        try:
            raices = [sp.nsolve(expr, x, 0)]
        except Exception:
            raices = "No se pudieron encontrar raíces"

    # -------- COLUMNA IZQUIERDA --------

    with col1:

        st.subheader("Función")
        st.latex(sp.latex(expr))

        st.subheader("Derivada")
        st.latex(sp.latex(derivada))

        st.subheader("Integral")
        st.latex(sp.latex(integral))

        st.subheader("Raíces")
        st.write(raices)

        # -------- GRAFICA --------

        f = sp.lambdify(x, expr, "numpy")
        d = sp.lambdify(x, derivada, "numpy")

        xs = np.linspace(-10, 10, 400)

        ys = f(xs)
        yd = d(xs)

        fig, ax = plt.subplots()

        ax.plot(xs, ys, label="f(x)")
        ax.plot(xs, yd, label="f'(x)")

        ax.axhline(0)
        ax.axvline(0)

        ax.legend()

        st.subheader("Gráfica")

        st.pyplot(fig)

    # -------- COLUMNA DERECHA --------

    with col2:

        st.subheader("Procedimiento")

        pasos = explicar_derivada(expr, x)

        st.subheader("Procedimiento de la derivada")

        for p in pasos:
            st.markdown(p)

        st.markdown("**1. Función original**")
        st.latex("f(x) = " + sp.latex(expr))

        st.markdown("**2. Derivamos respecto a x**")

        st.latex(
            "\\frac{d}{dx}\\left(" + sp.latex(expr) + "\\right)"
        )

        st.markdown("**3. Resultado de la derivada**")

        st.latex("f'(x) = " + sp.latex(derivada))

        st.markdown("**4. Calculamos la integral**")

        st.latex(
            "\\int " + sp.latex(expr) + "\\, dx"
        )

        st.markdown("**5. Resultado de la integral**")

        st.latex(
            "\\int " + sp.latex(expr) + "\\, dx = " + sp.latex(integral)
        )

        st.markdown("**6. Encontramos las raíces**")

        st.latex(
            sp.latex(expr) + "=0"
        )

        st.write("Soluciones:", raices)


except Exception as e:

    st.error("Error en la función")

    st.write(e)