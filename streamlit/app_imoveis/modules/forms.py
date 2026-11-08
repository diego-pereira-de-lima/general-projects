import streamlit as st
import pandas as pd
from modules.utils import geocode_address

def render_form():
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

