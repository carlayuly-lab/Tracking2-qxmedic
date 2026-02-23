import streamlit as st
import pandas as pd

# 1. Configuración de página
st.set_page_config(page_title="Tracking Qx Medic", page_icon="📦", layout="centered")

# 2. CSS Mejorado
st.markdown("""
    <style>
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
    .header-banner {
        background: linear-gradient(135deg, #1E40AF 0%, #1D4ED8 100%);
        padding: 25px; border-radius: 20px; color: white; text-align: center;
        margin-bottom: 30px;
    }
    
    /* --- AQUÍ SE AJUSTA EL TAMAÑO DEL LOGO --- */
    .logo-img {
        max-width: 120px; 
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
        margin-top: 20px; padding: 12px 24px;
        background-color: #2563EB; color: white !important;
        text-decoration: none !important; border-radius: 12px; font-weight: bold;
    }
    .info-label { color: #64748B; font-size: 0.75rem; margin:0; font-weight:bold; text-transform: uppercase; }
    .info-value { margin:0; font-size: 0.95rem; margin-bottom: 10px; color: var(--text-main); font-weight: 500; }
    </style>
    """, unsafe_allow_html=True)

# 3. Datos y Logo
logo_url = "https://www.dropbox.com/scl/fi/65bmjdwdeb8ya3gb4wsw5/logo-qx4.png?rlkey=wlp7kp10dhuvltr3yav3vmw6w&dl=1" 

st.markdown(f'''
    <div class="header-banner">
        <img src="{logo_url}" class="logo-img">
        <h1 style="font-size: 1.8rem; margin-top: 0;">SISTEMA DE TRACKING</h1>
        <p style="margin: 0; opacity: 0.9;">Logística y Envíos 2026</p>
    </div>
''', unsafe_allow_html=True)

# ... El resto del código de carga de datos y lógica se mantiene igual ...