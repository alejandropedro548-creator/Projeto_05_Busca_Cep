import streamlit as st
import requests
import json
import BuscarCep  # Certifique-se de que esse módulo está implementado corretamente
import pandas as pd
import math

# --------------------------
# FUNÇÕES AUXILIARES
# --------------------------
def safe_float(x):
    """Tenta converter x para float; retorna None se não for possível."""
    if x is None or (isinstance(x, str) and x.strip().lower() == "none"):
        return None
    try:
        return float(x)
    except (ValueError, TypeError):
        return None

def extract_lat_lon(resultado):
    """
    Tenta extrair latitude e longitude de 'resultado' retornado por BuscarCep.buscar_cep.
    Suporta: lista/tupla no formato [cep, endereco, bairro, cidade, uf, lat, lon]
    ou dicionário com chaves prováveis.
    Retorna (lat_float_or_None, lon_float_or_None)
    """
    lat = None
    lon = None

    if isinstance(resultado, dict):
        possible_lat_keys = ["latitude", "lat", "lati", "y", "latitude_value"]
        possible_lon_keys = ["longitude", "lon", "lng", "x", "longitude_value"]
        for k in possible_lat_keys:
            if k in resultado:
                lat = resultado.get(k)
                break
        for k in possible_lon_keys:
            if k in resultado:
                lon = resultado.get(k)
                break

    if (lat is None or lon is None) and isinstance(resultado, (list, tuple)):
        if len(resultado) > 6:
            lat = lat if lat is not None else resultado[5]
            lon = lon if lon is not None else resultado[6]
        elif len(resultado) > 5:
            lat = lat if lat is not None else resultado[5]

    if (lat is None or lon is None) and isinstance(resultado, (list, tuple)):
        for item in resultado:
            if lat is None:
                maybe = safe_float(item)
                if maybe is not None and -90 <= maybe <= 90:
                    lat = maybe
                    continue
            if lon is None:
                maybe = safe_float(item)
                if maybe is not None and -180 <= maybe <= 180:
                    lon = maybe
                    continue

    latf = safe_float(lat) if lat is not None else None
    lonf = safe_float(lon) if lon is not None else None

    return latf, lonf

def is_valid_coordinate(value, lat_or_lon="lat"):
    """Valida se 'value' é número real e está dentro dos limites de latitude/longitude."""
    if value is None:
        return False
    if not isinstance(value, (float, int)):
        return False
    if math.isnan(value) or math.isinf(value):
        return False
    if lat_or_lon == "lat":
        return -90.0 <= value <= 90.0
    else:
        return -180.0 <= value <= 180.0

# --------------------------
# STREAMLIT APP
# --------------------------
st.set_page_config(
    page_title="Busca CEP - Estilo ML",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("<h1>📦 Busca CEP</h1>", unsafe_allow_html=True)
st.markdown("<h3>Encontre endereços com rapidez e segurança</h3>", unsafe_allow_html=True)
st.markdown("---")

st.sidebar.header("🧭 Menu")
opcoes = ["🏠 Página Principal", "🔍 Buscar CEP", "📍 Descobrir CEP"]
escolha = st.sidebar.radio("Selecione uma opção:", opcoes)

if escolha == "🏠 Página Principal":
    st.subheader("👋 Bem-vindo ao Busca CEP!")
    st.write("Use o menu lateral para buscar ou descobrir um CEP.")
    try:
        st.image("principal.png", caption="Entrega garantida com segurança")
    except Exception:
        pass

elif escolha == "🔍 Buscar CEP":
    st.subheader("🔍 Buscar endereço pelo CEP")
    try:
        st.image("logo.png", caption="Entrega rápida e segura")
    except Exception:
        pass

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
                        cep_res = endereco_res = bairro_res = cidade_res = uf_res = None

                        if isinstance(resultado, (list, tuple)):
                            cep_res = resultado[0] if len(resultado) > 0 else None
                            endereco_res = resultado[1] if len(resultado) > 1 else None
                            bairro_res = resultado[2] if len(resultado) > 2 else None
                            cidade_res = resultado[3] if len(resultado) > 3 else None
                            uf_res = resultado[4] if len(resultado) > 4 else None
                        elif isinstance(resultado, dict):
                            cep_res = resultado.get("cep") or resultado.get("CEP") or resultado.get("postal_code")
                            endereco_res = resultado.get("endereco") or resultado.get("logradouro") or resultado.get("address")
                            bairro_res = resultado.get("bairro") or resultado.get("neighborhood")
                            cidade_res = resultado.get("cidade") or resultado.get("localidade") or resultado.get("city")
                            uf_res = resultado.get("uf") or resultado.get("estado") or resultado.get("state")

                        st.success("✅ Endereço encontrado.")
                        st.markdown(f"""
                            - 🔎 **CEP:** {cep_res or cep}
                            - 📍 **Endereço:** {endereco_res or '—'}
                            - 🏘️ **Bairro:** {bairro_res or '—'}
                            - 🌆 **Cidade:** {cidade_res or '—'} - {uf_res or '—'}
                        """)

                        latf, lonf = extract_lat_lon(resultado)

                        if is_valid_coordinate(latf, "lat") and is_valid_coordinate(lonf, "lon"):
                            st.markdown("🗺️ **Localização do CEP informado no mapa:**")
                            st.markdown(f"""
                                - 📌 **Latitude:** `{latf}`
                                - 📌 **Longitude:** `{lonf}`
                            """)
                            mapa_df = pd.DataFrame({'lat': [latf], 'lon': [lonf]})
                            st.map(mapa_df, zoom=15)
                        else:
                            st.info("🗺️ Localização geográfica não disponível ou inválida para este CEP.")
                    else:
                        st.error("❌ CEP não encontrado.")
                except Exception as e:
                    st.error(f"🚫 Erro ao buscar CEP: {e}")

elif escolha == "📍 Descobrir CEP":
    st.subheader("📍 Descobrir o CEP pelo endereço")
    try:
        st.image("Descobrir.png", caption="Encontre o CEP ideal")
    except Exception:
        pass

    endereco = st.text_input("🏠 Digite o endereço completo:")
    if endereco:
        with st.spinner("🔄 Buscando no Google..."):
            try:
                url_resultado = BuscarCep.descobrir_cep(endereco)
                st.success("✅ Busca realizada.")
                st.markdown("🔍 Resultado da busca no Google:")
                if url_resultado:
                    st.markdown(f"[📎 Clique aqui para ver o resultado]({url_resultado})")
                else:
                    st.info("Nenhum resultado encontrado.")
            except Exception as e:
                st.error(f"🚫 Erro ao descobrir CEP: {e}")
