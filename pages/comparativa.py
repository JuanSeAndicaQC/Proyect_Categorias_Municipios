import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import utils as ut
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Comparativa", page_icon="📊", layout="wide",
                   initial_sidebar_state="expanded")
ut.generarMenu()
df = ut.cargar_datos()

#st.header(" Municipios respecto al promedio")
st.set_page_config(
    "📊Municipios respecto al promedio",
    "Wide",
    initial_sidebar_state="expanded"
    )

# Filtros encadenados
c1, c2, c3 = st.columns(3)

with c1:
    años = ["Todos"] + sorted(df["Año"].unique().tolist())
    año_sel = st.selectbox("Año", años)

with c2:
    cats = ["Todas"] + sorted(df["Categoria"].unique().tolist())
    cat_sel = st.selectbox("Categoría", cats)

with c3:
    deptos = ["Todos"] + sorted(df["Departamento"].unique().tolist())
    depto_sel = st.selectbox("Departamento", deptos)
    
# ── Aplicar filtros ──────────────────────────────
datos = df.copy()

if año_sel != "Todos":
    datos = datos[datos["Año"] == año_sel]
if cat_sel != "Todas":
    datos = datos[datos["Categoria"] == cat_sel]
if depto_sel != "Todos":
    datos = datos[datos["Departamento"] == depto_sel]

# Agrupar por municipio (acumula si hay varios años)
muni = (
    datos.groupby("Municipio")["Total dispositivos"]
    .sum()
    .sort_values(ascending=True)
    .reset_index()
)

# ── Validación: que haya datos ──────────────────────────────
if muni.empty:
    st.warning("No hay municipios para esta combinación de filtros.")
    st.stop()

# ── Calcular la media del grupo filtrado ──────────────────────────────
promedio = muni["Total dispositivos"].mean()

# ── Colores según posición respecto a la media ──────────────────────────────
colores = ["#2ca02c" if v >= promedio else "#d62728"
           for v in muni["Total dispositivos"]]

import plotly.graph_objects as go

#Gráfico en Plotly
with st.container(border=True):
    titulo = "Dispositivos por municipio"
    sub = []
    if año_sel != "Todos":   sub.append(f"Año {año_sel}")
    if cat_sel != "Todas":   sub.append(f"Cat. {cat_sel}")
    if depto_sel != "Todos": sub.append(depto_sel)
    if sub:
        titulo += " — " + ", ".join(sub)

    st.subheader(titulo)

    # Colores según posición respecto a la media
    colores = ["#118be3" if v >= promedio else "#ec5959"
               for v in muni["Total dispositivos"]]

    fig = go.Figure()

    # Barras horizontales
    fig.add_trace(go.Bar(
        y=muni["Municipio"],
        x=muni["Total dispositivos"],
        orientation="h",
        marker_color=colores,
        text=muni["Total dispositivos"],
        texttemplate="%{text:,.0f}",
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Dispositivos: %{x:,.0f}<extra></extra>"
    ))

    # Línea vertical del promedio
    fig.add_vline(
        x=promedio,
        line_dash="solid",
        line_color="#e8dd0d",
        line_width=5,
        annotation_text=f"PROMEDIO: {promedio:,.0f}",
        annotation_position="top",
        annotation_yshift=15
    )

    # Alto dinámico según número de municipios
    alto = max(400, len(muni) * 28)

    fig.update_layout(
        height=alto,
        template="plotly_dark",
        xaxis_title="Total dispositivos",
        yaxis_title="",
        margin=dict(l=10, r=40, t=40, b=10),
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

    st.caption("🔵 Por encima del promedio   🔴 Por debajo del promedio ")

