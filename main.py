#Uso del framework: se instala en la terminal con: pip install streamlit
import streamlit as st
#Uso de pandas: es una biblioteca para trabajar con tablas
import pandas as pd
import plotly.graph_objects as go
#Uso de plotly: es una biblioteca para la generacion de los graficos, aqui está invocando metodos que vienen de depreciacion.py
from depreciacion import linea_recta, saldo_decreciente, suma_digitos, unidad_produccion, seleccion_optima

st.set_page_config(page_title="Calculadora de Depreciación", layout="centered")
# Estilo personalizado con CSS
st.markdown("""
    <style>
        /* Fondo con imagen y capa oscura */
        .stApp {
            background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)),
                        url("https://media.istockphoto.com/id/1436149179/es/foto/la-moneda-del-d%C3%B3lar-estadounidense-cae-disminuci%C3%B3n-del-tipo-de-cambio-devaluaci%C3%B3n-y-utilidades.jpg?s=612x612&w=0&k=20&c=wCLokUIH0Ur5JtKb8gjZQBvs3pTH2RrXoEPrDTYiM5A=");
            background-size: auto;
            background-position: center;
            background-attachment: fixed;
        }

        /* Texto en blanco */
        html, body, [class*="css"] {
            color: white;
        }

        /* Estilo de botones */
        .stButton > button {
            background-color: #00aaff;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 0.5em 1em;
        }

        .stButton > button:hover {
            background-color: #008ecc;
        }

        /* Entradas con fondo blanco para contraste */
        input, textarea, select {
            background-color: rgba(255, 255, 255, 0.85);
            color: black;
            border-radius: 6px;
        }

        /* Tablas y cuadros de resultado */
        .stDataFrame, .stTable {
            background-color: rgba(255,255,255,0.85);
            color: black;
        }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown(
        """
        <div style="text-align: center;">
    <img src="https://memoria.ues.edu.sv/wp-content/uploads/sites/46/2023/09/logo-ues-blanco.png" width="150" alt="Logo UES">
    <br><br>
    <h2><strong>Universidad de El Salvador</strong></h2>
    <h3><strong>Desarrolladores</strong></h3>
    <ul style="list-style-type: none; padding: 0; font-size: 12px; margin: 0 auto; display: inline-block; text-align: left;">
        <li>ERAZO GARCIA, JOSUE NATANAEL – EG22009</li>
        <li>GARCÍA VALIENTE, JOSUE ADAN – GV22023</li>
        <li>MEJÍA MARTÍNEZ, WENDY CAROLINA – MM18069</li>
        <li>SANTOS GAMEZ, KATHERINE ALEXANDRA – SG21038</li>
        <li>VILLALTA OVIEDO, HECTOR ALEXANDER – VO09005</li>
    </ul>
</div>

        """,
        unsafe_allow_html=True
    )



st.title("📉 Calculadora de Depreciación")

with st.expander("📝 Planteamiento del Problema", expanded=True):
    st.markdown("""
En el ámbito contable y financiero, calcular la depreciación adecuada de un activo es fundamental tanto para la toma de decisiones empresariales como para el cumplimiento fiscal.

La elección del método de depreciación puede afectar significativamente:

- La distribución del gasto contable a lo largo del tiempo.
- El valor en libros del activo.
- El impacto fiscal derivado del gasto por depreciación y, por tanto, del cálculo del impuesto sobre la renta.

Por ello, esta herramienta permite comparar distintos métodos de depreciación tomando en cuenta variables clave como:

- **Costo inicial del activo**
- **Valor residual**
- **Vida útil**
- **Tasa de uso anual del activo**
- **Impacto fiscal** (dependiendo del criterio elegido)

El objetivo es no solo calcular los valores de depreciación anual, sino también **recomendar el método más conveniente** según el criterio del usuario: optimización fiscal o estabilidad contable.
    """)


costo = st.number_input("💰 Costo inicial del activo:", min_value=0.0)
residual = st.number_input("🪙 Valor residual:", min_value=0.0)
vida = st.number_input("📆 Vida útil en años:", min_value=1, format="%d")
criterio = st.selectbox("🎯 ¿Cuál es tu criterio de optimización?", ["fiscal", "contable"])

uso_anual = []
st.markdown("### ⚙️ Uso anual")

cols = st.columns(int(vida))

for i in range(int(vida)):
    uso = cols[i].number_input(f"Año {i+1}", min_value=0.0, key=f"uso_{i}")
    uso_anual.append(uso)
uso_total = sum(uso_anual)

if st.button("📊 Calcular Depreciaciones"):
    metodos = {
        "Línea Recta": linea_recta(costo, residual, vida),
        "Saldo Decreciente": saldo_decreciente(costo, vida),
        "Suma Dígitos": suma_digitos(costo, residual, vida),
        "Unidad Producción": unidad_produccion(costo, residual, uso_anual, uso_total)
    }

    mejor = seleccion_optima(metodos, criterio)

    st.subheader("📈 Resultados de los Métodos de Depreciación")
    df = pd.DataFrame(metodos)
    df.index = [f"Año {i+1}" for i in range(len(df))]
    st.dataframe(df.style.format("{:.2f}"))

    st.subheader("🔍 Recomendación")
    st.success(f"Mejor método según criterio '{criterio}': *{mejor[0]}*")

    st.markdown("### 📉 Comparación Gráfica")
    fig = go.Figure()
    for nombre, valores in metodos.items():
        fig.add_trace(go.Scatter(y=valores, x=list(range(1, len(valores)+1)), mode='lines+markers', name=nombre))
    fig.update_layout(title="Depreciación por Año", xaxis_title="Año", yaxis_title="Depreciación Anual", template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)