import streamlit as st
import requests
import json
import BuscarCep  # Certifique-se de que esse módulo está implementado corretamente
import pandas as pd

# CONFIGURAÇÃO DE PÁGINA
st.set_page_config(
    page_title="Busca CEP - Estilo ML",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ESTILO VISUAL PERSONALIZADO
st.markdown("""
    <style>
        html, body, [class*="css"] {
            background-color: #fff200;
            color: #000000 !important;
            font-family: 'Segoe UI', sans-serif;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        h1, h2, h3, p, label, span, div {
            color: #000000 !important;
        }
        .stSidebar {
            background-color: #fff200 !important;
        }
        .stRadio > div > label span {
            color: #000000 !important;
            font-weight: bold !important;
        }
        .stRadio > div > label {
            padding: 10px 14px;
            border-radius: 8px;
            transition: all 0.3s ease-in-out;
        }
        .stRadio > div > label:hover {
            background-color: #ffe600;
            transform: scale(1.03);
            cursor: pointer;
        }
        .stImage img {
            display: block;
            margin-left: auto;
            margin-right: auto;
            border-radius: 16px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            width: 600px !important;
        }
        .stTextInput > div > input {
            background-color: #ffffff;
            color: #333333;
            border: 1px solid #ccc;
            padding: 10px;
            border-radius: 6px;
        }
        .stButton > button {
            background-color: #ff69b4;
            color: #ffffff;
            font-weight: bold;
            border-radius: 8px;
            padding: 10px 20px;
            transition: all 0.3s ease-in-out;
        }
        .stButton > button:hover {
            background-color: #ff1493;
            transform: scale(1.05);
        }
        .stMarkdown a {
            color: #3483fa;
            font-weight: bold;
            transition: all 0.3s ease-in-out;
        }
        .stMarkdown a:hover {
            color: #0056b3;
            text-decoration: underline;
        }
    </style>
""", unsafe_allow_html=True)

# CABEÇALHO
st.markdown("<h1>📦 Busca CEP</h1>", unsafe_allow_html=True)
st.markdown("<h3>Encontre endereços com rapidez e segurança</h3>", unsafe_allow_html=True)
st.markdown("---")

# MENU LATERAL
st.sidebar.header("🧭 Menu")
opcoes = ["🏠 Página Principal", "🔍 Buscar CEP", "📍 Descobrir CEP"]
escolha = st.sidebar.radio("Selecione uma opção:", opcoes)

# CONTEÚDO
if escolha == "🏠 Página Principal":
    st.subheader("👋 Bem-vindo ao Busca CEP!")
    st.write("Use o menu lateral para buscar ou descobrir um CEP.")
    st.image("principal.png", caption="Entrega garantida com segurança")

elif escolha == "🔍 Buscar CEP":
    st.subheader("🔍 Buscar endereço pelo CEP")
    st.image("logo.png", caption="Entrega rápida e segura")
    cep = st.text_input("📬 Digite o CEP com os 8 números:")

    if cep:
        if not cep.isdigit():
            st.warning("⚠️ O CEP deve conter apenas números.")
        elif len(cep) != 8:
            st.warning("⚠️ O CEP deve conter exatamente 8 dígitos.")
        else:
            with st.spinner("🔄 Buscando informações..."):
                try:
                    resultado = BuscarCep.buscar_cep(cep)
                    if resultado:
                        st.success("✅ Endereço encontrado.")
                        st.markdown(f"""
                            - 🔎 **CEP:** {resultado[0]}
                            - 📍 **Endereço:** {resultado[1]}
                            - 🏘️ **Bairro:** {resultado[2]}
                            - 🌆 **Cidade:** {resultado[3]} - {resultado[4]}
                        """)
                        latitude = resultado[5]
                        longitude = resultado[6]
                        if latitude and longitude:
                            st.markdown("🗺️ **Localização do CEP informado no mapa:**")
                            st.markdown(f"""
                                - 📌 **Latitude:** `{latitude}`
                                - 📌 **Longitude:** `{longitude}`
                            """)
                            mapa_df = pd.DataFrame({'lat': [latitude], 'lon': [longitude]})
                            st.map(mapa_df, zoom=15)
                        else:
                            st.info("🗺️ Localização geográfica não disponível para este CEP.")
                    else:
                        st.error("❌ CEP não encontrado.")
                except Exception as e:
                    st.error(f"🚫 Erro ao buscar CEP: {e}")

elif escolha == "📍 Descobrir CEP":
    st.subheader("📍 Descobrir o CEP pelo endereço")
    st.image("descobrir.png", caption="Encontre o CEP ideal")
    endereco = st.text_input("🏠 Digite o endereço completo:")
    if endereco:
        with st.spinner("🔄 Buscando no Google..."):
            try:
                url_resultado = BuscarCep.descobrir_cep(endereco)
                st.success("✅ Busca realizada.")
                st.markdown("🔍 Resultado da busca no Google:")
                st.markdown(f"[📎 Clique aqui para ver o resultado]({url_resultado})")
            except Exception as e:
                st.error(f"🚫 Erro ao descobrir CEP: {e}")
