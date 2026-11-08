# tests/test_form.py
import streamlit as st
import pandas as pd
from unittest.mock import patch, MagicMock
from modules.forms import render_form

@patch("modules.forms.geocode_address", return_value=(-23.5, -46.6))
@patch("streamlit.form_submit_button", return_value=True)
@patch("streamlit.radio", return_value="Endereço")
@patch("streamlit.text_input")
@patch("streamlit.number_input")
@patch("streamlit.selectbox", return_value="Real")
@patch("streamlit.columns")
def test_render_form_endereco(
    mock_columns,
    mock_selectbox,
    mock_number_input,
    mock_text_input,
    mock_radio,
    mock_submit_button,
    mock_geocode
):
    # Cria mocks que funcionam como context manager (com 'with')
    mock_col = MagicMock()
    mock_col.__enter__.return_value = mock_col
    mock_col.__exit__.return_value = None
    mock_columns.return_value = [mock_col, mock_col]

    # Simula os inputs
    mock_text_input.side_effect = ["Av. Brasil", "10", "São Paulo", "SP"]
    mock_number_input.side_effect = [120.0, 2]

    # Prepara session_state
    st.session_state.clear()
    st.session_state.df = pd.DataFrame(columns=[
        "Rua", "Número", "Cidade", "Estado",
        "Área", "Vagas", "Tipo", "Latitude", "Longitude"
    ])

    render_form()

    # Verifica inserção
    assert not st.session_state.df.empty
    row = st.session_state.df.iloc[0]
    assert row["Cidade"] == "São Paulo"
    assert row["Área"] == 120.0
    assert row["Latitude"] == -23.5
