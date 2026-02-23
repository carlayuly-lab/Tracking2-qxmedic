import streamlit as st
import pandas as pd

# 1. Configuración de página - Debe ser la primera instrucción
st.set_page_config(page_title="Tracking", page_icon="📦", layout="centered")

# 2. CSS Simplificado y Seguro
st.markdown("""
    <style>
    /* Ocultar elementos de la interfaz de Streamlit de forma segura */
    header, footer, .stAppDeployButton {
        display: none !important;
    }
    
    #MainMenu { visibility: hidden; }

    /* Contenedor de la tarjeta de resultados */
    .main-card {
        background-color: white; 
        padding: 25px; 
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1); 
        border-top: 6px solid #1E40AF;
        color: #1E293B;
        margin-top: 20px;
    }

    .info-label { color: #64748B; font-size: 0.75rem; margin:0; font-weight:bold; text-transform: uppercase; }
    .info-value { margin:0; font-size: 0.95rem; margin-bottom: 8px; color: #1E293B; font-weight: 500; }
    
    .pill {
        padding: 4px 12px; border-radius: 50px; font-weight: bold; font-size: 0.75rem;
    }
    
    .olva-btn {
        display: inline-block;
        margin-top: 15px;
        padding: 10px 20px;
        background-color: #2563EB;
        color: white !important;
        text-decoration: none !important;
        border-radius: 10px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Carga de datos optimizada
@st.cache_data(ttl=300)
def load_data():
    try:
        # URL de tu Google Sheet (asegúrate de que el CSV sea accesible)
        sheet_id = "1tkKTopAlCGS_Ba7DaCkWFOHiwr_1uiU_Bima_cM5qcY"
        gid = "1777353802"
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
        df = pd.read_csv(url, dtype=str)
        df.columns = [str(c).strip().upper() for c in df.columns]
        return df
    except Exception as e:
        return None

# --- Interfaz de Usuario (UI) ---

data = load_data()

if data is not None:
    # Espacio opcional arriba si quieres que no pegue al borde superior de Jotform
    st.write("") 
    
    dni_input = st.text_input("🔍 Ingresa tu DNI:", placeholder="Ej. 70254718").strip()

    if dni_input:
        # Filtrar por DNI
        resultado = data[data['DNI'].astype(str) == str(dni_input)]

        if not resultado.empty:
            res = resultado.iloc[0]
            st.balloons()

            # Obtener datos de la fila
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

            # Tarjeta de resultados en HTML
            html_card = f"""
            <div class="main-card">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 10px;">
                    <div>
                        <p class="info-label">ESTUDIANTE</p>
                        <h2 style="margin:0; font-size: 1.2rem;">{nombre}</h2>
                    </div>
                    <span class="pill" style="background-color: {bg_p}; color: {tx_p};">{estado}</span>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; border-top: 1px solid #EEE; padding-top: 10px;">
                    <div><p class="info-label">TRACKING</p><p style="font-weight: 800; color: #3B82F6; margin:0; font-size: 1.1rem;">{tracking}</p></div>
                    <div><p class="info-label">REGISTRO</p><p class="info-value">{registro}</p></div>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                    <div><p class="info-label">CURSO</p><p class="info-value">{curso}</p></div>
                    <div><p class="info-label">FECHA ENTREGA</p><p class="info-value">{entrega}</p></div>
                </div>
                <div style="margin-top: 5px;"><p class="info-label">UBICACIÓN</p><p class="info-value">📍 {ubi}</p></div>
                <div style="margin-top: 5px; padding: 10px; background: #F8FAFC; border-radius: 10px;">
                    <p class="info-label">OBSERVACIÓN</p><p style="margin:0; font-size: 0.8rem; font-style: italic;">{obs}</p>
                </div>
                <a href="https://tracking.olvaexpress.pe" target="_blank" class="olva-btn">🚚 Ver en Olva Courier</a>
            </div>
            """
            st.markdown(html_card, unsafe_allow_html=True)
        else:
            st.error("❌ No se encontró el DNI.")
else:
    st.error("Error al conectar con la base de datos de Google Sheets.")

# Pie de página opcional y discreto
st.markdown("<br><p style='text-align: center; color: #94A3B8; font-size: 0.7rem;'>Sistema de Logística 2026</p>", unsafe_allow_html=True)