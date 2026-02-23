import streamlit as st
import pandas as pd

# 1. Configuración básica
st.set_page_config(page_title="Consulta", layout="centered")

# 2. CSS de compatibilidad total para Iframes
st.markdown("""
    <style>
    /* Ocultar elementos de Streamlit */
    header, footer, .stAppDeployButton, [data-testid="stToolbar"] {
        display: none !important;
    }
    
    /* Evitar que la app se esconda si el Iframe es pequeño */
    .block-container {
        padding-top: 10px !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    /* Estilo de la tarjeta de resultados */
    .main-card {
        background-color: white; 
        padding: 20px; 
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1); 
        border-top: 5px solid #1E40AF;
        color: #1E293B;
        margin-top: 15px;
    }

    .info-label { color: #64748B; font-size: 0.7rem; font-weight:bold; text-transform: uppercase; margin:0; }
    .info-value { font-size: 0.9rem; color: #1E293B; font-weight: 500; margin-bottom: 8px; }
    .pill { padding: 4px 10px; border-radius: 50px; font-weight: bold; font-size: 0.7rem; }
    
    .olva-btn {
        display: inline-block;
        margin-top: 10px;
        padding: 8px 16px;
        background-color: #2563EB;
        color: white !important;
        text-decoration: none !important;
        border-radius: 8px;
        font-weight: bold;
        font-size: 0.85rem;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Función de carga
@st.cache_data(ttl=60) # Tiempo de caché reducido para ver cambios rápido
def load_data():
    try:
        sheet_id = "1tkKTopAlCGS_Ba7DaCkWFOHiwr_1uiU_Bima_cM5qcY"
        gid = "1777353802"
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
        return pd.read_csv(url, dtype=str)
    except:
        return None

df = load_data()

if df is not None:
    df.columns = [str(c).strip().upper() for c in df.columns]
    
    dni = st.text_input("🔍 DNI:", placeholder="Ingresa tu número aquí").strip()

    if dni:
        res_df = df[df['DNI'].astype(str) == str(dni)]

        if not res_df.empty:
            res = res_df.iloc[0]
            
            # Variables de datos
            nombre = res.get('NOMBRES', '-')
            tracking = res.get('TRACKING', '-')
            estado = str(res.get('ESTADO', 'PROCESANDO')).upper()
            curso = res.get('CURSO', '-')
            ubi = f"{res.get('DISTRITO', '')}, {res.get('PROVINCIA', '')}"
            
            color_bg = "#DCFCE7" if "ENTREGADO" in estado else "#FEF9C3"
            color_tx = "#16A34A" if "ENTREGADO" in estado else "#854D0E"

            st.markdown(f"""
            <div class="main-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h3 style="margin:0; font-size: 1.1rem;">{nombre}</h3>
                    <span class="pill" style="background-color: {color_bg}; color: {color_tx};">{estado}</span>
                </div>
                <hr style="margin: 15px 0; border: 0; border-top: 1px solid #EEE;">
                <p class="info-label">TRACKING</p>
                <p class="info-value" style="color: #2563EB; font-size: 1.1rem;">{tracking}</p>
                <p class="info-label">CURSO</p>
                <p class="info-value">{curso}</p>
                <p class="info-label">UBICACIÓN</p>
                <p class="info-value">📍 {ubi}</p>
                <a href="https://tracking.olvaexpress.pe" target="_blank" class="olva-btn">🚚 Olva Courier</a>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("DNI no encontrado.")