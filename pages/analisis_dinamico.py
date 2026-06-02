import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import utils as ut

# ── Configuración de la página ──────────────────────────────
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

# ── Diccionarios: nombre visible → columna real ──────────────────────────────
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

# ── Selectores ──────────────────────────────
col1, col2 = st.columns(2)
with col1:
    var_label = st.selectbox("Variable a analizar", list(variables.keys()), key="var_din")
with col2:
    grup_label = st.selectbox("Agrupar por", list(agrupaciones.keys()), key="grup_din")

columna_var = variables[var_label]
columna_grup = agrupaciones[grup_label]

# ── Agrupar y graficar ──────────────────────────────
with st.container(border=True):
    st.subheader(f"{var_label} por {grup_label}")

    datos = df.groupby(columna_grup)[columna_var].sum().reset_index()

    fig = go.Figure()

    if grup_label == "Año":
        # Línea para evolución temporal
        fig.add_trace(go.Scatter(
            x=datos[columna_grup],
            y=datos[columna_var],
            mode="lines+markers",
            fill="tozeroy",
            line_color="#1f77b4",
            hovertemplate=f"{grup_label}: %{{x}}<br>{var_label}: %{{y:,.0f}}<extra></extra>"
        ))
        fig.update_xaxes(dtick=1)
    else:
        # Barras horizontales para departamento y categoría
        datos = datos.sort_values(columna_var, ascending=True)
        fig.add_trace(go.Bar(
            y=datos[columna_grup].astype(str),
            x=datos[columna_var],
            orientation="h",
            marker_color="#2ca02c",
            text=datos[columna_var],
            texttemplate="%{text:,.0f}",
            textposition="outside",
            hovertemplate=f"<b>%{{y}}</b><br>{var_label}: %{{x:,.0f}}<extra></extra>"
        ))

    # Alto dinámico para barras de departamento (32 categorías)
    alto = 800 if grup_label == "Departamento" else 450

    fig.update_layout(
        height=alto,
        template="plotly_dark",
        xaxis_title=var_label,
        yaxis_title="",
        margin=dict(l=10, r=40, t=30, b=10),
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)