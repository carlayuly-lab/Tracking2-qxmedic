import streamlit as st
import pandas as pd

# 1. Configuración de página (OBLIGATORIO ser la primera línea)
st.set_page_config(page_title="Consulta Qx Medic", layout="centered")

# 2. CSS de compatibilidad total para Jotform
st.markdown("""
    <style>
    /* Ocultar elementos de la interfaz de Streamlit */
    header, footer, .stAppDeployButton, [data-testid="stToolbar"] {
        display: none !important;
        visibility: hidden !important;
    }
    /* Eliminar espacios en blanco superiores */
    .block-container {
        padding-top: 0rem !important;
    }
    /* Estilo de la tarjeta de resultados */
    .main-card {
        background-color: white; 
        padding: 20px; 
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1); 
        border-top: 5px solid #1E40AF;
        color: #1E293B;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Función de carga de datos
@st.cache_data(ttl=60)
def load_data():
    try:
        url = "https://docs.google.com/spreadsheets/d/1tkKTopAlCGS_Ba7DaCkWFOHiwr_1uiU_Bima_cM5qcY/export?format=csv&gid=1777353802"
        df = pd.read_csv(url, dtype=str)
        df.columns = [str(c).strip().upper() for c in df.columns]
        return df
    except:
        return None

df = load_data()

if df is not None:
    # Buscador
    dni = st.text_input("🔍 Ingresa tu DNI:", placeholder="Ej: 72190439").strip()

    if dni:
        res_df = df[df['DNI'].astype(str) == str(dni)]
        if not res_df.empty:
            res = res_df.iloc[0]
            st.balloons()
            
            # Mostrar tarjeta en HTML
            st.markdown(f"""
            <div class="main-card">
                <h3 style="margin:0;">{res.get('NOMBRES', 'Estudiante')}</h3>
                <p style="color: green; font-weight: bold;">ENTREGADO</p>
                <hr>
                <p><b>Tracking:</b> {res.get('TRACKING', '-')}</p>
                <p><b>Curso:</b> {res.get('CURSO', '-')}</p>
                <p><b>Ubicación:</b> {res.get('DISTRITO', '')}, {res.get('PROVINCIA', '')}</p>
                <br>
                <a href="https://tracking.olvaexpress.pe" target="_blank" 
                   style="background:#2563EB; color:white; padding:10px; border-radius:8px; text-decoration:none;">
                   🚚 Ver en Olva Courier</a>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("DNI no encontrado.")