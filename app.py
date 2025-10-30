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

                        # ✅ Verifica e converte corretamente latitude/longitude
                        if latitude is not None and longitude is not None:
                            try:
                                lat = float(latitude)
                                lon = float(longitude)
                                st.markdown("🗺️ **Localização do CEP informado no mapa:**")
                                st.markdown(f"""
                                    - 📌 **Latitude:** `{lat}`
                                    - 📌 **Longitude:** `{lon}`
                                """)
                                mapa_df = pd.DataFrame({'lat': [lat], 'lon': [lon]})
                                st.map(mapa_df, zoom=15)
                            except (ValueError, TypeError):
                                st.info("🗺️ Localização geográfica não disponível para este CEP.")
                        else:
                            st.info("🗺️ Localização geográfica não disponível para este CEP.")
                    else:
                        st.error("❌ CEP não encontrado.")
                except Exception as e:
                    st.error(f"🚫 Erro ao buscar CEP: {e}")

elif escolha == "📍 Descobrir CEP":
    st.subheader("📍 Descobrir o CEP pelo endereço")
    st.image("Descobrir.png", caption="Encontre o CEP ideal")
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