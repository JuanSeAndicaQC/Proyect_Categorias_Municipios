# DataEdu — Acceso a tecnología en municipios de categoría 5 y 6 en Colombia

Análisis del programa **Computadores para Educar (CPE)** del MinTIC en los municipios más vulnerables del país (categorías 5 y 6), mediante el cruce de datos abiertos oficiales y su visualización en una aplicación web interactiva.

## Descripción

En Colombia, los municipios de categoría 5 y 6 —los de menor población e ingresos fiscales según la Ley 1551 de 2012— concentran las mayores brechas de acceso a tecnología educativa. Este proyecto integra y analiza datos públicos para medir cómo se distribuyó la cobertura del programa Computadores para Educar entre 2010 y 2022, e identificar qué municipios recibieron menor dotación, con el fin de aportar evidencia para la focalización de futuras intervenciones de política pública.

## Fuentes de datos

1. **MinTIC — Computadores para Educar (2010–2022):** entregas de dispositivos (PCs y tabletas para estudiantes y docentes), inversión, sedes beneficiadas. Granularidad original: corte mensual por municipio.
2. **Contaduría General de la Nación (CGN):** historial de categorización municipal según la Ley 1551 de 2012.

Las dos bases se cruzan mediante el **código DIVIPOLA / DANE** del municipio, normalizado a 5 dígitos.

## Procesamiento de datos

El tratamiento de los datos se realizó en Python (Google Colab) e incluyó:

- Estandarización del código DIVIPOLA a 5 dígitos en ambas bases (manejo de ceros a la izquierda y de valores con decimales).
- Limpieza de la columna de inversión (formato de moneda a numérico).
- Agregación de los cortes mensuales de CPE a una sola fila por municipio-año, sumando las variables de flujo (dispositivos, inversión, sedes) y evitando la duplicación de registros.
- Cruce de ambas bases mediante un *left join* sobre el código de municipio.
- Filtrado a municipios de categoría 5 y 6.
- Creación de la columna derivada `Total dispositivos`, suma de todos los tipos de equipo por registro.

El resultado es un conjunto consolidado de **1.002 municipios** (43 de categoría 5 y 959 de categoría 6) a lo largo de **13 años** (2010–2022).

## Aplicación

La interfaz se desarrolló en **Streamlit** y se organiza en varias páginas:

- **Inicio / Pronóstico:** tarjetas de métricas generales y estadísticas, ranking de municipios mejor y peor atendidos, y vista del dataset.
- **Gráficos (Análisis Visual):** evolución temporal de entregas, dispositivos por departamento y comparación entre categorías 5 y 6.
- **Comparativa:** barras por municipio con línea de promedio dinámico; el color indica si el municipio está por encima (verde) o por debajo (rojo) de la media del grupo filtrado.
- **Línea de tiempo:** evolución año a año de los municipios seleccionados, con filtros encadenados por departamento y categoría.
- **Análisis Dinámico:** exploración interactiva eligiendo variable (dispositivos, PCs, tabletas, sedes, inversión) y nivel de agrupación.

Las visualizaciones interactivas usan **Plotly**.

## Tecnologías

- Python
- Pandas — procesamiento y análisis de datos
- Streamlit — interfaz web
- Plotly — visualizaciones interactivas
- Google Colab / Jupyter — limpieza y cruce de datos

## Estructura del proyecto

```
Interfaz_proyecto/
├── app.py                      # Página principal
├── utils.py                    # Funciones compartidas (menú, carga, métricas)
├── data/
│   └── df_merge.csv            # Dataset consolidado
├── media/                      # Imágenes y recursos
└── pages/
    ├── pronostico.py           # Métricas y ranking
    ├── graficos.py             # Análisis visual
    ├── comparativa.py          # Municipios vs promedio
    ├── lineatiempo.py          # Evolución por municipio
    └── analisis_dinamico.py    # Exploración por variable
```

## Cómo ejecutar

1. Instalar las dependencias:

```bash
pip install streamlit pandas plotly
```

2. Desde la carpeta del proyecto, ejecutar:

```bash
streamlit run app.py
```

3. La aplicación se abrirá en el navegador (por defecto en `http://localhost:8501`).

> Nota: la ruta del archivo de datos está definida en `utils.py`. Si se ejecuta fuera de Google Colab, ajustar la variable `PATH` a la ubicación local del proyecto.

## Alcance y limitaciones

- El análisis se realiza a nivel de **municipio**, no de institución educativa o sede individual.
- La categorización municipal cambia año a año; un municipio puede haber pertenecido a la categoría 5 o 6 solo durante parte del período.
- El estudio refleja las entregas registradas por Computadores para Educar y no contempla otras fuentes de dotación tecnológica (entidades territoriales, cooperación, sector privado).
- La métrica `Total dispositivos` agrega equipos de distinta naturaleza (computadores y tabletas) como unidades equivalentes.

## Autores

Juan Sebastián Andica Largo
Luis W. Morales M.
Santiago León

## Contexto

Proyecto desarrollado en el marco de BOOTCAMP / TALENTO TECH - ANALISIS DE DATOS, 02 de Junio del 2026.
