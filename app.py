import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Explorador Matemático PRO", layout="wide")

st.title("Explorador Matemático PRO")

x = sp.symbols('x')

# ---------- MEMORIA ----------
if "expr_text" not in st.session_state:
    st.session_state.expr_text = ""

def agregar(valor):
    st.session_state.expr_text += valor

def borrar():
    st.session_state.expr_text = ""

# ---------- TECLADO ----------
st.subheader("Teclado Matemático")

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

# ---------- CAMPO DE FUNCION ----------
expr_text = st.text_input("Función:", st.session_state.expr_text)

# ---------- CÁLCULOS ----------
try:

    expr = sp.sympify(expr_text)

    derivada = sp.diff(expr, x)
    integral = sp.integrate(expr, x)

    try:
        raices = sp.solve(expr, x)
    except:
        raices = "No simbólicas"

    col1, col2 = st.columns([2,1])

    # ---------- GRAFICA ----------
    with col1:

        f = sp.lambdify(x, expr, "numpy")
        d = sp.lambdify(x, derivada, "numpy")

        xs = np.linspace(-10,10,500)
        ys = f(xs)

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=xs,
            y=ys,
            mode='lines',
            name='f(x)'
        ))

        # tangente
        punto = st.slider("Punto para recta tangente", -5.0, 5.0, 0.0)

        pendiente = d(punto)
        y0 = f(punto)

        tangente = pendiente*(xs-punto)+y0

        fig.add_trace(go.Scatter(
            x=xs,
            y=tangente,
            mode='lines',
            name='Tangente'
        ))

        fig.add_trace(go.Scatter(
            x=[punto],
            y=[y0],
            mode='markers',
            name='Punto'
        ))

        fig.update_layout(
            title="Gráfica interactiva",
            xaxis_title="x",
            yaxis_title="y"
        )

        st.plotly_chart(fig, use_container_width=True)

    # ---------- RESULTADOS ----------
    with col2:

        st.subheader("Resultados")

        st.markdown("**Función**")
        st.latex(sp.latex(expr))

        st.markdown("**Derivada**")
        st.latex(sp.latex(derivada))

        st.markdown("**Integral**")
        st.latex(sp.latex(integral))

        st.markdown("**Raíces**")
        st.write(raices)

except:
    st.info("Escribe una función para comenzar.")
