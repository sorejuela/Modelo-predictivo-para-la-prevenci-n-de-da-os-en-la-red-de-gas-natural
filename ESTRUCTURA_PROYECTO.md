# 📁 Estructura del Proyecto

## Organización de Archivos

```
proyectofinal/
│
├── 📓 Notebooks y Scripts
│   ├── modelo.ipynb                      # Notebook principal - Modelo SARIMA completo
│   ├── analisis_resultados_fase1.py     # Script de análisis de resultados
│   └── dashboard.py                      # Dashboard interactivo con Streamlit
│
├── 📊 Visualizaciones
│   ├── descomposicion_estacional.png          # Análisis de componentes temporales
│   ├── proceso_estacionariedad.png            # Transformaciones para estacionariedad
│   ├── diagnostico_residuos.png               # Validación del modelo
│   ├── comparacion_modelos_sarima.png         # Comparativa de configuraciones
│   ├── resultados_modelo_final.png            # Métricas del modelo optimizado
│   └── analisis_predictivo_completo.png       # Predicciones y análisis
│
├── 📄 Documentación
│   ├── README.md                         # Documentación principal del proyecto
│   ├── README_DASHBOARD.md               # Guía de uso de los dashboards
│   └── ESTRUCTURA_PROYECTO.md           # Este archivo
│
├── ⚙️ Configuración
│   ├── requirements.txt                  # Dependencias principales
│   ├── requirements_dashboard.txt        # Dependencias del dashboard
│   └── .gitignore                       # Archivos excluidos del repositorio
│
└── 📦 Datos (no incluidos en GitHub)
    └── Copia de base_datos.xlsx         # Dataset original (privado)
```

## Descripción de Componentes

### 📓 Notebooks y Scripts

#### `modelo.ipynb`
Notebook principal que contiene:
- Carga y preprocesamiento de datos
- Análisis exploratorio de datos (EDA)
- Descomposición estacional
- Transformaciones de estacionariedad
- Entrenamiento del modelo SARIMA
- Validación cruzada temporal
- Diagnóstico de residuos
- Predicciones futuras

#### `dashboard.py`
Dashboard interactivo con Streamlit que incluye:
- 4 tabs de análisis (Predicciones, Análisis Espacial, Temporal, Diagnóstico)
- Filtros interactivos (horizonte, mes, top N barrios, intervalo de confianza)
- Generación y descarga de reportes PDF
- Visualizaciones interactivas con Plotly
- Métricas en tiempo real
- Análisis espacial y temporal de roturas

### 📊 Visualizaciones

Todas las imágenes son generadas automáticamente por el notebook y muestran:
- Patrones estacionales y tendencias
- Proceso de transformación de datos
- Validación estadística del modelo
- Comparativas de rendimiento
- Predicciones con intervalos de confianza

### 📄 Documentación

- **README.md**: Descripción general, instalación, uso, metodología, despliegue web
- **README_DASHBOARD.md**: Instrucciones específicas para los dashboards
- **ESTRUCTURA_PROYECTO.md**: Esta guía de organización

### ⚙️ Configuración

#### `requirements.txt`
Dependencias completas del proyecto para análisis y modelado.

#### `requirements_dashboard.txt`
Dependencias específicas para ejecutar los dashboards.

#### `.gitignore`
Excluye archivos sensibles y temporales del repositorio.

## Flujo de Trabajo Recomendado

1. **Instalación**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Análisis y Modelado**:
   - Abrir `modelo.ipynb` en Jupyter
   - Ejecutar celdas secuencialmente
   - Revisar visualizaciones generadas

3. **Visualización Interactiva con Streamlit**:
   ```bash
   pip install -r requirements_dashboard.txt
   streamlit run dashboard.py
   ```
   El dashboard se abrirá automáticamente en http://localhost:8501

## Notas Importantes

- Los datos originales (`*.xlsx`) no están incluidos en el repositorio por privacidad
- Los entornos virtuales están excluidos del control de versiones
- Todas las visualizaciones pueden regenerarse ejecutando el notebook
- El dashboard Streamlit requiere Python 3.11 o 3.12 para funcionar correctamente

## Requisitos del Sistema

- Python 3.11 o 3.12 (recomendado)
- 4GB RAM mínimo
- 500MB espacio en disco
- Navegador web moderno (para dashboards)

## Licencia y Contacto

Ver `README.md` para información de licencia y contacto.
