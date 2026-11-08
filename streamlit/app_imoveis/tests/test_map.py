import streamlit as st
from modules.map import render_map
import pandas as pd
from modules.utils import img_to_data_url
from unittest.mock import patch

@patch("modules.utils.img_to_data_url", return_value="data:image/png;base64,fake")
def test_render_map_with_data(mock_icon):
    st.session_state.df = pd.DataFrame([
        {
            "Rua": "Av. Brasil",
            "Número": "10",
            "Cidade": "São Paulo",
            "Estado": "SP",
            "Área": 80,
            "Vagas": 1,
            "Tipo": "Real",
            "Latitude": -23.5,
            "Longitude": -46.6
        },
        {
            "Rua": "Rua Azul",
            "Número": "20",
            "Cidade": "Campinas",
            "Estado": "SP",
            "Área": 100,
            "Vagas": 2,
            "Tipo": "Anúncio",
            "Latitude": -22.9,
            "Longitude": -47.1
        }
    ])

    render_map()
    assert "icon_data" in st.session_state.df.columns
