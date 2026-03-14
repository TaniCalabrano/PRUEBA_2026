import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Explorador Matemático", layout="wide")

st.title("Explorador Matemático")

x = sp.symbols('x')

# -------- MEMORIA --------

if "expr_text" not in st.session_state:
    st.session_state.expr_text = ""

def agregar(valor):
    st.session_state.expr_text += valor

def borrar():
    st.session_state.expr_text = ""

# -------- PASOS DE DERIVACIÓN --------

def derivada_pasos(expr, x):

    pasos = []

    pasos.append(r"\textbf{Paso 1: Derivamos respecto a } x")
    pasos.append(r"\frac{d}{dx}\left(" + sp.latex(expr) + r"\right)")

    if expr.is_Add:

        pasos.append(r"\textbf{Paso 2: Aplicamos la linealidad de la derivada}")

        suma = " + ".join(
            [r"\frac{d}{dx}\left(" + sp.latex(t) + r"\right)" for t in expr.args]
        )

        pasos.append(suma)

        pasos.append(r"\textbf{Paso 3: Derivamos cada término}")

        derivadas = " + ".join(
            [sp.latex(sp.diff(t, x)) for t in expr.args]
        )

        pasos.append(derivadas)

    elif expr.is_Pow and expr.args[0] == x:

        pasos.append(r"\textbf{Paso 2: Aplicamos la regla de la potencia}")

        pasos.append(r"\frac{d}{dx}(x^n)=nx^{n-1}")

        pasos.append(sp.latex(sp.diff(expr, x)))

    elif expr.is_Mul:

        pasos.append(r"\textbf{Paso 2: Aplicamos la regla del producto}")

        pasos.append(r"(uv)' = u'v + uv'")

        pasos.append(sp.latex(sp.diff(expr, x)))

    else:

        pasos.append(r"\textbf{Aplicamos derivación directa}")

        pasos.append(sp.latex(sp.diff(expr, x)))

    return pasos

# -------- ANALISIS DE DERIVADA --------

def analizar_derivada(derivada, x):

    tipo = ""
    comportamiento = ""

    if derivada.is_number:
        tipo = "Función constante"

    elif derivada.is_polynomial():

        grado = sp.degree(derivada)

        if grado == 0:
            tipo = "Función constante"
        elif grado == 1:
            tipo = "Función lineal"
        elif grado == 2:
            tipo = "Función cuadrática"
        else:
            tipo = f"Polinomio de grado {grado}"

    else:
        tipo = "Función no polinómica"

    try:

        criticos = sp.solve(sp.diff(derivada, x), x)

        if derivada.is_number:

            if derivada > 0:
                comportamiento = "La función original es creciente en todo su dominio."
            elif derivada < 0:
                comportamiento = "La función original es decreciente en todo su dominio."
            else:
                comportamiento = "La función es constante."

        elif len(criticos) == 0:

            comportamiento = "La función mantiene el mismo comportamiento en todo su dominio."

        else:

            comportamiento = f"La derivada cambia de comportamiento en x = {criticos}"

    except:

        comportamiento = "No se pudo analizar completamente el comportamiento."

    return tipo, comportamiento

# -------- TECLADO --------

st.subheader("Teclado matemático")

c1,c2,c3,c4,c5,c6 = st.columns(6)

with c1:
    st.button("7", on_click=agregar, args=("7",))
    st.button("4", on_click=agregar, args=("4",))
    st.button("1", on_click=agregar, args=("1",))
    st.button("0", on_click=agregar, args=("0",))

with c2:
    st.button("8", on_click=agregar, args=("8",))
    st.button("5", on_click=agregar, args=("5",))
    st.button("2", on_click=agregar, args=("2",))
    st.button("x", on_click=agregar, args=("x",))

with c3:
    st.button("9", on_click=agregar, args=("9",))
    st.button("6", on_click=agregar, args=("6",))
    st.button("3", on_click=agregar, args=("3",))
    st.button("+", on_click=agregar, args=("+",))

with c4:
    st.button("-", on_click=agregar, args=("-",))
    st.button("*", on_click=agregar, args=("*",))
    st.button("/", on_click=agregar, args=("/",))
    st.button("(", on_click=agregar, args=("(",))

with c5:
    st.button(")", on_click=agregar, args=(")",))
    st.button("^2", on_click=agregar, args=("**2",))
    st.button("^3", on_click=agregar, args=("**3",))
    st.button("√", on_click=agregar, args=("sqrt(",))

with c6:
    st.button("sin", on_click=agregar, args=("sin(",))
    st.button("cos", on_click=agregar, args=("cos(",))
    st.button("tan", on_click=agregar, args=("tan(",))
    st.button("Borrar", on_click=borrar)

expr_text = st.text_input("Función:", st.session_state.expr_text)

# -------- CALCULOS --------

try:

    expr = sp.sympify(expr_text)

    derivada = sp.diff(expr, x)
    integral = sp.integrate(expr, x)

    try:
        raices = sp.solve(expr, x)
    except:
        raices = "No se encontraron raíces simbólicas"

    col1, col2 = st.columns(2)

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

        f = sp.lambdify(x, expr, "numpy")
        d = sp.lambdify(x, derivada, "numpy")

        xs = np.linspace(-10,10,400)

        ys = f(xs)
        yd = d(xs)

        fig = make_subplots(
            rows=2,
            cols=1,
            shared_xaxes=True,
            subplot_titles=("f(x)", "f'(x)")
        )

        fig.add_trace(
            go.Scatter(x=xs, y=ys, mode='lines', name='f(x)'),
            row=1, col=1
        )

        fig.add_trace(
            go.Scatter(x=xs, y=yd, mode='lines', name="f'(x)"),
            row=2, col=1
        )

        fig.update_layout(
            height=600,
            title="Función y su derivada"
        )

        st.plotly_chart(fig,use_container_width=True)

# -------- COLUMNA DERECHA --------

    with col2:

        st.subheader("Procedimiento de la derivada")

        pasos = derivada_pasos(expr, x)

        for p in pasos:
            st.latex(p)

        st.markdown("### Solución")

        st.latex("f'(x) = " + sp.latex(derivada))

        tipo, comportamiento = analizar_derivada(derivada, x)

        st.markdown("**Tipo de función de la derivada:**")
        st.write(tipo)

        st.markdown("**Comportamiento:**")
        st.write(comportamiento)

except:
    st.info("Escribe una función para comenzar.")
