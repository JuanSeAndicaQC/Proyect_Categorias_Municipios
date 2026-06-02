import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import utils as ut

# Configuración de la página
st.set_page_config(
    page_title="Línea de tiempo",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

ut.generarMenu()

df = ut.cargar_datos()

st.header("📈 Evolución de entregas por municipio")
st.caption("Compara cómo evolucionaron las entregas año a año en los municipios que elijas.")

# Filtros encadenados
c1, c2 = st.columns(2)

with c1:
    deptos = sorted(df["Departamento"].unique().tolist())
    depto_sel = st.selectbox("Departamento", deptos, key="depto_linea")

with c2:
    cats = ["Todas"] + sorted(df["Categoria"].unique().tolist())
    cat_sel = st.selectbox("Categoría", cats, key="cat_linea")

# Filtrar para alimentar el multiselect
base = df[df["Departamento"] == depto_sel]
if cat_sel != "Todas":
    base = base[base["Categoria"] == cat_sel]

municipios_disponibles = sorted(base["Municipio"].unique().tolist())
municipios_sel = st.multiselect(
    "Municipios a comparar",
    options=municipios_disponibles,
    default=[],
    key="muni_linea"
)

# Validación
if not municipios_sel:
    st.warning("Selecciona al menos un municipio para ver el gráfico.")
    st.stop()

# Gráfico de líneas
with st.container(border=True):
    st.subheader(f"Evolución de entregas — {depto_sel}")

    fig = go.Figure()

    for muni in municipios_sel:
        datos_muni = (
            base[base["Municipio"] == muni]
            .groupby("Año")["Total dispositivos"]
            .sum()
            .reset_index()
            .sort_values("Año")
        )

        fig.add_trace(go.Scatter(
            x=datos_muni["Año"],
            y=datos_muni["Total dispositivos"],
            mode="lines+markers",
            name=muni,
            hovertemplate="<b>%{fullData.name}</b><br>Año: %{x}<br>Dispositivos: %{y:,.0f}<extra></extra>"
        ))

    fig.update_layout(
        height=500,
        template="plotly_dark",
        xaxis_title="Año",
        yaxis_title="Total dispositivos",
        hovermode="x unified",
        margin=dict(l=10, r=10, t=40, b=10)
    )
    fig.update_xaxes(dtick=1)

    st.plotly_chart(fig, use_container_width=True)