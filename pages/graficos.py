import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import utils as ut

# ── Configuración de la página ──────────────────────────────
st.set_page_config(
    page_title="Gráficos",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

ut.generarMenu()

df = ut.cargar_datos()

st.header("Análisis Visual")

with st.container(border=True):

    # ── Gráfico 1: Evolución temporal ──────────────────────────────
    with st.expander("📅 Evolución de entregas por año", expanded=False):
        evol = df.groupby("Año")["Total dispositivos"].sum().reset_index()

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=evol["Año"],
            y=evol["Total dispositivos"],
            mode="lines+markers",
            fill="tozeroy",
            line_color="#1f77b4",
            hovertemplate="Año: %{x}<br>Dispositivos: %{y:,.0f}<extra></extra>"
        ))
        fig.update_layout(
            height=350,
            template="plotly_dark",
            xaxis_title="Año",
            yaxis_title="Total dispositivos",
            margin=dict(l=10, r=10, t=30, b=10)
        )
        fig.update_xaxes(dtick=1)
        st.plotly_chart(fig, use_container_width=True)

    # ── Gráfico 2: Por departamento ──────────────────────────────
    with st.expander("🗺️ Dispositivos por departamento", expanded=False):
        por_depto = (
            df.groupby("Departamento")["Total dispositivos"]
            .sum()
            .sort_values(ascending=True)
            .reset_index()
        )

        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=por_depto["Departamento"],
            x=por_depto["Total dispositivos"],
            orientation="h",
            marker_color="#2ca02c",
            text=por_depto["Total dispositivos"],
            texttemplate="%{text:,.0f}",
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Dispositivos: %{x:,.0f}<extra></extra>"
        ))
        fig.update_layout(
            height=800,
            template="plotly_dark",
            xaxis_title="Total dispositivos",
            yaxis_title="",
            margin=dict(l=10, r=40, t=30, b=10)
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── Gráfico 3: Cat 5 vs Cat 6 por año ──────────────────────────────
    with st.expander("⚖️ Categoría 5 vs Categoría 6 — dispositivos por año", expanded=False):
        cat_año = (
            df.groupby(["Año", "Categoria"])["Total dispositivos"]
            .sum()
            .unstack(fill_value=0)
            .reset_index()
        )

        fig = go.Figure()
        if 5 in cat_año.columns:
            fig.add_trace(go.Bar(
                x=cat_año["Año"], y=cat_año[5],
                name="Cat. 5", marker_color="#ff7f0e",
                hovertemplate="Año: %{x}<br>Cat. 5: %{y:,.0f}<extra></extra>"
            ))
        if 6 in cat_año.columns:
            fig.add_trace(go.Bar(
                x=cat_año["Año"], y=cat_año[6],
                name="Cat. 6", marker_color="#1f77b4",
                hovertemplate="Año: %{x}<br>Cat. 6: %{y:,.0f}<extra></extra>"
            ))
        fig.update_layout(
            height=400,
            template="plotly_dark",
            barmode="group",
            xaxis_title="Año",
            yaxis_title="Total dispositivos",
            margin=dict(l=10, r=10, t=30, b=10)
        )
        fig.update_xaxes(dtick=1)
        st.plotly_chart(fig, use_container_width=True)