import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import utils as ut

st.set_page_config(
    page_title="Análisis Dinámico",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

ut.generarMenu()

df = ut.cargar_datos()

st.header("📊 Análisis Dinámico")
st.caption("Explora los datos eligiendo qué variable analizar y cómo agruparla.")

# Diccionarios: nombre visible → columna real
variables = {
    "Total dispositivos": "Total dispositivos",
    "PCs MinTIC": "PCs aportados por MinTic",
    "Tabletas estudiantes": "Tabletas MinTic para estudiantes",
    "Tabletas docentes": "Tabletas MinTic para docentes",
    "Sedes beneficiadas": "Sedes beneficiadas",
    "Inversión": "Inversión",
}

agrupaciones = {
    "Departamento": "Departamento",
    "Año": "Año",
    "Categoría": "Categoria",
}

# Dos selectores lado a lado
col1, col2 = st.columns(2)
with col1:
    var_label = st.selectbox("Variable a analizar", list(variables.keys()))
with col2:
    grup_label = st.selectbox("Agrupar por", list(agrupaciones.keys()))

# Traducir la selección a nombres de columna reales
columna_var  = variables[var_label]
columna_grup = agrupaciones[grup_label]

# Agrupar según la selección y graficar
with st.container(border=True):
    st.subheader(f"{var_label} por {grup_label}")

    datos = df.groupby(columna_grup)[columna_var].sum().reset_index()

    fig, ax = plt.subplots(figsize=(10, 5))

    if grup_label == "Año":
        # Línea para evolución temporal
        ax.plot(datos[columna_grup], datos[columna_var],
                marker="o", color="#1f77b4", linewidth=2)
        ax.fill_between(datos[columna_grup], datos[columna_var], alpha=0.15, color="#1f77b4")
        ax.set_xticks(datos[columna_grup])
        ax.grid(axis="y", linestyle="--", alpha=0.5)
    else:
        # Barras horizontales para departamento y categoría
        datos = datos.sort_values(columna_var, ascending=True)
        bars = ax.barh(datos[columna_grup].astype(str), datos[columna_var], color="#2ca02c")
        ax.bar_label(bars, fmt="{:,.0f}", padding=3, fontsize=8)
        ax.grid(axis="x", linestyle="--", alpha=0.4)

    ax.set_xlabel(var_label)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close()
