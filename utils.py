from numpy.matrixlib import defmatrix
import streamlit as st
from PIL import Image
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from pickle import load, dump

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import export_graphviz
from sklearn.metrics import (
    accuracy_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
    RocCurveDisplay,
    PrecisionRecallDisplay
    )

# Crear las rutas (Los de visual no lo necesitan)
# Ruta en Colab
PATH = ""

def generarMenu():
    with st.sidebar:
        # Creamos 2 columnas
        col_1, col_2 = st.columns(spec=2)   
        with col_1:
            logo = Image.open(PATH + "media/mapa_Colombia.png")
            st.image(image=logo,
                    width=80)
        with col_2:
            st.title("DataEdu")


#Opciones de menú
        st.page_link(
            page="app.py",
            label="Inicio",
            #icon="❤️​"
        )
        st.page_link(
            page="pages/comparativa.py",
            label="Comparativa",
            #icon="📊"
        )
        st.page_link(
            page="pages/linea_tiempo.py",
            label="Linea de tiempo Municipios",
            #icon="📊"
        )
        st.page_link(
            page="pages/pronostico.py",
            label="Pronóstico",
            #icon="❤️‍🩹​"
        )
        #st.page_link(
        #    page="pages/arboles.py",
        #    label="Arboles",
        #    #icon="❤️‍🩹​"
        #)
        st.page_link(
            page="pages/graficos.py",
            label="Graficos",
            #icon="❤️‍🩹​"
        )
        st.page_link(
            page="pages/analisis_dinamico.py",
            label="Análisis Dinámico",
            #icon="📊"
                
)

# Función para cargar los datos
# Decorador para memoria cache
@st.cache_data
def cargar_datos():
    ruta = PATH + "data/df_merge.csv"
    df = pd.read_csv(ruta, encoding="utf-8", sep=",")
    return df

# Método para el análisis inicial de los datos
def eda(df: pd.DataFrame):
    with st.expander(
        "DataSet",
        expanded=False,
        #icon="📂"
        ):
        st.dataframe(df, hide_index=True)



# ── Helpers numéricos ──────────────────────────────────────────────────────────

def limpiar_inversion(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Inversión"] = (
        df["Inversión"]
        .astype(str)
        .str.strip()
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)    # quita la coma de miles
        .astype(float)                         # el punto decimal ya está bien
    )
    return df

#Parano traer datos duplicados si no encerrarlo en uno solo
def metricas_generales(df: pd.DataFrame) -> dict:
    total_municipios   = df[["Cod Municipio", "Municipio"]].drop_duplicates().shape[0]
    total_dispositivos = df["Total dispositivos"].sum()
    total_inversion    = df["Inversión"].sum()

    # Municipios que NUNCA recibieron nada en todo el período
    por_municipio = df.groupby("Cod Municipio")["Total dispositivos"].sum()
    sin_entrega   = (por_municipio == 0).sum()

    return {
        "total_municipios":   total_municipios,
        "total_dispositivos": int(total_dispositivos),
        "sin_entrega":        int(sin_entrega),
        "total_inversion":    total_inversion,
    }


def metricas_estadisticas(df: pd.DataFrame) -> dict:
    por_municipio = df.groupby("Municipio")["Total dispositivos"].sum()
    ultimo_año    = df[df["Total dispositivos"] > 0].groupby("Municipio")["Año"].max()
    obsoletos     = (ultimo_año <= 2015).sum()   # última entrega hace +7 años

    return {
        "promedio_disp":   round(por_municipio.mean(), 1),
        "mediana_disp":    round(por_municipio.median(), 1),
        "max_municipio":   por_municipio.idxmax(),
        "max_valor":       int(por_municipio.max()),
        "obsoletos":       int(obsoletos),
        "año_pico":        int(df.groupby("Año")["Total dispositivos"].sum().idxmax()),
    }


    
