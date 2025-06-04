#Uso del framework: se instala en la terminal con: pip install streamlit
import streamlit as st
#Uso de pandas: es una biblioteca para trabajar con tablas
import pandas as pd
import plotly.graph_objects as go
#Uso de plotly: es una biblioteca para la generacion de los graficos, aqui está invocando metodos que vienen de depreciacion.py
from depreciacion import linea_recta, saldo_decreciente, suma_digitos, unidad_produccion, seleccion_optima
#Titulo de la pestaña
st.set_page_config(page_title="Calculadora de Depreciación", layout="centered")
#Titulo del sitio
st.title("📉 Calculadora Inteligente de Depreciación")
#Descripcion breve
st.markdown("""
Esta herramienta calcula la depreciación de un activo usando diferentes métodos contables y recomienda el más conveniente
según el criterio elegido: *maximizar beneficios fiscales* o *minimizar la variabilidad contable*.
""")
#Datos que se van a ingresar
costo = st.number_input("💰 Costo inicial del activo:", min_value=0.0)
residual = st.number_input("🪙 Valor residual:", min_value=0.0)
vida = st.number_input("📆 Vida útil en años:", min_value=1, format="%d")
criterio = st.selectbox("🎯 ¿Cuál es tu criterio de optimización?", ["fiscal", "contable"])
#Arreglo que genera los campos del uso anual segun la vida util
uso_anual = []
st.markdown("### ⚙️ Uso anual (solo para 'Unidad de Producción')")
#Columnas
cols = st.columns(int(vida))
#Filas
for i in range(int(vida)):
    uso = cols[i].number_input(f"Año {i+1}", min_value=0.0, key=f"uso_{i}")
    uso_anual.append(uso)
uso_total = sum(uso_anual)
 #Boton y decision para el metodo 
if st.button("📊 Calcular Depreciaciones"):
    metodos = {
        "Línea Recta": linea_recta(costo, residual, vida),
        "Saldo Decreciente": saldo_decreciente(costo, vida),
        "Suma Dígitos": suma_digitos(costo, residual, vida),
        "Unidad Producción": unidad_produccion(costo, residual, uso_anual, uso_total)
    }

    mejor = seleccion_optima(metodos, criterio)
 #Generacion y resultados de la tabla
    st.subheader("📈 Resultados de los Métodos de Depreciación")
    df = pd.DataFrame(metodos)
    df.index = [f"Año {i+1}" for i in range(len(df))]
    st.dataframe(df.style.format("{:.2f}"))
 #Muestra de la recomendacion en el campo 
    st.subheader("🔍 Recomendación")
    st.success(f"Mejor método según criterio '{criterio}': *{mejor[0]}*")
 #Generacion del grafico
    st.markdown("### 📉 Comparación Gráfica")
    fig = go.Figure()
    for nombre, valores in metodos.items():
        fig.add_trace(go.Scatter(y=valores, x=list(range(1, len(valores)+1)), mode='lines+markers', name=nombre))
    fig.update_layout(title="Depreciación por Año", xaxis_title="Año", yaxis_title="Depreciación Anual", template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)