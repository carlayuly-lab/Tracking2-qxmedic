import streamlit as st
import pandas as pd

# 1. Configuración de página
st.set_page_config(page_title="Tracking Qx Medic", page_icon="📦", layout="centered")

# 2. CSS Mejorado: Ajuste de Logo y Estética
st.markdown("""
    <style>
    /* OCULTAR ELEMENTOS DE STREAMLIT */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stAppDeployButton {display:none;}
    
    :root {
        --bg-card: white;
        --text-main: #1E293B;
        --border-color: #EEE;
    }
    @media (prefers-color-scheme: dark) {
        :root {
            --bg-card: #1E293B;
            --text-main: #F8FAFC;
            --border-color: #334155;
        }
    }

    /* --- BANNER PRINCIPAL --- */
    .header-banner {
        background: linear-gradient(135deg, #1E40AF 0%, #1D4ED8 100%);
        padding: 30px 15px; 
        border-radius: 20px; 
        color: white; 
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* --- LOGO RE-ESTILIZADO (Corrección de ancho) --- */
    .logo-img {
        width: 180px; /* Ancho fijo para evitar que se vea estirado */
        height: auto; /* Mantiene la proporción original */
        margin-bottom: 15px;
        filter: drop-shadow(0px 4px 8px rgba(0,0,0,0.3));
        object-fit: contain;
    }
    
    .main-card {
        background-color: var(--bg-card); 
        padding: 30px; border-radius: 25px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1); 
        border-top: 8px solid #1E40AF;
        color: var(--text-main);
    }
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
        transition: transform 0.2s;
    }
    .olva-btn:hover {
        transform: scale(1.02);
        background-color: #1D4ED8;
    }
    .info-label { color: #64748B; font-size: 0.75rem; margin:0; font-weight:bold; text-transform: uppercase; }
    .info-value { margin:0; font-size: 0.95rem; margin-bottom: 10px; color: var(--text-main); font-weight: 500; }
    </style>
    """, unsafe_allow_html=True)

# 3. Carga de datos optimizada
@st.cache_data(ttl=300)
def load_data():
    try:
        # Tu ID de hoja y GID de la pestaña de Tracking
        sheet_id = "1tkKTopAlCGS_Ba7DaCkWFOHiwr_1uiU_Bima_cM5qcY"
        gid = "1777353802"
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
        df = pd.read_csv(url, dtype=str)
        # Limpiar nombres de columnas
        df.columns = [str(c).strip().upper() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return None

# --- UI HEADER ---
logo_url = "https://www.dropbox.com/scl/fi/1tbfn3ge2b33nqnjgagft/LOGO-QX-MEDIC-600x315.png?rlkey=4qwxkmhs736fovnz2l3oxzier&raw=1" 

st.markdown(f'''
    <div class="header-banner">
        <img src="{logo_url}" class="logo-img">
        <h1 style="font-size: 1.6rem; margin: 0; font-weight: 800;">SISTEMA DE TRACKING</h1>
        <p style="margin: 5px 0 0 0; opacity: 0.8; font-size: 0.9rem;">Logística y Envíos 2026</p>
    </div>
''', unsafe_allow_html=True)

# --- LÓGICA DE BÚSQUEDA ---
data = load_data()

if data is not None:
    # Contenedor de búsqueda centrado
    dni_input = st.text_input("🔍 Ingresa tu DNI para consultar:", placeholder="Ej. 72190439").strip()

    if dni_input:
        # Filtro de seguridad por DNI
        resultado = data[data['DNI'].astype(str) == str(dni_input)]

        if not resultado.empty:
            res = resultado.iloc[0]
            st.balloons()

            # Extracción de variables del Excel
            nombre = res.get('NOMBRES', 'No disponible')
            tracking = res.get('TRACKING', 'PENDIENTE')
            estado = str(res.get('ESTADO', 'PROCESANDO')).upper()
            curso = res.get('CURSO', '-')
            registro = res.get('FECHA DE REGISTRO', '-')
            entrega = res.get('FECHA DE ENTREGA', '-')
            obs = res.get('OBSERVACIÓN', 'NINGUNA')
            ubi = f"{res.get('DISTRITO', '')}, {res.get('PROVINCIA', '')} - {res.get('DEPARTAMENTO', '')}"

            # Colores dinámicos según estado
            bg_p = "#DCFCE7" if "ENTREGADO" in estado else "#FEF9C3"
            tx_p = "#16A34A" if "ENTREGADO" in estado else "#854D0E"

            # Tarjeta de resultado (Card)
            html_card = f"""
            <div class="main-card">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 20px;">
                    <div>
                        <p class="info-label">ESTUDIANTE</p>
                        <h2 style="margin:0; font-size: 1.4rem; line-height: 1.2;">{nombre}</h2>
                    </div>
                    <span class="pill" style="background-color: {bg_p}; color: {tx_p};">{estado}</span>
                </div>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; border-top: 1px solid var(--border-color); padding-top: 15px;">
                    <div><p class="info-label">N° TRACKING</p><p style="font-weight: 800; color: #3B82F6; margin:0; font-size: 1.2rem;">{tracking}</p></div>
                    <div><p class="info-label">FECHA REGISTRO</p><p class="info-value">{registro}</p></div>
                </div>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 10px;">
                    <div><p class="info-label">CURSO</p><p class="info-value">{curso}</p></div>
                    <div><p class="info-label">FECHA ENTREGA</p><p class="info-value">{entrega}</p></div>
                </div>
                
                <div style="margin-top: 10px;"><p class="info-label">DESTINO</p><p class="info-value">📍 {ubi}</p></div>
                
                <div style="margin-top: 10px; padding: 12px; background: rgba(148, 163, 184, 0.1); border-radius: 12px; border-left: 4px solid #3B82F6;">
                    <p class="info-label">NOTAS DE LOGÍSTICA</p><p style="margin:0; font-size: 0.85rem; font-style: italic;">{obs}</p>
                </div>
                
                <center>
                    <a href="https://tracking.olvaexpress.pe" target="_blank" class="olva-btn">🚚 Rastrear en Olva Courier</a>
                </center>
            </div>
            """
            st.markdown(html_card, unsafe_allow_html=True)
        else:
            st.warning(f"⚠️ El DNI {dni_input} no se encuentra en nuestra base de datos actual.")

# Pie de página
st.markdown("<br><p style='text-align: center; color: #94A3B8; font-size: 0.8rem;'>© 2026 QX Medic | Todos los derechos reservados</p>", unsafe_allow_html=True)