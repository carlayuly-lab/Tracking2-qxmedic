import streamlit as st
import pandas as pd

# 1. Configuración de página
st.set_page_config(page_title="Tracking", page_icon="📦", layout="centered")

# 2. CSS Ultra-Simplificado (Solo lo esencial para que no falle)
st.markdown("""
    <style>
    /* Ocultar elementos básicos de la interfaz de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Eliminar espacios blancos superiores */
    .block-container {
        padding-top: 1rem !important;
    }

    /* Estilos de la tarjeta y banner */
    .header-banner {
        background: linear-gradient(135deg, #1E40AF 0%, #1D4ED8 100%);
        padding: 30px; 
        border-radius: 20px; 
        margin-bottom: 30px;
        min-height: 100px; /* Banner azul vacío pero presente */
    }
    
    .main-card {
        background-color: white; 
        padding: 30px; 
        border-radius: 25px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1); 
        border-top: 8px solid #1E40AF;
        color: #1E293B;
    }

    .info-label { color: #64748B; font-size: 0.75rem; margin:0; font-weight:bold; text-transform: uppercase; }
    .info-value { margin:0; font-size: 0.95rem; margin-bottom: 10px; color: #1E293B; font-weight: 500; }
    
    .pill {
        padding: 6px 15px; border-radius: 50px; font-weight: bold; font-size: 0.8rem;
    }
    
    .olva-btn {
        display: inline-block;
        margin-top: 20px;
        padding: 12px 24px;
        background-color: #2563EB;
        color: white !important;
        text-decoration: none !important;
        border-radius: 12px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Carga de datos
@st.cache_data(ttl=300)
def load_data():
    try:
        # Usando los datos de tu Google Sheet
        sheet_id = "1tkKTopAlCGS_Ba7DaCkWFOHiwr_1uiU_Bima_cM5qcY"
        gid = "1777353802"
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
        df = pd.read_csv(url, dtype=str)
        df.columns = [str(c).strip().upper() for c in df.columns]
        return df
    except Exception as e:
        return None

# --- UI ---
# Banner azul vacío (sin texto ni logos)
st.markdown('<div class="header-banner"></div>', unsafe_allow_html=True)

data = load_data()

if data is not None:
    dni_input = st.text_input("🔍 Ingresa tu DNI:", placeholder="Ej. 70254718").strip()

    if dni_input:
        resultado = data[data['DNI'].astype(str) == str(dni_input)]

        if not resultado.empty:
            res = resultado.iloc[0]
            st.balloons()

            nombre = res.get('NOMBRES', '-')
            tracking = res.get('TRACKING', 'PENDIENTE')
            estado = str(res.get('ESTADO', 'PROCESANDO')).upper()
            curso = res.get('CURSO', '-')
            registro = res.get('FECHA DE REGISTRO', '-')
            entrega = res.get('FECHA DE ENTREGA', '-')
            obs = res.get('OBSERVACIÓN', 'NINGUNA')
            ubi = f"{res.get('DISTRITO', '')}, {res.get('PROVINCIA', '')} - {res.get('DEPARTAMENTO', '')}"

            bg_p = "#DCFCE7" if "ENTREGADO" in estado else "#FEF9C3"
            tx_p = "#16A34A" if "ENTREGADO" in estado else "#854D0E"

            html_card = f"""
            <div class="main-card">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 15px;">
                    <div>
                        <p class="info-label">ESTUDIANTE</p>
                        <h2 style="margin:0; font-size: 1.4rem;">{nombre}</h2>
                    </div>
                    <span class="pill" style="background-color: {bg_p}; color: {tx_p};">{estado}</span>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; border-top: 1px solid var(--border-color); padding-top: 15px;">
                    <div><p class="info-label">TRACKING</p><p style="font-weight: 800; color: #3B82F6; margin:0; font-size: 1.2rem;">{tracking}</p></div>
                    <div><p class="info-label">REGISTRO</p><p class="info-value">{registro}</p></div>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 10px;">
                    <div><p class="info-label">CURSO</p><p class="info-value">{curso}</p></div>
                    <div><p class="info-label">FECHA ENTREGA</p><p class="info-value">{entrega}</p></div>
                </div>
                <div style="margin-top: 10px;"><p class="info-label">UBICACIÓN</p><p class="info-value">📍 {ubi}</p></div>
                <div style="margin-top: 10px; padding: 12px; background: rgba(148, 163, 184, 0.1); border-radius: 12px;">
                    <p class="info-label">OBSERVACIÓN</p><p style="margin:0; font-size: 0.85rem; font-style: italic;">{obs}</p>
                </div>
                <a href="https://tracking.olvaexpress.pe" target="_blank" class="olva-btn">🚚 Ver en Olva Courier</a>
            </div>
            """
            st.markdown(html_card, unsafe_allow_html=True)
        else:
            st.error("❌ No se encontró el DNI.")
else:
    st.error("Error al conectar con la base de datos.")