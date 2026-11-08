import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim
import pydeck as pdk
import base64

st.set_page_config(page_title="Mapa de Imóveis", layout="wide")
st.title("📍 Mapa de Imóveis com Ícones Locais")

geolocator = Nominatim(user_agent="streamlit-app")

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=[
        "Rua", "Número", "Cidade", "Estado",
        "Área", "Vagas", "Tipo", "Latitude", "Longitude"
    ])

def geocode_address(rua, numero, cidade, estado):
    endereco = f"{rua}, {numero}, {cidade}, {estado}, Brasil"
    try:
        location = geolocator.geocode(endereco)
        return location.latitude, location.longitude if location else (None, None)
    except:
        return None, None

def img_to_data_url(path):
    with open(path, "rb") as img_file:
        b64_str = base64.b64encode(img_file.read()).decode()
    ext = path.split('.')[-1]
    return f"data:image/{ext};base64,{b64_str}"

# Converte as imagens locais em data URLs
icon_laranja_url = img_to_data_url("imgs/laranja.png")
icon_azul_url = img_to_data_url("imgs/azul.png")

with st.form("formulario"):
    st.subheader("Adicionar Imóvel")

    tipo_input = st.radio("Modo de entrada", ["Endereço", "Latitude/Longitude"])

    col1, col2 = st.columns(2)
    with col1:
        area = st.number_input("Área (m²)", min_value=0.0)
        vagas = st.number_input("Vagas", min_value=0)
        tipo_imovel = st.selectbox("Tipo de imóvel", ["Real", "Anúncio"])

    if tipo_input == "Endereço":
        rua = st.text_input("Rua")
        numero = st.text_input("Número")
        cidade = st.text_input("Cidade")
        estado = st.text_input("Estado")

    else:
        lat = st.number_input("Latitude", format="%.6f")
        lon = st.number_input("Longitude", format="%.6f")

    enviado = st.form_submit_button("Adicionar imóvel")

    if enviado:
        if tipo_input == "Endereço":
            if rua and numero and cidade and estado:
                lat, lon = geocode_address(rua, numero, cidade, estado)
                if lat and lon:
                    nova_linha = {
                        "Rua": rua, "Número": numero, "Cidade": cidade, "Estado": estado,
                        "Área": area, "Vagas": vagas, "Tipo": tipo_imovel,
                        "Latitude": lat, "Longitude": lon
                    }
                    st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([nova_linha])], ignore_index=True)
                    st.success("Imóvel adicionado!")
                else:
                    st.error("Endereço não localizado.")
            else:
                st.warning("Preencha todos os campos.")
        else:
            if lat and lon:
                nova_linha = {
                    "Rua": "", "Número": "", "Cidade": "", "Estado": "",
                    "Área": area, "Vagas": vagas, "Tipo": tipo_imovel,
                    "Latitude": lat, "Longitude": lon
                }
                st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([nova_linha])], ignore_index=True)
                st.success("Imóvel adicionado!")
            else:
                st.warning("Informe latitude e longitude válidos.")

df = st.session_state.df

if not df.empty:
    st.subheader("📌 Mapa de Imóveis")

    def get_icon_data(tipo):
        return {
            "url": icon_laranja_url if tipo == "Real" else icon_azul_url,
            "width": 100,
            "height": 100,
            "anchorY": 100
        }

    df["icon_data"] = df["Tipo"].apply(get_icon_data)

    icon_layer = pdk.Layer(
        "IconLayer",
        data=df,
        get_icon="icon_data",
        get_position="[Longitude, Latitude]",
        size_scale=20,
        pickable=True
    )

    view_state = pdk.ViewState(
        latitude=df["Latitude"].mean(),
        longitude=df["Longitude"].mean(),
        zoom=10,
        pitch=0
    )

    tooltip = {
        "html": """
            <b>Tipo:</b> {Tipo}<br/>
            <b>Área:</b> {Área} m²<br/>
            <b>Vagas:</b> {Vagas}<br/>
            <b>Cidade:</b> {Cidade}<br/>
        """,
        "style": {"color": "black"}
    }

    st.pydeck_chart(pdk.Deck(
        layers=[icon_layer],
        initial_view_state=view_state,
        tooltip=tooltip
    ))
else:
    st.info("Nenhum imóvel adicionado.")
