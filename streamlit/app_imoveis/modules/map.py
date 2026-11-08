import streamlit as st
import pydeck as pdk
from modules.utils import img_to_data_url

def render_map():
    df = st.session_state.df

    if not df.empty:
        st.subheader("📌 Mapa de Imóveis")

        icon_laranja_url = img_to_data_url("imgs/laranja.png")
        icon_azul_url = img_to_data_url("imgs/azul.png")

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
            tooltip=tooltip,

        ))
    else:
        st.info("Nenhum imóvel adicionado.")
