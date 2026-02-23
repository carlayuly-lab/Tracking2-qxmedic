import streamlit as st
import pandas as pd

# 1. Configuración de página - Modo ancho para ocupar todo el celular
st.set_page_config(
    page_title="Tracking Qx Medic", 
    page_icon="📦", 
    layout="wide" 
)

# 2. CSS Maestro para eliminar bordes, marcas de agua y ajustar el ancho
st.markdown("""
    <style>
    /* ELIMINAR ELEMENTOS DE STREAMLIT (Built with Streamlit, Fullscreen, etc) */
    header, footer, .stAppDeployButton, [data-testid="stToolbar"] {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* ELIMINAR BOTÓN DE FULLSCREEN (Pantalla completa en imágenes/tarjetas) */
    button[title="View fullscreen"] {
        display: none !important;
    }

    /* FORZAR ANCHO TOTAL Y ELIMINAR MÁRGENES LATERALES EN MÓVILES */
    .block-container {
        max-width: 100% !important;
        padding-top: 1rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
        padding-bottom: 0rem !important;
    }

    /* AJUSTE DE LA TARJETA PARA CELULARES */
    .main-card {
        background-color: white; 
        padding: 20px; 
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1); 
        border-top: 8px solid #1E40AF;
        color: #1E293B;
        width: 100% !important;
        margin: auto;
    }

    /* Banner adaptable */
    .header-banner {
        background: linear-gradient(135deg, #1E40AF 0%, #1D4ED8 100%);
        padding: 25px 10px; border-radius: 15px; color: white; text-align: center;
        margin-bottom: 20px; width: 100%;
    }
    
    .logo-img {
        max-width: 150px;
        filter: drop-shadow(0px 4px 6px rgba(0,0,0,0.1));
    }

    /* Estilos de texto y etiquetas */
    .info-label { color: #64748B; font-size: 0.7rem; font-weight:bold; text-transform: uppercase; }
    .info-value { font-size: 0.9rem; margin-bottom: 8px; color: #1E293B; font-weight: 500; }
    .pill { padding: 4px 10px; border-radius: 50px; font-weight: bold; font-size: 0.7rem; }
    
    .olva-btn {
        display: inline-block; margin-top: 15px; padding: 10px 20px;
        background-color: #2563EB; color: white !important;
        text-decoration: none !important; border-radius: 10px; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Carga de datos
@st.cache_data(ttl=300)
def load_data():
    try:
        sheet_id = "1tkKTopAlCGS_Ba7DaCkWFOHiwr_1uiU_Bima_cM5qcY"
        gid = "1777353802"
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
        df = pd.read_csv(url, dtype=str)
        df.columns = [str(c).strip().upper() for c in df.columns]
        return df
    except Exception as e:
        return None

# --- UI ---
logo_url = "https://www.dropbox.com/scl/fi/65bmjdwdeb8ya3gb4wsw5/logo-qx4.png?rlkey=wlp7kp10dhuvltr3yav3vmw6w&raw=1"

st.markdown(f'''
    <div class="header-banner">
        <img src="{logo_url}" class="logo-img">
        <p style="margin:0; opacity: 0.9; font-size: 0.9rem; font-weight: 300;">SISTEMA DE SEGUIMIENTO 2026</p>
    </div>
''', unsafe_allow_html=True)

data = load_data()

if data is not None:
    dni_input = st.text_input("🔍 Ingresa tu DNI:", placeholder="Ej. 70254718").strip()

    if dni_input:
        resultado = data[data['DNI'].astype(str) == str(dni_input)]
        if not resultado.empty:
            res = resultado.iloc[0]
            st.balloons()
            
            nombre = res.get('NOMBRES', '-')
            tracking = res.get('TRACKING', '-')
            estado = str(res.get('ESTADO', 'PROCESANDO')).upper()
            curso = res.get('CURSO', '-')
            ubi = f"{res.get('DISTRITO', '')}, {res.get('PROVINCIA', '')}"

            bg_p = "#DCFCE7" if "ENTREGADO" in estado else "#FEF9C3"
            tx_p = "#16A34A" if "ENTREGADO" in estado else "#854D0E"

            html_card = f"""
            <div class="main-card">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 10px;">
                    <h2 style="margin:0; font-size: 1.1rem;">{nombre}</h2>
                    <span class="pill" style="background-color: {bg_p}; color: {tx_p};">{estado}</span>
                </div>
                <div style="border-top: 1px solid #EEE; padding-top: 10px; margin-top: 10px;">
                    <p class="info-label">TRACKING</p><p class="info-value" style="color:#2563EB; font-weight:bold;">{tracking}</p>
                    <p class="info-label">CURSO</p><p class="info-value">{curso}</p>
                    <p class="info-label">UBICACIÓN</p><p class="info-value">📍 {ubi}</p>
                </div>
                <a href="https://tracking.olvaexpress.pe" target="_blank" class="olva-btn">🚚 Olva Courier</a>
            </div>
            """
            st.markdown(html_card, unsafe_allow_html=True)
        else:
            st.error("DNI no encontrado.")

st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 0.7rem; margin-top:20px;'>© 2026 Qx Medic | Logística</p>", unsafe_allow_html=True)