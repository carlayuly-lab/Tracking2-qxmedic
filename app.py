import streamlit as st
import pandas as pd

# 1. Configuración de página
st.set_page_config(page_title="Tracking Qx Medic", page_icon="📦", layout="centered")

# 2. CSS DE LIMPIEZA TOTAL (Superior e Inferior)
st.markdown("""
    <style>
    /* 1. OCULTAR BARRA SUPERIOR Y MENÚ DE PERFIL */
    header[data-testid="stHeader"] {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* 2. OCULTAR EL TOOLBAR DE STREAMLIT (Deploy, Config, etc.) */
    [data-testid="stToolbar"] {
        display: none !important;
        visibility: hidden !important;
    }

    /* 3. OCULTAR LA BARRA INFERIOR (Hosted with Streamlit) */
    /* Este selector apunta al widget de estado y al footer estándar */
    footer {
        display: none !important;
        visibility: hidden !important;
    }
    
    #MainMenu {
        visibility: hidden !important;
    }

    /* Ocultar el botón flotante de la comunidad en la esquina inferior */
    div[data-testid="stStatusWidget"], .stDeployButton {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Regla agresiva para el botón rojo de "Hosted with Streamlit" */
    div[class^="st-emotion-cache-"] > div[data-testid="stToolbar"] {
        display: none !important;
    }

    /* 4. AJUSTE DE DISEÑO */
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
    .header-banner {
        background: linear-gradient(135deg, #1E40AF 0%, #1D4ED8 100%);
        padding: 35px 20px; border-radius: 20px; color: white; text-align: center;
        margin-bottom: 30px;
    }
    
    .logo-img {
        max-width: 180px;
        margin-bottom: 10px;
        filter: drop-shadow(0px 4px 6px rgba(0,0,0,0.1));
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
    }
    .info-label { color: #64748B; font-size: 0.75rem; margin:0; font-weight:bold; text-transform: uppercase; }
    .info-value { margin:0; font-size: 0.95rem; margin-bottom: 10px; color: var(--text-main); font-weight: 500; }
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
        st.error(f"Error: {e}")
        return None

# --- UI ---
logo_url = "https://www.dropbox.com/scl/fi/65bmjdwdeb8ya3gb4wsw5/logo-qx4.png?rlkey=wlp7kp10dhuvltr3yav3vmw6w&raw=1"

st.markdown(f'''
    <div class="header-banner">
        <img src="{logo_url}" class="logo-img">
        <p style="margin:0; opacity: 0.9; font-size: 1.1rem; font-weight: 300; letter-spacing: 1px;">
            SISTEMA DE SEGUIMIENTO 2026
        </p>
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

st.markdown("<br><p style='text-align: center; color: #94A3B8; font-size: 0.75rem;'>© 2026 Qx Medic | Logística</p>", unsafe_allow_html=True)