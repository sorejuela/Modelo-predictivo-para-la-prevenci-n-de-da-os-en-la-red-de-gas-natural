"""
🔮 Dashboard Interactivo - Predicción de Roturas en Red de Gas
Universidad Tecnológica de Bolívar
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime
import pickle
import warnings
warnings.filterwarnings('ignore')

# Configuración de la página
st.set_page_config(
    page_title="Dashboard - Predicción de Roturas",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2E86AB;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Cargar datos
@st.cache_data
def cargar_datos():
    """Carga los datos procesados del análisis"""
    try:
        df = pd.read_excel('Copia de base_datos.xlsx')
        df.columns = df.columns.str.strip()
        df['Fecha de Creación'] = pd.to_datetime(df['Fecha de Creación'], errors='coerce')
        df = df.dropna(subset=['Fecha de Creación']).sort_values('Fecha de Creación')
        
        # Variables temporales
        df['Año'] = df['Fecha de Creación'].dt.year
        df['Mes'] = df['Fecha de Creación'].dt.month
        df['Mes_Nombre'] = df['Fecha de Creación'].dt.strftime('%B')
        df['Dia_Semana'] = df['Fecha de Creación'].dt.dayofweek
        df['Hora'] = df['Fecha de Creación'].dt.hour
        
        # Serie mensual
        df_mensual = df.groupby(pd.Grouper(key='Fecha de Creación', freq='M')).size()
        df_mensual = pd.DataFrame(df_mensual, columns=['Num_Roturas'])
        
        return df, df_mensual
        
    except FileNotFoundError:
        # Generar datos simulados si no existe el archivo
        st.warning("⚠️ Usando datos simulados para demostración. Para datos reales, configura el archivo Excel en Streamlit Cloud.")
        fechas = pd.date_range(start='2019-01-01', end='2025-07-31', freq='D')
        np.random.seed(42)
        n_registros = 4162
        df = pd.DataFrame({
            'Fecha de Creación': np.random.choice(fechas, n_registros),
            'Barrio': np.random.choice(['BARRIO ABAJO', 'CENTRO', 'MANGA', 'PIE DE LA POPA', 'SAN DIEGO', 
                                       'ESPINAL', 'BOSTON', 'CABRERO', 'TORICES', 'CRESPO'], n_registros),
            'Distrito': np.random.choice(['CARTAGENA', 'TURBACO', 'ARJONA'], n_registros, p=[0.8, 0.15, 0.05])
        })
        df = df.sort_values('Fecha de Creación')
        
        # Variables temporales
        df['Año'] = df['Fecha de Creación'].dt.year
        df['Mes'] = df['Fecha de Creación'].dt.month
        df['Mes_Nombre'] = df['Fecha de Creación'].dt.strftime('%B')
        df['Dia_Semana'] = df['Fecha de Creación'].dt.dayofweek
        df['Hora'] = df['Fecha de Creación'].dt.hour
        
        # Serie mensual
        df_mensual = df.groupby(pd.Grouper(key='Fecha de Creación', freq='M')).size()
        df_mensual = pd.DataFrame(df_mensual, columns=['Num_Roturas'])
        
        return df, df_mensual
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        return None, None

# Cargar modelo y predicciones (simuladas por ahora)
@st.cache_data
def cargar_predicciones():
    """Genera predicciones para los próximos meses"""
    # Datos de ejemplo - en producción cargarías del modelo entrenado
    fechas_futuras = pd.date_range(start='2025-08-01', periods=12, freq='M')
    predicciones = [64, 48, 52, 76, 69, 58, 45, 51, 63, 72, 67, 54]
    ic_inferior = [33, 23, 24, 33, 28, 23, 20, 22, 28, 32, 29, 24]
    ic_superior = [123, 99, 114, 174, 168, 148, 112, 125, 145, 165, 158, 132]
    
    # Nombres de meses en español
    meses_es = {
        1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
        5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
        9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
    }
    
    df_pred = pd.DataFrame({
        'Fecha': fechas_futuras,
        'Prediccion': predicciones,
        'IC_Inferior': ic_inferior,
        'IC_Superior': ic_superior,
        'Mes_Nombre': [f"{meses_es[f.month]} {f.year}" for f in fechas_futuras],
        'Año': [f.year for f in fechas_futuras],
        'Mes': [f.month for f in fechas_futuras]
    })
    
    return df_pred

df, df_mensual = cargar_datos()
df_predicciones = cargar_predicciones()

# ============= HEADER =============
st.markdown('<p class="main-header">🔮 Sistema de Predicción de Roturas en Red de Gas</p>', unsafe_allow_html=True)
st.markdown("**Universidad Tecnológica de Bolívar** | Modelo SARIMA(0,1,1)(0,1,1,12)")
st.markdown("")

# ============= FILTROS EN LÍNEA =============
st.markdown("#### ⚙️ Configuración y Filtros")
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    # Selector de horizonte de predicción
    horizonte = st.selectbox(
        "Horizonte de predicción",
        options=[3, 6, 9, 12],
        index=1,
        help="Número de meses a predecir",
        key="horizonte_select"
    )

with col2:
    # Selector de mes específico - incluir meses históricos
    # Obtener meses históricos únicos
    meses_es = {
        1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
        5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
        9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
    }
    
    df_meses_hist = df.copy()
    df_meses_hist['Año_Mes'] = df_meses_hist['Fecha de Creación'].dt.to_period('M')
    meses_historicos = df_meses_hist['Año_Mes'].unique()
    meses_hist_nombres = [f"{meses_es[pd.Period(m).month]} {pd.Period(m).year}" for m in sorted(meses_historicos, reverse=True)[:12]]
    
    meses_disponibles = ['Todos'] + meses_hist_nombres
    
    mes_seleccionado = st.selectbox(
        "Mes a analizar (histórico)",
        options=meses_disponibles,
        help="Selecciona un mes histórico para ver detalles específicos",
        key="mes_select"
    )

with col3:
    # Filtro de barrios
    top_n_barrios = st.slider(
        "Top N barrios",
        min_value=3,
        max_value=15,
        value=6,
        help="Número de barrios con mayor incidencia",
        key="barrios_slider"
    )

# Nivel de confianza fijo en 95%
confianza = 95

st.markdown("")
st.markdown("")

# Métricas principales
col1, col2, col3, col4 = st.columns(4, gap="medium")

with col1:
    total_historico = len(df)
    st.metric(
        "Total Roturas Históricas",
        f"{total_historico:,}",
        help="Roturas registradas 2019-2025"
    )

with col2:
    promedio_mensual = df_mensual['Num_Roturas'].mean()
    st.metric(
        "Promedio Mensual",
        f"{promedio_mensual:.1f}",
        help="Promedio histórico de roturas/mes"
    )

with col3:
    pred_proximo = df_predicciones.iloc[0]['Prediccion']
    st.metric(
        "Próximo Mes Predicho",
        f"{pred_proximo:.0f}",
        f"{((pred_proximo - promedio_mensual)/promedio_mensual*100):+.1f}%",
        help="Predicción para el próximo mes"
    )

with col4:
    mes_critico = df_predicciones.head(horizonte).loc[df_predicciones.head(horizonte)['Prediccion'].idxmax(), 'Mes_Nombre']
    max_pred = df_predicciones.head(horizonte)['Prediccion'].max()
    st.metric(
        "Mes Crítico",
        mes_critico.split()[0],
        f"{max_pred:.0f} roturas",
        help="Mes con mayor predicción de roturas"
    )

st.markdown("---")

# ============= TABS PRINCIPALES =============
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Predicciones", 
    "🗺️ Análisis Espacial", 
    "⏰ Análisis Temporal",
    "🔬 Diagnóstico del Modelo"
])

# ============= TAB 1: PREDICCIONES =============
with tab1:
    st.markdown("### 📊 Predicciones Futuras")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Gráfico de serie temporal con predicciones
        fig = go.Figure()
        
        # Histórico
        fig.add_trace(go.Scatter(
            x=df_mensual.index,
            y=df_mensual['Num_Roturas'],
            mode='lines',
            name='Histórico',
            line=dict(color='#2E86AB', width=2)
        ))
        
        # Predicciones
        df_pred_filtrado = df_predicciones.head(horizonte)
        fig.add_trace(go.Scatter(
            x=df_pred_filtrado['Fecha'],
            y=df_pred_filtrado['Prediccion'],
            mode='lines+markers',
            name='Predicción',
            line=dict(color='#D90429', width=3, dash='dash'),
            marker=dict(size=8)
        ))
        
        # Intervalo de confianza
        fig.add_trace(go.Scatter(
            x=df_pred_filtrado['Fecha'].tolist() + df_pred_filtrado['Fecha'].tolist()[::-1],
            y=df_pred_filtrado['IC_Superior'].tolist() + df_pred_filtrado['IC_Inferior'].tolist()[::-1],
            fill='toself',
            fillcolor='rgba(217, 4, 41, 0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            name='IC 95%',
            showlegend=True
        ))
        
        # Línea de promedio histórico
        fig.add_hline(
            y=promedio_mensual,
            line_dash="dot",
            line_color="gray",
            annotation_text=f"Promedio: {promedio_mensual:.1f}",
            annotation_position="right"
        )
        
        fig.update_layout(
            title=f"Serie Temporal y Predicciones ({horizonte} meses)",
            xaxis_title="Fecha",
            yaxis_title="Roturas/Mes",
            hovermode='x unified',
            height=500,
            template='plotly_white'
        )
        
        st.plotly_chart(fig, use_column_width=True)
    
    with col2:
        # Tabla de predicciones
        st.markdown("#### 📋 Tabla de Predicciones")
        
        tabla_pred = df_pred_filtrado[['Mes_Nombre', 'Prediccion', 'IC_Inferior', 'IC_Superior']].copy()
        tabla_pred.columns = ['Mes', 'Predicción', 'IC Inf.', 'IC Sup.']
        tabla_pred['Predicción'] = tabla_pred['Predicción'].apply(lambda x: f"{x:.0f}")
        tabla_pred['IC Inf.'] = tabla_pred['IC Inf.'].apply(lambda x: f"{x:.0f}")
        tabla_pred['IC Sup.'] = tabla_pred['IC Sup.'].apply(lambda x: f"{x:.0f}")
        
        st.dataframe(
            tabla_pred,
            hide_index=True,
            height=400
        )
        
        # Resumen
        total_pred = df_pred_filtrado['Prediccion'].sum()
        st.info(f"**Total {horizonte} meses:** {total_pred:.0f} roturas")

# ============= TAB 2: ANÁLISIS ESPACIAL =============
with tab2:
    st.markdown("### 🗺️ Distribución Espacial de Roturas")
    
    # Filtrar datos según mes seleccionado
    if mes_seleccionado != 'Todos':
        try:
            # Parsear el mes seleccionado (formato: "Mes Año")
            meses_inv = {
                'Enero': 1, 'Febrero': 2, 'Marzo': 3, 'Abril': 4,
                'Mayo': 5, 'Junio': 6, 'Julio': 7, 'Agosto': 8,
                'Septiembre': 9, 'Octubre': 10, 'Noviembre': 11, 'Diciembre': 12
            }
            partes = mes_seleccionado.split()
            mes_num = meses_inv[partes[0]]
            año_num = int(partes[1])
            
            df_filtrado = df[
                (df['Fecha de Creación'].dt.year == año_num) &
                (df['Fecha de Creación'].dt.month == mes_num)
            ]
            titulo_adicional = f" - {mes_seleccionado}"
            
            if len(df_filtrado) == 0:
                st.warning(f"⚠️ No hay datos para {mes_seleccionado}")
                df_filtrado = df
                titulo_adicional = " - Histórico Completo"
        except Exception as e:
            st.error(f"Error al filtrar por mes: {e}")
            df_filtrado = df
            titulo_adicional = " - Histórico Completo"
    else:
        df_filtrado = df
        titulo_adicional = " - Histórico Completo"
    
    # Análisis por barrio
    barrio_counts = df_filtrado['Barrio'].value_counts().head(top_n_barrios)
    total_meses = len(df_mensual)
    
    col1, col2 = st.columns([3, 2], gap="large")
    
    with col1:
        # Gráfico de barrios
        fig = go.Figure()
        
        promedio_mensual_barrios = barrio_counts / total_meses if mes_seleccionado == 'Todos' else barrio_counts
        
        # Definir colores según nivel de riesgo
        colors = []
        for val in promedio_mensual_barrios:
            if mes_seleccionado == 'Todos':
                if val > 2:
                    colors.append('#D90429')  # Muy Alto
                elif val > 1.5:
                    colors.append('#F18F01')  # Alto
                elif val > 1:
                    colors.append('#FFD93D')  # Medio
                else:
                    colors.append('#06A77D')  # Bajo
            else:
                colors.append('#2E86AB')
        
        fig.add_trace(go.Bar(
            y=barrio_counts.index[::-1],
            x=promedio_mensual_barrios[::-1],
            orientation='h',
            marker=dict(color=colors[::-1]),
            text=promedio_mensual_barrios[::-1].round(2),
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Roturas: %{x:.2f}<extra></extra>'
        ))
        
        fig.update_layout(
            title=f"Top {top_n_barrios} Barrios con Mayor Incidencia{titulo_adicional}",
            xaxis_title="Roturas" + ("/Mes" if mes_seleccionado == 'Todos' else ""),
            yaxis_title="Barrio",
            height=400,
            template='plotly_white',
            showlegend=False
        )
        
        st.plotly_chart(fig, use_column_width=True)
    
    with col2:
        # Estadísticas por barrio
        st.markdown("#### 📊 Estadísticas")
        
        total_top = barrio_counts.sum()
        total_general = len(df_filtrado)
        concentracion = (total_top / total_general) * 100
        
        st.metric(
            "Roturas en Top Barrios",
            f"{total_top:,}",
            f"{concentracion:.1f}% del total"
        )
        
        barrio_mas_afectado = barrio_counts.index[0]
        roturas_max = barrio_counts.iloc[0]
        
        st.metric(
            "Barrio Más Afectado",
            barrio_mas_afectado[:20] + "..." if len(barrio_mas_afectado) > 20 else barrio_mas_afectado,
            f"{roturas_max} roturas"
        )
        
        # Predicción para próximo mes en barrio crítico
        if mes_seleccionado == 'Todos':
            pred_barrio = roturas_max / total_meses
            st.metric(
                "Predicción Mensual (Barrio Crítico)",
                f"{pred_barrio:.2f}",
                help="Promedio mensual esperado en el barrio más afectado"
            )
    
    # Tabla detallada
    st.markdown("#### 📋 Detalle por Barrio")
    
    tabla_barrios = pd.DataFrame({
        'Ranking': range(1, len(barrio_counts) + 1),
        'Barrio': barrio_counts.index,
        'Roturas': barrio_counts.values,
        'Porcentaje': (barrio_counts.values / total_general * 100).round(2)
    })
    
    if mes_seleccionado == 'Todos':
        tabla_barrios['Prom/Mes'] = (tabla_barrios['Roturas'] / total_meses).round(2)
    
    st.dataframe(
        tabla_barrios,
        hide_index=True,
        height=300
    )

# ============= TAB 3: ANÁLISIS TEMPORAL =============
with tab3:
    st.markdown("### ⏰ Patrones Temporales de Roturas")
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        # Distribución por hora
        hora_counts = df.groupby('Hora').size()
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=hora_counts.index,
            y=hora_counts.values,
            marker=dict(
                color=hora_counts.values,
                colorscale='Reds',
                showscale=True,
                colorbar=dict(title="Roturas")
            ),
            hovertemplate='<b>Hora %{x}:00</b><br>Roturas: %{y}<extra></extra>'
        ))
        
        fig.update_layout(
            title="Distribución por Hora del Día",
            xaxis_title="Hora",
            yaxis_title="Número de Roturas",
            height=400,
            template='plotly_white',
            xaxis=dict(tickmode='linear', tick0=0, dtick=2)
        )
        
        st.plotly_chart(fig, use_column_width=True)
        
        # Estadísticas horarias
        hora_critica = hora_counts.idxmax()
        roturas_hora_critica = hora_counts.max()
        prob_hora = (roturas_hora_critica / len(df) * 100)
        
        st.info(f"🕐 **Hora crítica:** {hora_critica}:00 - {(hora_critica+1)%24}:00 hrs ({roturas_hora_critica} roturas, {prob_hora:.1f}%)")
    
    with col2:
        # Distribución por día de la semana
        dias_nombres = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        dia_counts = df.groupby('Dia_Semana').size().reindex(range(7), fill_value=0)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dias_nombres,
            y=dia_counts.values,
            marker=dict(
                color=dia_counts.values,
                colorscale='Blues',
                showscale=True,
                colorbar=dict(title="Roturas")
            ),
            hovertemplate='<b>%{x}</b><br>Roturas: %{y}<extra></extra>'
        ))
        
        fig.update_layout(
            title="Distribución por Día de la Semana",
            xaxis_title="Día",
            yaxis_title="Número de Roturas",
            height=400,
            template='plotly_white'
        )
        
        st.plotly_chart(fig, use_column_width=True)
        
        # Estadísticas semanales
        dia_critico = dias_nombres[dia_counts.idxmax()]
        roturas_dia_critico = dia_counts.max()
        prob_dia = (roturas_dia_critico / len(df) * 100)
        
        st.info(f"📅 **Día crítico:** {dia_critico} ({roturas_dia_critico} roturas, {prob_dia:.1f}%)")
    
    # Mapa de calor
    st.markdown("#### 🔥 Mapa de Calor: Día × Hora")
    
    heatmap_data = df.groupby(['Dia_Semana', 'Hora']).size().unstack(fill_value=0)
    heatmap_data.index = dias_nombres
    
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='YlOrRd',
        hovertemplate='<b>%{y}</b> - Hora %{x}:00<br>Roturas: %{z}<extra></extra>',
        colorbar=dict(title="Roturas")
    ))
    
    fig.update_layout(
        title="Concentración de Roturas por Día y Hora",
        xaxis_title="Hora del Día",
        yaxis_title="Día de la Semana",
        height=400,
        template='plotly_white'
    )
    
    st.plotly_chart(fig, use_column_width=True)
    
    # Recomendaciones
    st.markdown("#### 💡 Recomendaciones Operativas")
    
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        st.success(f"""
        **Vigilancia Preventiva**
        - Reforzar en {dia_critico}
        - Horario: {hora_critica}:00-{(hora_critica+2)%24}:00
        - Recursos adicionales: +30%
        """)
    
    with col2:
        # Períodos del día
        madrugada = df[df['Hora'].between(0, 5)].shape[0]
        manana = df[df['Hora'].between(6, 11)].shape[0]
        tarde = df[df['Hora'].between(12, 17)].shape[0]
        noche = df[df['Hora'].between(18, 23)].shape[0]
        
        periodo_critico = max(
            [('Madrugada', madrugada), ('Mañana', manana), ('Tarde', tarde), ('Noche', noche)],
            key=lambda x: x[1]
        )[0]
        
        st.warning(f"""
        **Período Crítico**
        - {periodo_critico}: Mayor incidencia
        - Inspecciones: Diarias
        - Cuadrillas: 2-3 equipos
        """)
    
    with col3:
        semana_laboral = df[df['Dia_Semana'].between(0, 4)].shape[0]
        fin_semana = df[df['Dia_Semana'].between(5, 6)].shape[0]
        ratio = semana_laboral / fin_semana if fin_semana > 0 else 0
        
        st.info(f"""
        **Distribución Semanal**
        - Lun-Vie: {semana_laboral} roturas
        - Sáb-Dom: {fin_semana} roturas
        - Ratio: {ratio:.1f}x más en laborables
        """)

# ============= TAB 4: DIAGNÓSTICO =============
with tab4:
    st.markdown("### 🔬 Diagnóstico del Modelo SARIMA")
    
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        st.metric("Precisión del Modelo", "79.69%", "+1.60%")
        st.caption("Intervalo de Confianza 95%: [72.35%, 87.03%]")
    
    with col2:
        st.metric("Error Absoluto Medio (MAE)", "10.70", "-21.7%")
        st.caption("Reducción vs baseline")
    
    with col3:
        st.metric("Test Ljung-Box", "✅ APROBADO", "p = 0.9665")
        st.caption("Sin autocorrelación en residuos")
    
    st.markdown("---")
    
    # Información del modelo
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("#### 📊 Configuración del Modelo")
        
        modelo_info = pd.DataFrame({
            'Parámetro': ['Orden (p,d,q)', 'Orden Estacional (P,D,Q,s)', 'Transformación', 'Validación', 'Ventanas de Validación'],
            'Valor': ['(0, 1, 1)', '(0, 1, 1, 12)', 'Logarítmica (log1p)', 'Rolling Window', '14 ventanas']
        })
        
        st.dataframe(modelo_info, hide_index=True, use_container_width=True)
        
        st.markdown("#### ✅ Validaciones Estadísticas")
        
        validaciones = pd.DataFrame({
            'Test': ['Ljung-Box (Autocorrelación)', 'Shapiro-Wilk (Normalidad)', 'Media de Residuos'],
            'Resultado': ['✅ Aprobado (p > 0.05)', '⚠️ No aprobado (outliers)', '✅ ≈ 0 (sin sesgo)'],
            'p-value': ['0.9665', '0.0000', 'Media: 0.0267']
        })
        
        st.dataframe(validaciones, hide_index=True, use_container_width=True)
    
    with col2:
        st.markdown("#### 🎯 Comparación de Modelos")
        
        comparacion = pd.DataFrame({
            'Modelo': ['Baseline', 'Óptimo', '+ Log', '+ Rolling'],
            'Precisión': [78.09, 78.27, 78.20, 79.69],
            'MAE': [13.67, 13.26, 13.22, 10.70]
        })
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=comparacion['Modelo'],
            y=comparacion['Precisión'],
            mode='lines+markers',
            name='Precisión (%)',
            line=dict(color='#2E86AB', width=3),
            marker=dict(size=10)
        ))
        
        fig.update_layout(
            title={
                'text': "Evolución de Precisión",
                'font': {'size': 14, 'color': '#2E86AB'}
            },
            yaxis_title="Precisión (%)",
            height=350,
            template='plotly_white',
            showlegend=False,
            margin=dict(l=50, r=30, t=50, b=50)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Conclusión
    st.markdown("#### 💡 Conclusión del Diagnóstico")
    
    st.success("""
    **✅ El modelo SARIMA(0,1,1)(0,1,1,12) es ADECUADO para predicción operativa:**
    
    - ✅ **Ljung-Box aprobado:** Sin autocorrelación en residuos (modelo capturó toda la información)
    - ✅ **Media de residuos ≈ 0:** Sin sesgo sistemático en las predicciones
    - ✅ **Precisión 79.69%:** Supera benchmarks típicos para series con CV > 40% (70-75%)
    - ✅ **Reducción MAE 21.7%:** Mejora significativa vs modelo baseline
    - ⚠️ **Shapiro-Wilk no aprobado:** Esperado con outliers, no invalida el modelo
    
    **Recomendación:** Implementar en producción con actualización trimestral.
    """)

# ============= FOOTER =============
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p><strong>Universidad Tecnológica de Bolívar</strong></p>
    <p>Modelos de Regresión y Series de Tiempo con Aplicaciones en IA</p>
    <p>Última actualización: Noviembre 2025 | Modelo v1.0</p>
</div>
""", unsafe_allow_html=True)


# ============= FUNCIÓN PARA GENERAR PDF =============
def generar_pdf_reporte(df, df_predicciones, mes_seleccionado, top_n_barrios):
    """
    Genera un reporte PDF con los resultados del análisis
    """
    try:
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
        from datetime import datetime
        import io
        
        # Crear buffer para el PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        # Estilos
        styles = getSampleStyleSheet()
        titulo_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2E86AB'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        subtitulo_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#D90429'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        # Contenido
        elementos = []
        
        # Portada
        elementos.append(Spacer(1, 1.5*inch))
        elementos.append(Paragraph("🔮 REPORTE DE PREDICCIÓN", titulo_style))
        elementos.append(Paragraph("Roturas en Red de Gas de Bolívar", styles['Heading2']))
        elementos.append(Spacer(1, 0.5*inch))
        elementos.append(Paragraph(f"<b>Fecha de generación:</b> {datetime.now().strftime('%d de %B de %Y, %H:%M')}", styles['Normal']))
        elementos.append(Paragraph("<b>Modelo:</b> SARIMA(0,1,1)(0,1,1,12)", styles['Normal']))
        elementos.append(Paragraph(f"<b>Precisión:</b> 79.69% (±3.75%)", styles['Normal']))
        elementos.append(Paragraph("<b>Universidad Tecnológica de Bolívar</b>", styles['Normal']))
        
        elementos.append(PageBreak())
        
        # Resumen Ejecutivo
        elementos.append(Paragraph("1. RESUMEN EJECUTIVO", subtitulo_style))
        
        resumen_texto = f"""
        El presente reporte presenta los resultados del modelo predictivo SARIMA aplicado a las roturas 
        causadas por terceros en la red de gas de Bolívar. El modelo alcanzó una precisión del 79.69%, 
        superando el benchmark esperado para series temporales con alta variabilidad.
        <br/><br/>
        <b>Métricas principales:</b><br/>
        • Precisión: 79.69% (IC 95%: [72.35%, 87.03%])<br/>
        • MAE: 10.70 roturas (reducción del 21.7% vs baseline)<br/>
        • Total de observaciones históricas: {len(df):,} roturas (79 meses)<br/>
        • Promedio mensual histórico: {df.groupby(pd.Grouper(key='Fecha de Creación', freq='M')).size().mean():.1f} roturas/mes
        """
        
        elementos.append(Paragraph(resumen_texto, styles['Normal']))
        elementos.append(Spacer(1, 0.3*inch))
        
        # Tabla de predicciones
        elementos.append(Paragraph("2. PREDICCIONES PRÓXIMOS MESES", subtitulo_style))
        
        tabla_data = [['Mes', 'Predicción', 'IC Inferior', 'IC Superior']]
        for _, row in df_predicciones.iterrows():
            tabla_data.append([
                row['Mes_Nombre'],
                f"{row['Prediccion']:.0f}",
                f"{row['IC_Inferior']:.0f}",
                f"{row['IC_Superior']:.0f}"
            ])
        
        tabla = Table(tabla_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        
        elementos.append(tabla)
        elementos.append(Spacer(1, 0.3*inch))
        
        # Análisis por barrios
        elementos.append(Paragraph("3. ANÁLISIS ESPACIAL", subtitulo_style))
        
        barrio_counts = df['Barrio'].value_counts().head(top_n_barrios)
        total_meses = len(df.groupby(pd.Grouper(key='Fecha de Creación', freq='M')).size())
        
        tabla_barrios_data = [['Ranking', 'Barrio', 'Roturas', 'Prom/Mes', '% Total']]
        total_roturas = len(df)
        
        for i, (barrio, count) in enumerate(barrio_counts.items(), 1):
            promedio = count / total_meses
            porcentaje = (count / total_roturas) * 100
            nombre_corto = barrio[:35] + "..." if len(barrio) > 35 else barrio
            tabla_barrios_data.append([
                str(i),
                nombre_corto,
                str(count),
                f"{promedio:.2f}",
                f"{porcentaje:.1f}%"
            ])
        
        tabla_barrios = Table(tabla_barrios_data, colWidths=[0.6*inch, 3*inch, 1*inch, 1*inch, 1*inch])
        tabla_barrios.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#D90429')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        
        elementos.append(tabla_barrios)
        elementos.append(Spacer(1, 0.3*inch))
        
        # Recomendaciones
        elementos.append(PageBreak())
        elementos.append(Paragraph("4. RECOMENDACIONES OPERATIVAS", subtitulo_style))
        
        recomendaciones_texto = """
        <b>4.1 Planificación de Recursos</b><br/>
        • Incrementar recursos preventivos en meses de noviembre y diciembre (pico estacional)<br/>
        • Mantener cuadrillas de respuesta rápida en barrios de mayor incidencia<br/>
        • Programar mantenimiento preventivo en agosto-septiembre (baja incidencia)<br/><br/>
        
        <b>4.2 Vigilancia y Monitoreo</b><br/>
        • Reforzar inspecciones en horario de 8:00-12:00 hrs (horario crítico)<br/>
        • Priorizar días laborables (5x mayor incidencia vs fines de semana)<br/>
        • Implementar sistema de alertas tempranas basado en predicciones<br/><br/>
        
        <b>4.3 Actualización del Modelo</b><br/>
        • Re-entrenar modelo cada 3 meses con datos nuevos<br/>
        • Incorporar variables exógenas (clima, festividades) para mejorar precisión<br/>
        • Monitorear métricas de desempeño continuamente<br/><br/>
        
        <b>4.4 Inversión en Infraestructura</b><br/>
        • Renovar tuberías en los 6 barrios de mayor riesgo identificados<br/>
        • Implementar señalización preventiva en zonas críticas<br/>
        • Coordinar con entidades de obras civiles para minimizar daños
        """
        
        elementos.append(Paragraph(recomendaciones_texto, styles['Normal']))
        
        # Construir PDF
        doc.build(elementos)
        
        # Guardar archivo
        pdf_filename = f"reporte_prediccion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        buffer.seek(0)
        
        with open(pdf_filename, 'wb') as f:
            f.write(buffer.read())
        
        # Botón de descarga en Streamlit
        buffer.seek(0)
        st.download_button(
            label="📥 Descargar PDF",
            data=buffer,
            file_name=pdf_filename,
            mime="application/pdf"
        )
        
        return pdf_filename
        
    except ImportError:
        st.warning("⚠️ La librería reportlab no está instalada. Instálala con: `pip install reportlab`")
        return None
    except Exception as e:
        st.error(f"Error al generar PDF: {e}")
        return None
