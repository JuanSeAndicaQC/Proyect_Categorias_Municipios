import pandas as pd
import streamlit as st
import utils as ut
from PIL import Image
from utils import PATH

# Configuración de la página
st.set_page_config(page_title="Proyecto DANE",
                   page_icon="📊",
                   layout="wide",
                   initial_sidebar_state="expanded")

# Barra lateral (Menú)
ut.generarMenu()

#contenido principal

col_1, col_2, col_3 = st.columns(
    spec=[0.2,1,0.2],
    gap="small", 
    vertical_alignment="center",
    border=False,
    width="stretch"
)

with col_2:

    #Titulo de proyecto
    st.title("ACCESO A LAS TECNOLOGÍAS EN MUNICIPIOS DE CATEGORÍA 5 Y 6 EN COLOMBIA")

    #Texto de introducción del proyecto
    st.write(
        """
Esta aplicación consolida y analiza conjuntos de datos oficiales del programa Computadores para Educar 
y registros de clasificación municipal. 
Mediante visualizaciones interactivas y herramientas 
de exploración de datos, los usuarios pueden evaluar la cobertura del programa, 
identificar tendencias y generar información valiosa para la planificación estratégica y la asignación de recursos.
"""
    )


# imagen
    imagen = Image.open(PATH + "media/imagen_Introductoria.jpg")
    st.image(
        image=imagen,
        caption="Enfermedad cardiovascular",
        width=550
        )

#subtitulo
    st.header("Key Performance Indicators (KPIs)")

#Texto de conceptualización
    st.write(
        """
- Los siguientes indicadores resumen el alcance del programa 
entre 2010 y 2022, incluyendo municipios beneficiados, 
dispositivos entregados, sedes impactadas e inversión ejecutada, 
proporcionando una visión general de su cobertura y evolución.
"""
    )
