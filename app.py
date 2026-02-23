import streamlit as st
import pandas as pd

# 1. Configuración de página (Debe ser la primera línea)
st.set_page_config(page_title="Consulta", layout="centered")

# 2. CSS de Limpieza Absoluta para evitar bloqueos visuales
st.markdown("""
    <style>
    /* Ocultar todo lo que no sea el contenido */
    header, footer, .stAppDeployButton, [data-testid="stToolbar"] {
        display: none !important;
    }
    .block-container {
        padding-top: 10px !important;
    }
    /* Diseño de la tarjeta */
    .resultado-card {
        background-color: white; 
        padding: 20px; 
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1); 
        border-top: 5px solid #1E40AF;
        color: #1E293B;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Carga de datos simplificada
@st.cache_data(ttl=60)
def get_data():
    try:
        # Tu Sheet ID y GID de siempre
        url = "https://docs.google.com/spreadsheets/d/1tkKTopAlCGS_Ba7DaCkWFOHiwr_1uiU_Bima_cM5qcY/export?format=csv&gid=1777353802"
        return pd.read_csv(url, dtype=str)
    except Exception as e:
        st.error("Error técnico de conexión.")
        return None

df = get_data()

if df is not None:
    # Normalizar columnas
    df.columns = [str(c).strip().upper() for c in df.columns]
    
    # Buscador sencillo
    dni = st.text_input("🔍 Ingresa DNI:").strip()

    if dni:
        res = df[df['DNI'].astype(str) == str(dni)]

        if not res.empty:
            fila = res.iloc[0]
            st.balloons()
            
            # Mostrar resultado en HTML limpio
            st.markdown(f"""
            <div class="resultado-card">
                <h3 style="margin:0;">{fila.get('NOMBRES', 'Usuario')}</h3>
                <hr>
                <p><b>Estado:</b> {fila.get('ESTADO', '-')}</p>
                <p><b>Tracking:</b> <span style="color:blue;">{fila.get('TRACKING', '-')}</span></p>
                <p><b>Curso:</b> {fila.get('CURSO', '-')}</p>
                <br>
                <a href="https://tracking.olvaexpress.pe" target="_blank" 
                   style="background:#2563EB; color:white; padding:10px; border-radius:5px; text-decoration:none;">
                   🚚 Rastrear en Olva
                </a>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("DNI no registrado.")