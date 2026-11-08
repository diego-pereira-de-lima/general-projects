import pytest
import pandas as pd
from unittest.mock import patch, mock_open, MagicMock
import streamlit as st
from app import img_to_data_url, geocode_address

# ----------------------
# Testes para img_to_data_url
# ----------------------
@patch("builtins.open", new_callable=mock_open, read_data=b"fakebytes")
def test_img_to_data_url_success(mock_file):
    result = img_to_data_url("imgs/laranja.png")
    assert result.startswith("data:image/png;base64,")

@patch("builtins.open", side_effect=FileNotFoundError("not found"))
def test_img_to_data_url_failure(mock_file):
    result = img_to_data_url("imgs/inexistente.png")
    assert result is None

# ----------------------
# Testes para geocode_address
# ----------------------
@patch("app.geolocator.geocode")
def test_geocode_address_success(mock_geocode):
    mock_location = MagicMock()
    mock_location.latitude = -23.5
    mock_location.longitude = -46.6
    mock_geocode.return_value = mock_location

    lat, lon = geocode_address("Rua A", "100", "São Paulo", "SP")
    assert lat == -23.5
    assert lon == -46.6

@patch("app.geolocator.geocode")
def test_geocode_address_none(mock_geocode):
    mock_geocode.return_value = None
    lat, lon = geocode_address("Rua Inexistente", "0", "X", "Y")
    assert lat is None
    assert lon is None

@patch("app.geolocator.geocode", side_effect=Exception("error"))
def test_geocode_address_exception(mock_geocode):
    lat, lon = geocode_address("Rua Erro", "0", "X", "Y")
    assert lat is None
    assert lon is None

# ----------------------
# Teste simples de estado de sessão
# ----------------------
def test_session_state_df_creation():
    st.session_state.clear()
    from app import st  # força a execução de app.py (estrutura)
    assert isinstance(st.session_state.df, pd.DataFrame)
    assert list(st.session_state.df.columns) == [
        "Rua", "Número", "Cidade", "Estado",
        "Área", "Vagas", "Tipo", "Latitude", "Longitude"
    ]
