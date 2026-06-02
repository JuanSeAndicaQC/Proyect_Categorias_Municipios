import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import utils as ut

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

#Gráfico 1: Evolución temporal
    with st.expander("📅 Evolución de entregas por año", expanded=False):

        evol = df.groupby("Año")["Total dispositivos"].sum().reset_index()

        fig, ax = plt.subplots(figsize=(10, 3))
        ax.plot(evol["Año"], evol["Total dispositivos"],
                marker="o", color="#1f77b4", linewidth=2)
        ax.fill_between(evol["Año"], evol["Total dispositivos"], alpha=0.15, color="#1f77b4")
        ax.set_xlabel("Año")
        ax.set_ylabel("Total dispositivos")
        ax.set_xticks(evol["Año"])
        ax.grid(axis="y", linestyle="--", alpha=0.5)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close()

    # Gráfico 2: Por departamento
    with st.expander("🗺️ Dispositivos por departamento", expanded=False):

        por_depto = (
            df.groupby("Departamento")["Total dispositivos"]
            .sum()
            .sort_values(ascending=True)
            .reset_index()
        )

        fig, ax = plt.subplots(figsize=(10, 8))
        bars = ax.barh(por_depto["Departamento"], por_depto["Total dispositivos"],
                    color="#2ca02c")
        ax.set_xlabel("Total dispositivos")
        ax.bar_label(bars, fmt="{:,.0f}", padding=3, fontsize=8)
        ax.grid(axis="x", linestyle="--", alpha=0.4)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close()

    #Gráfico 3: Cat 5 vs Cat 6 por año
    with st.expander("⚖️ Categoría 5 vs Categoría 6 — dispositivos por año", expanded=False):

        cat_año = (
            df.groupby(["Año", "Categoria"])["Total dispositivos"]
            .sum()
            .unstack(fill_value=0)
            .reset_index()
        )

        x = cat_año["Año"]
        ancho = 0.35
        fig, ax = plt.subplots(figsize=(10, 4))

        if 5 in cat_año.columns:
            ax.bar(x - ancho/2, cat_año[5], ancho, label="Cat. 5", color="#ff7f0e")
        if 6 in cat_año.columns:
            ax.bar(x + ancho/2, cat_año[6], ancho, label="Cat. 6", color="#1f77b4")

        ax.set_xlabel("Año")
        ax.set_ylabel("Total dispositivos")
        ax.set_xticks(x)
        ax.legend()
        ax.grid(axis="y", linestyle="--", alpha=0.4)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close()