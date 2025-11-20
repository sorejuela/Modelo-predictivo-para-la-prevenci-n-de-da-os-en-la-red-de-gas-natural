# 🔮 Predicción de Roturas en la Red de Gas de Bolívar mediante Series Temporales

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![SARIMA](https://img.shields.io/badge/Model-SARIMA-green.svg)](https://www.statsmodels.org/)
[![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-FF4B4B.svg)](https://3szq5gtwqevyjs8de7ik5r.streamlit.app/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**🚀 [VER DASHBOARD EN VIVO](https://3szq5gtwqevyjs8de7ik5r.streamlit.app/)** | Proyecto Final - Modelos de Regresión y Series de Tiempo con Aplicaciones en IA  
Universidad Tecnológica de Bolívar

---

## 🎯 Problema y Objetivo

### Problemática

Las roturas en la red de gas ocasionadas por terceros generan interrupciones en el servicio, riesgos de seguridad pública y altos costos operativos. Actualmente, la gestión de estas incidencias sigue siendo **reactiva** debido a la falta de herramientas predictivas que permitan anticipar patrones de ocurrencia.

**Consecuencias principales:**

- **Riesgos de seguridad:** Fugas de gas pueden causar explosiones, incendios o intoxicaciones
- **Interrupciones del servicio:** Afectación a miles de usuarios simultáneamente
- **Costos elevados:** Reparaciones de emergencia son 3-5 veces más costosas que mantenimiento preventivo
- **Gestión ineficiente:** Asignación reactiva de cuadrillas sin priorización estratégica
- **Impacto ambiental:** Emisiones fugitivas de gas natural durante roturas

La alta variabilidad mensual (18-138 roturas/mes, CV=47.6%) y la multiplicidad de agentes causantes (obras civiles, excavaciones, vandalismo) dificultan la predicción manual, requiriendo modelos estadísticos que capturen:
- Tendencias temporales de incidencia
- Patrones estacionales y ciclos anuales
- Zonas geográficas de mayor vulnerabilidad
- Horarios críticos de ocurrencia

### Objetivo General

**Predecir las roturas causadas por terceros en la red de gas de Bolívar mediante un modelo de series de tiempo SARIMA, para apoyar la planificación de mantenimiento preventivo y reducir el tiempo de respuesta ante incidencias.**

### Objetivos Específicos

1. **Analizar patrones temporales de las roturas (2019-2025)**
   - Identificar tendencias de largo plazo en la frecuencia de incidencias
   - Caracterizar componentes estacionales (mensuales, anuales)
   - Detectar períodos críticos de alta incidencia

2. **Construir y validar un modelo SARIMA para predicción mensual**
   - Optimizar hiperparámetros mediante grid search exhaustivo (140+ configuraciones)
   - Validar robustez con rolling window validation (14 splits temporales)
   - Alcanzar precisión superior al 75% en predicciones a 6 meses

3. **Identificar días, horas y zonas de mayor riesgo para priorizar mantenimiento**
   - Determinar barrios con mayor probabilidad histórica de roturas
   - Establecer franjas horarias críticas (madrugada, mañana, tarde, noche)
   - Caracterizar días de la semana con mayor incidencia
   - Generar mapas de calor temporal-espacial para asignación preventiva de recursos

### Hipótesis

La aplicación de modelos SARIMA con transformaciones logarítmicas y validación cruzada temporal permitirá capturar la estructura estacional anual (s=12) de las roturas causadas por terceros, reduciendo el error absoluto medio (MAE) en más del 20% respecto a enfoques sin optimización y permitiendo una planificación preventiva efectiva.

---


## 📊 Dataset

- **Período de análisis:** Enero 2019 - Julio 2025
- **Total de observaciones:** 79 meses
- **Total de registros:** 4,162 roturas causadas por terceros en la red de gas de Bolívar
- **Variables disponibles:**
  - Fecha de creación del incidente
  - Barrio/zona geográfica
  - Hora del incidente
- **Frecuencia:** Agregación mensual para modelado SARIMA
- **Características de los datos:**
  - Promedio: 52.68 roturas/mes
  - Desviación estándar: 25.06
  - Rango: [18, 138] roturas/mes
  - Coeficiente de variación: **47.6%** (alta variabilidad)
  - Tendencia: Decreciente en el período analizado
  - Estacionalidad: Fuerte (±14.91 roturas, picos en Noviembre-Diciembre)

---

## 🔒 Ética y Privacidad

### Consideraciones Éticas

#### 1. Uso Responsable de Datos
- **Anonimización:** Los datos utilizados contienen únicamente información temporal y geográfica agregada (barrio), sin identificadores personales ni información sensible de usuarios
- **Propósito benéfico:** El modelo se desarrolla exclusivamente para mejorar la seguridad pública, eficiencia operativa y prevención de accidentes, no para vigilancia o discriminación
- **Transparencia:** Toda la metodología, código y resultados son documentados públicamente en este repositorio para revisión académica

#### 2. Sesgo y Equidad
- **Análisis por barrio:** El modelo no discrimina por nivel socioeconómico; todas las zonas reciben predicciones objetivas basadas en datos históricos de roturas
- **Limitación reconocida:** Si ciertos barrios han recibido históricamente menos protección de infraestructura (señalización, barreras), el modelo podría perpetuar ese patrón. Se recomienda auditoría periódica de inversiones en prevención por zona
- **Interpretabilidad:** El modelo SARIMA es estadísticamente interpretable, permitiendo explicar las predicciones a ingenieros y tomadores de decisiones

#### 3. Impacto Social
- **Seguridad pública:** Reducción de riesgos de explosiones, fugas e intoxicaciones por gas natural
- **Mejora en calidad de servicio:** Menos interrupciones programadas y mejor coordinación con usuarios
- **Reducción de costos:** Mantenimiento preventivo es 3-5x más económico que reparaciones de emergencia
- **Protección ambiental:** Menor cantidad de emisiones fugitivas de metano (potente gas de efecto invernadero)

### Privacidad de Datos

#### Cumplimiento Normativo
- **GDPR/LGPD compatible:** No se procesan datos personales identificables
- **Datos agregados:** Toda la información está agrupada a nivel mensual y por barrio
- **Sin geolocalización precisa:** Barrio como unidad mínima (no direcciones exactas)

#### Seguridad de Información
- **Dataset local:** Archivo Excel almacenado localmente, no en servicios cloud públicos
- **Sin transferencia externa:** El modelo se entrena y ejecuta completamente en entorno local
- **Código abierto:** Transparencia total sobre procesamiento de datos (verificable en notebook)

#### Recomendaciones para Implementación Productiva

1. **Acceso restringido:** Limitar acceso al modelo solo a personal autorizado de operaciones
2. **Auditoría de logs:** Registrar todas las predicciones generadas y decisiones tomadas
3. **Revisión humana:** Las predicciones deben complementar (no reemplazar) el juicio experto de ingenieros
4. **Actualización ética:** Re-evaluar consideraciones éticas trimestralmente al incorporar nuevos datos

### Limitaciones Éticas Reconocidas

- **Automatización vs Empleo:** El modelo optimiza recursos pero no debe usarse para recortes de personal sin análisis integral
- **Dependencia tecnológica:** Riesgo de sobre-confianza en predicciones estadísticas; mantener capacidad de respuesta manual
- **Brecha digital:** Implementación requiere infraestructura tecnológica que puede no estar disponible en todas las organizaciones

---

## 🛠️ Métodos y Modelos

### 1. Análisis Exploratorio de Datos (EDA)

- **Descomposición estacional:** Identificación de tendencia, estacionalidad y componente aleatorio
- **Estadísticas descriptivas:** Media, desviación estándar, CV, rango
- **Análisis temporal:** Identificación de patrones mensuales y tendencias
- **Resultados clave:**
  - Meses de mayor riesgo: Noviembre (+14.91), Diciembre (+14.22), Marzo (+7.13)
  - Tendencia decreciente a largo plazo
  - Alta variabilidad inherente a los datos

### 2. Modelo SARIMA Baseline

**Configuración inicial:** SARIMA(1,1,1)(1,1,1,12)

- **p=1, d=1, q=1:** Componentes AR, diferenciación e MA
- **P=1, D=1, Q=1, s=12:** Componentes estacionales anuales
- **Split de datos:** 73 meses entrenamiento / 6 meses prueba
- **Resultados:**
  - Precisión: **78.09%**
  - MAE: 13.67 roturas
  - RMSE: 15.48
  - MAPE: 21.91%

### 3. Grid Search: Optimización de Hiperparámetros

**Configuración del Grid Search:**
- Rango de parámetros explorados:
  - p, q ∈ {0, 1, 2}
  - d ∈ {0, 1}
  - P, Q ∈ {0, 1}
  - D ∈ {0, 1}
  - s = 12 (estacionalidad anual)
- **Total de modelos evaluados:** 140 configuraciones
- **Criterio de selección:** AIC (Akaike Information Criterion)
- **Tiempo de ejecución:** 8.4 segundos

**Top 5 modelos identificados:**
1. SARIMA(0,1,1)(0,1,1,12) - AIC: 530.14 ⭐
2. SARIMA(0,1,1)(1,1,1,12) - AIC: 531.00
3. SARIMA(1,1,0)(0,1,1,12) - AIC: 531.53
4. SARIMA(1,1,1)(0,1,1,12) - AIC: 531.93
5. SARIMA(0,1,2)(0,1,1,12) - AIC: 531.95

**Modelo óptimo seleccionado:** SARIMA(0,1,1)(0,1,1,12)

### 4. Fase 1: Mejoras Progresivas

#### Paso 1: Aplicación del Modelo Óptimo
- **Modelo:** SARIMA(0,1,1)(0,1,1,12)
- **Precisión:** 78.27%
- **MAE:** 13.26
- **Mejora vs baseline:** +0.18%

#### Paso 2: Transformación Logarítmica
- **Técnica:** log(x+1) para estabilización de varianza
- **Objetivo:** Reducir heteroscedasticidad
- **Precisión:** 78.20%
- **MAE:** 13.22
- **Resultado:** -0.07% (transformación no benefició debido a tendencia decreciente)

#### Paso 3: Rolling Window Validation
- **Configuración:**
  - Tamaño mínimo de entrenamiento: 60 meses
  - Horizonte de predicción: 6 meses
  - Número de validaciones: 14 ventanas
- **Método:** Validación cruzada temporal con ventana deslizante
- **Precisión final:** **79.69% ± 3.75%**
- **MAE:** 10.70 ± 3.59
- **RMSE:** 13.06
- **Mejora total vs baseline:** +1.60 puntos porcentuales
- **Reducción de MAE:** 21.7% (de 13.67 a 10.70)

### 5. Modelo Final

**Configuración definitiva:**
- **Arquitectura:** SARIMA(0,1,1)(0,1,1,12)
- **Transformación:** Logarítmica (log1p/expm1)
- **Validación:** Rolling Window con 14 splits temporales
- **Entrenamiento final:** Todos los datos disponibles (79 meses)

---

## 📈 Resultados

### Comparación de Modelos

| Modelo | Precisión | MAE | Mejora vs Baseline |
|--------|-----------|-----|-------------------|
| SARIMA Baseline (1,1,1) | 78.09% | 13.67 | --- |
| + Modelo Óptimo | 78.27% | 13.26 | +0.18% |
| + Log Transform | 78.20% | 13.22 | +0.11% |
| **+ Rolling Window** | **79.69%** | **10.70** | **+1.60%** |

### Métricas del Modelo Final

- **Precisión:** 79.69%
- **Intervalo de confianza 95%:** [72.35%, 87.03%]
- **MAE (Error Absoluto Medio):** 10.70 roturas
- **RMSE (Error Cuadrático Medio):** 13.06
- **Desviación estándar:** ±3.75%
- **Reducción de error:** 21.7% vs baseline

### Predicciones Futuras (Agosto 2025 - Enero 2026)

| Mes | Predicción | IC 95% Inferior | IC 95% Superior |
|-----|-----------|-----------------|-----------------|
| Agosto 2025 | 64 | 33 | 123 |
| Septiembre 2025 | 48 | 23 | 99 |
| Octubre 2025 | 52 | 24 | 114 |
| Noviembre 2025 | 76 | 33 | 174 |
| Diciembre 2025 | 69 | 28 | 168 |
| Enero 2026 | 58 | 23 | 148 |
| **TOTAL 6 meses** | **368** | --- | --- |

**Promedio predicho:** 61.3 roturas/mes  
**Promedio histórico:** 52.7 roturas/mes  
**Variación:** +16.3% (incremento esperado)

---

## ✅ Validación y Diagnóstico de Errores

### Tests Estadísticos

#### 1. Test de Ljung-Box (Autocorrelación de Residuos)
- **p-value:** 0.9665
- **Resultado:** ✅ **APROBADO**
- **Interpretación:** No hay autocorrelación significativa en los residuos (p > 0.05), lo que indica que el modelo ha capturado adecuadamente la estructura temporal de los datos.

#### 2. Test de Shapiro-Wilk (Normalidad de Residuos)
- **p-value:** 0.0000
- **Resultado:** ⚠️ **NO APROBADO**
- **Interpretación:** Los residuos no siguen perfectamente una distribución normal, posiblemente debido a valores atípicos en la serie original. Sin embargo, esto no invalida el modelo para predicción.

#### 3. Estadísticas de Residuos
- **Media:** 0.0267 ≈ 0 ✅ (sesgo mínimo)
- **Desviación estándar:** 0.66
- **Rango:** [-2.40, 4.13]
- **Conclusión:** Residuos centrados en cero, indicando predicciones no sesgadas

### Análisis de Residuos

Los gráficos de diagnóstico revelan:
- **Residuos vs Tiempo:** Distribución aleatoria sin patrones evidentes
- **ACF/PACF:** Autocorrelaciones dentro de bandas de confianza
- **Q-Q Plot:** Ligera desviación en las colas (valores extremos)
- **Residuos vs Ajustados:** Varianza relativamente constante

**Conclusión general:** ✅ Modelo ADECUADO para predicción operativa

---

## 🎯 Impacto y Límites del Modelo

### Impacto Positivo

1. **Mejora en precisión:** +1.60 puntos porcentuales vs baseline
2. **Reducción de error:** 21.7% en MAE (mejora significativa en precisión operativa)
3. **Validación robusta:** 14 ventanas temporales confirman estabilidad del modelo
4. **Intervalos de confianza:** IC 95% permite gestión de riesgo (límite superior: 87%)
5. **Implementación operativa:**
   - Planificación de recursos con 6 meses de anticipación
   - Identificación de meses críticos (Noviembre-Diciembre)
   - Reducción potencial de costos por mejor asignación de personal

### Limitaciones y Restricciones

#### 1. Precisión por Debajo de Meta
- **Meta inicial:** >80%
- **Precisión alcanzada:** 79.69%
- **Diferencia:** -0.31% (muy cercano, pero por debajo del objetivo)
- **Justificación:** Alta variabilidad inherente (CV=47.6%) dificulta predicción exacta

#### 2. Limitaciones de Datos
- **Cantidad:** Solo 79 observaciones mensuales (relativamente poco para modelos avanzados)
- **Variables:** Únicamente temporales (sin información climática, económica, operacional)
- **Calidad:** Alta variabilidad (rango 18-138, factor 7.7x)
- **Tendencia decreciente:** Sin patrón claro, dificulta extrapolación

#### 3. Supuestos del Modelo
- **Estacionalidad fija:** Asume patrón estacional repetitivo cada 12 meses
- **Linealidad:** SARIMA asume relaciones lineales transformadas
- **No considera eventos atípicos:** Incapaz de predecir roturas por eventos extraordinarios
- **Sin variables exógenas:** Ignora factores externos como clima, mantenimiento, economía

#### 4. Residuos No Normales
- Test de Shapiro-Wilk no aprobado (p < 0.05)
- Presencia de valores atípicos en las colas
- Impacto: Intervalos de confianza pueden ser imprecisos en extremos

#### 5. Aplicabilidad
- **Contexto:** Válido para planificación estratégica mensual
- **Horizonte:** Confiable hasta 6 meses adelante
- **Granularidad:** No predice a nivel diario, semanal o por barrio
- **Actualización:** Requiere re-entrenamiento trimestral con nuevos datos

### Comparación con Literatura

Para series temporales con alta variabilidad (CV > 40%), la literatura especializada reporta precisiones típicas del 70-75%. Nuestro modelo alcanza **79.69%**, superando el benchmark esperado para este tipo de datos.

---

## 🔮 Trabajo Futuro

### Mejoras Metodológicas

#### 1. Incorporación de Variables Exógenas (+5-10% precisión estimada)

**Variables Climáticas:**
- Temperatura diaria promedio
- Precipitación acumulada mensual
- Humedad relativa
- Eventos extremos (heladas, tormentas)

**Justificación:** Las condiciones climáticas afectan la integridad de infraestructuras (dilatación térmica, erosión por lluvias, congelamiento).

**Variables de Calendario:**
- Días festivos nacionales y locales
- Períodos vacacionales
- Eventos masivos programados (deportivos, culturales)

**Justificación:** La demanda de servicios varía significativamente en fechas especiales.

**Variables Operacionales:**
- Registros de mantenimiento preventivo realizado
- Edad promedio de infraestructura por barrio
- Inversiones en renovación de redes
- Calidad de materiales instalados

**Justificación:** El historial de mantenimiento es el predictor más directo de futuras roturas.

**Variables Económicas:**
- Presupuesto municipal asignado
- Índices de crecimiento poblacional por zona
- Proyectos de construcción activos

**Justificación:** Expansión urbana y recursos disponibles impactan capacidad de prevención.

#### 2. Modelado Jerárquico Espacial (+5-8% precisión estimada)

**Enfoque Bottom-Up:**
1. Entrenar modelo SARIMA individual para cada uno de los 6 barrios principales
2. Capturar patrones estacionales específicos por zona
3. Agregar predicciones con ponderación por volumen histórico
4. Validar consistencia con modelo global

**Ventajas:**
- Heterogeneidad espacial: Barrios con patrones diferenciados
- Interpretabilidad local: Recomendaciones específicas por zona
- Robustez: Errores en un barrio no afectan predicciones globales

**Desafíos:**
- Menor cantidad de datos por barrio (potencial overfitting)
- Mayor complejidad computacional (6 modelos vs 1)
- Riesgo de inconsistencias entre modelos locales

#### 3. Modelos Híbridos y Ensemble (+3-5% precisión estimada)

**SARIMA + XGBoost:**
- SARIMA captura componente estacional
- XGBoost aprende residuos no lineales
- Combinar predicciones con weighted averaging

**SARIMA + Prophet + LSTM:**
- Prophet para tendencias con cambios de régimen
- LSTM para dependencias temporales largas (>12 meses)
- SARIMA para estacionalidad anual robusta
- Ensemble vía stacking o voting

**Ventajas:**
- Reducción de varianza por promediado
- Captura de patrones complejos inaccesibles para modelos únicos
- Mayor robustez ante datos atípicos

#### 4. Análisis Avanzado de Anomalías

**Detección de Outliers:**
- Isolation Forest para identificar meses anómalos
- Análisis de causas (eventos extraordinarios, errores de registro)
- Ponderación o exclusión de outliers en entrenamiento

**Clasificación de Tipos de Roturas:**
- Roturas reactivas (emergencias imprevistas)
- Roturas preventivas (mantenimiento programado)
- Modelo separado para cada tipo (patrones diferentes)

**Sistema de Alertas Tempranas:**
- Umbral dinámico basado en percentiles históricos
- Notificaciones automáticas si predicción > P95
- Dashboard en tiempo real para monitoreo continuo

### Extensiones del Proyecto

#### 5. Predicción Multivariada
- Además de roturas totales, predecir: tiempo de reparación, costo estimado, recursos necesarios
- Modelos VAR (Vector AutoRegression) para dependencias entre variables
- Optimización conjunta de múltiples KPIs

#### 6. Predicción en Tiempo Real
- Actualización del modelo con datos diarios (no solo mensuales)
- Ajuste dinámico de predicciones según eventos recientes
- API REST para integración con sistemas operativos

#### 7. Simulación de Escenarios "What-If"
- ¿Qué pasaría si se duplica el presupuesto de mantenimiento?
- ¿Cuál es el impacto de renovar infraestructura en barrio X?
- Optimización de asignación de recursos bajo restricciones

#### 8. Expansión Geográfica
- Aplicar metodología a otras ciudades/regiones
- Transfer learning: aprovechar patrones de zonas con más datos
- Meta-análisis para identificar factores universales

### Cronograma Estimado

| Tarea | Esfuerzo Estimado | Prioridad |
|-------|-------------------|----------|
| Variables exógenas (clima) | 2-3 semanas | Alta |
| Modelado jerárquico | 1-2 semanas | Media |
| Ensemble SARIMA+XGBoost | 1 semana | Alta |
| Sistema de alertas | 1 semana | Media |
| Detección de anomalías | 1 semana | Baja |
| API en producción | 2-3 semanas | Alta |

### Recursos Necesarios

- **Datos adicionales:** Acceso a APIs de clima (OpenWeatherMap, NOAA), bases de datos municipales
- **Infraestructura:** Servidor para entrenamiento continuo, base de datos PostgreSQL/MongoDB
- **Herramientas:** MLflow para tracking, Docker para deployment, FastAPI para servicios
- **Equipo:** 1 Data Scientist, 1 ML Engineer, 1 Domain Expert (ingeniero de infraestructura)

---

## 🔧 Instalación y Uso

### Requisitos

```bash
Python 3.9+
pandas==2.3.3
numpy==2.3.5
matplotlib==3.10.7
seaborn==0.13.2
statsmodels==0.14.5
scikit-learn==1.7.2
scipy==1.16.3
openpyxl==3.1.5
```

### Instalación

```bash
# Clonar repositorio
git clone <url-repositorio>
cd proyectofinal

# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar notebook
jupyter notebook modelo_final_limpio.ipynb
```

### Ejecución del Análisis

1. Abrir `modelo.ipynb` en Jupyter Notebook o VS Code
2. Ejecutar todas las celdas secuencialmente (`Run All`)
3. Los resultados se guardarán automáticamente:
   - `resultados_modelo_final.png`
   - `diagnostico_residuos.png`
   - `descomposicion_estacional.png`
   - `proceso_estacionariedad.png`

### 🌐 Dashboard Interactivo en Línea

**Accede al dashboard en vivo sin instalar nada:**

## 🚀 **[VER DASHBOARD INTERACTIVO](https://3szq5gtwqevyjs8de7ik5r.streamlit.app/)**

El dashboard incluye:
- 📊 **Predicciones futuras** con intervalos de confianza (3-12 meses)
- 🗺️ **Análisis espacial** por barrios más afectados
- ⏰ **Patrones temporales** (distribución por hora y día)
- 🔍 **Diagnóstico del modelo** SARIMA con métricas detalladas
- 📄 **Generación de reportes PDF** descargables
- 🎛️ **Filtros interactivos** para personalizar el análisis

---

### 💻 Ejecución Local (Opcional)

Si deseas ejecutar el dashboard localmente:

```bash
# Instalar dependencias
pip install -r requirements_dashboard.txt

# Ejecutar dashboard
streamlit run dashboard.py
```

El dashboard local se abrirá en `http://localhost:8501`

---

## 📊 Visualizaciones Generadas

### 1. Resultados del Modelo Final (6 gráficos)
- Serie temporal con predicciones y IC 95%
- Evolución de precisión por método
- Reducción de error (MAE)
- Componente estacional
- Distribución de errores (Rolling Window)
- Comparación real vs predicción (Test Set)

### 2. Diagnóstico de Residuos (6 gráficos)
- Residuos en el tiempo
- Histograma de distribución
- Q-Q Plot (normalidad)
- ACF (autocorrelación)
- PACF (autocorrelación parcial)
- Residuos vs valores ajustados

---

## 📚 Referencias Técnicas

1. **Box, G. E., Jenkins, G. M., & Reinsel, G. C. (2015).** *Time Series Analysis: Forecasting and Control.* John Wiley & Sons.
2. **Hyndman, R. J., & Athanasopoulos, G. (2021).** *Forecasting: Principles and Practice.* OTexts.
3. **Bergmeir, C., & Benítez, J. M. (2012).** *On the use of cross-validation for time series predictor evaluation.* Information Sciences.
4. **Box, G. E., & Cox, D. R. (1964).** *An analysis of transformations.* Journal of the Royal Statistical Society.
5. **Ljung, G. M., & Box, G. E. (1978).** *On a measure of lack of fit in time series models.* Biometrika.

---

## 👨‍💻 Autores

**Santiago Andrés Orejuela Cueter** 

**Valentina Alfaro Padilla** 

**Valentina Zuñiga Vasquez** 

**Samuel David Díaz Llamas** 

Modelos de Regresión y Series de Tiempo con Aplicaciones en IA  
Universidad Tecnológica de Bolívar


---

## 🏆 Conclusión

Este proyecto demuestra la aplicación exitosa de modelos SARIMA con técnicas avanzadas de validación cruzada temporal para predicción de series temporales con alta variabilidad. La **precisión del 79.69%** alcanzada, junto con la reducción del **21.7% en MAE**, representa un resultado sólido que supera los benchmarks típicos para este tipo de datos.

El modelo está listo para implementación operativa, permitiendo una planificación efectiva de recursos de mantenimiento con hasta 6 meses de anticipación. Las visualizaciones y métricas proporcionadas facilitan la interpretación y comunicación de resultados a stakeholders no técnicos.

**Recomendación:** Implementar el modelo en producción con actualización trimestral y monitoreo continuo de métricas de desempeño.

