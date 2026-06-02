import streamlit as st
import pandas as pd
import utils as ut

# Configuración de la página
st.set_page_config(page_title="Pronóstico",
                   page_icon="❤️‍🩹",
                   layout="wide",
                   initial_sidebar_state="expanded")  # Ctrl + S -> Guardar

# Barra lateral (Menú)
ut.generarMenu()

# Cargar Datos
df_inicial = ut.cargar_datos()

# temporal — para diagnosticar
#st.write("Índice:", df_inicial.index.name)
#st.write("Columnas:", [repr(c) for c in df_inicial.columns])

df= ut.limpiar_inversion(df_inicial)  # ← línea nueva

# Presentar la información
st.header("Análisis Exploratorio")
# usamos un contenedor
with st.container(
    border=True,
    width="stretch",
    height="content",
    horizontal_alignment="distribute",
    vertical_alignment="distribute"
    ):    

    ut.eda(df=df_inicial)

# Análisis estadístico
st.header("Análisis Estadístico")

with st.container(border=True):
    with st.expander("Datos Generales", expanded=False):
        m = ut.metricas_generales(df)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Municipios analizados",   f"{m['total_municipios']:,}",    "Cat. 5 y 6")
        c2.metric("Dispositivos entregados",  f"{m['total_dispositivos']:,}",  "2010 – 2022")
        c3.metric("Sin ninguna entrega",      f"{m['sin_entrega']:,}",         "municipios")
        c4.metric("Inversión total",
                f"${m['total_inversion']/1_000_000_000:.1f}B COP",             "acumulada")

    with st.expander("Datos Estadísticos", expanded=False):
        e = ut.metricas_estadisticas(df)

        c1, c2, c3 = st.columns(3)
        c1.metric("Promedio dispositivos/municipio", f"{e['promedio_disp']:,}",
                f"Mediana: {e['mediana_disp']:,}")
        c2.metric("Municipio más atendido",           e["max_municipio"],
                f"{e['max_valor']:,} dispositivos")
        c3.metric("Equipos posiblemente obsoletos",   f"{e['obsoletos']:,}",
                "última entrega ≤ 2015")

        c4, c5, _ = st.columns(3)
        c4.metric("Año con más entregas", str(e["año_pico"]), "pico histórico")
        c5.metric("Años de datos",        "13",               "2010 – 2022")

#Top y Bottom 10 municipios

# Acumular dispositivos por municipio (sumando sus 13 años)
    ranking = (
        df.groupby(["Municipio", "Departamento"])["Total dispositivos"]
        .sum()
        .reset_index()
        .sort_values("Total dispositivos", ascending=False)
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Top 10 — más dispositivos**")
        st.dataframe(
            ranking.head(10).reset_index(drop=True),
            hide_index=True,
            use_container_width=True
        )

    with col2:
        st.markdown("**Bottom 10 — menos dispositivos**")
        st.dataframe(
            ranking.tail(10).sort_values("Total dispositivos").reset_index(drop=True),
            hide_index=True,
            use_container_width=True
        )

