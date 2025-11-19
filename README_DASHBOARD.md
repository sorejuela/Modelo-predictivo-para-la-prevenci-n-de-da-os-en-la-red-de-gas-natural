# 🔮 Dashboard Interactivo - Predicción de Roturas


Dashboard web interactivo con generación automática de reportes PDF para visualizar y analizar las predicciones del modelo SARIMA.

## 🚀 Instalación

### 1. Instalar dependencias

```bash
pip install -r requirements_dashboard.txt
```

O instalar individualmente:
```bash
pip install streamlit plotly reportlab
```

### 2. Ejecutar el dashboard

```bash
streamlit run dashboard.py
```

El dashboard se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 📊 Funcionalidades

### **Panel de Control (Sidebar)**
- 📅 **Selector de horizonte:** Elige entre 3, 6, 9 o 12 meses de predicción
- 🔍 **Filtro por mes:** Analiza un mes específico en detalle
- 🏘️ **Top N barrios:** Ajusta cuántos barrios mostrar (3-15)
- 📈 **Intervalo de confianza:** Configura el nivel de confianza (80-99%)
- 📄 **Generar PDF:** Descarga reporte ejecutivo con un click

### **4 Pestañas Principales**

#### 1️⃣ **Predicciones**
- Gráfico de serie temporal con histórico y predicciones futuras
- Intervalos de confianza dinámicos
- Tabla detallada con predicciones mes a mes
- Comparación con promedio histórico

#### 2️⃣ **Análisis Espacial**
- **Filtro por mes:** Ver barrios más afectados en un mes específico
- Top N barrios con mayor incidencia (ajustable)
- Código de colores según nivel de riesgo:
  - 🔴 Rojo: Muy Alto (>2 roturas/mes)
  - 🟠 Naranja: Alto (1.5-2 roturas/mes)
  - 🟡 Amarillo: Medio (1-1.5 roturas/mes)
  - 🟢 Verde: Bajo (<1 rotura/mes)
- Métricas de concentración y barrio crítico
- Tabla detallada con ranking completo

#### 3️⃣ **Análisis Temporal**
- **Distribución por hora:** Identifica horas críticas del día
- **Distribución por día:** Encuentra días de la semana más afectados
- **Mapa de calor Día × Hora:** Visualiza concentración de roturas
- **Recomendaciones operativas:** Sugerencias basadas en los datos

#### 4️⃣ **Diagnóstico del Modelo**
- Métricas de precisión y error
- Configuración del modelo SARIMA
- Tests estadísticos (Ljung-Box, Shapiro-Wilk)
- Comparación de evolución de modelos
- Conclusión de validación

## 📄 Reporte PDF

Al hacer click en **"📥 Generar Reporte PDF"**, se genera automáticamente un documento profesional con:

### Contenido del PDF:
1. **Portada**
   - Título del proyecto
   - Fecha y hora de generación
   - Información del modelo
   - Universidad Tecnológica de Bolívar

2. **Resumen Ejecutivo**
   - Métricas principales del modelo
   - Total de observaciones históricas
   - Promedio mensual

3. **Tabla de Predicciones**
   - Predicciones para los próximos meses (según horizonte seleccionado)
   - Intervalos de confianza inferior y superior
   - Formato tabular profesional

4. **Análisis Espacial**
   - Top N barrios con mayor incidencia
   - Ranking con roturas totales, promedio mensual y porcentaje
   - Tabla con código de colores

5. **Recomendaciones Operativas**
   - Planificación de recursos
   - Vigilancia y monitoreo
   - Actualización del modelo
   - Inversión en infraestructura

## 🎨 Características del Dashboard

### **Interactividad**
- ✅ Gráficos con zoom, pan y tooltips (Plotly)
- ✅ Filtros dinámicos que actualizan todos los gráficos
- ✅ Tablas con scroll y formato profesional
- ✅ Métricas con indicadores de cambio

### **Responsividad**
- ✅ Layout adaptable a diferentes tamaños de pantalla
- ✅ Columnas que se reorganizan automáticamente
- ✅ Gráficos que escalan según el ancho disponible

### **Rendimiento**
- ✅ Cache de datos con `@st.cache_data`
- ✅ Carga rápida de visualizaciones
- ✅ Actualización eficiente al cambiar filtros

## 🔧 Personalización

### **Colores del tema**
Puedes modificar los colores en el CSS personalizado (líneas 18-38 de `dashboard.py`):
- `#2E86AB`: Azul principal
- `#D90429`: Rojo de alertas
- `#F18F01`: Naranja
- `#06A77D`: Verde

### **Datos**
El dashboard carga automáticamente desde `Copia de base_datos.xlsx`. Para usar otros datos:
1. Asegúrate que tenga las columnas: `Fecha de Creación`, `Barrio`, `Hora`
2. Actualiza la ruta en la función `cargar_datos()` (línea 42)

### **Predicciones**
Actualmente usa datos simulados. Para integrar tu modelo real:
1. Guarda el modelo entrenado con `pickle`
2. Carga en la función `cargar_predicciones()` (línea 70)
3. Genera predicciones dinámicamente

## 📱 Despliegue

### **Opción 1: Local**
```bash
streamlit run dashboard.py
```

### **Opción 2: Streamlit Cloud (Gratis)**
1. Sube el código a GitHub
2. Ve a [share.streamlit.io](https://share.streamlit.io)
3. Conecta tu repositorio
4. ¡Listo! URL pública automática

### **Opción 3: Docker**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements_dashboard.txt
EXPOSE 8501
CMD ["streamlit", "run", "dashboard.py", "--server.port=8501"]
```

## 🐛 Solución de Problemas

### **Error: No se encuentra el archivo de datos**
```bash
FileNotFoundError: Copia de base_datos.xlsx
```
**Solución:** Asegúrate de que el archivo Excel esté en la misma carpeta que `dashboard.py`

### **Error: Módulo no encontrado**
```bash
ModuleNotFoundError: No module named 'streamlit'
```
**Solución:** Instala las dependencias:
```bash
pip install -r requirements_dashboard.txt
```

### **PDF no se genera**
```bash
WARNING: La librería reportlab no está instalada
```
**Solución:**
```bash
pip install reportlab
```

### **Puerto ocupado**
```bash
Error: Port 8501 is already in use
```
**Solución:** Usa otro puerto:
```bash
streamlit run dashboard.py --server.port=8502
```

## 📚 Tecnologías Utilizadas

- **Streamlit:** Framework web interactivo
- **Plotly:** Gráficos interactivos
- **ReportLab:** Generación de PDFs
- **Pandas:** Manipulación de datos
- **NumPy:** Cálculos numéricos

## 👥 Autores

**Universidad Tecnológica de Bolívar**  
Modelos de Regresión y Series de Tiempo con Aplicaciones en IA

## 📞 Soporte

Para problemas o sugerencias, contacta al equipo de desarrollo o abre un issue en el repositorio.

---

**¡Disfruta del dashboard! 🎉**
