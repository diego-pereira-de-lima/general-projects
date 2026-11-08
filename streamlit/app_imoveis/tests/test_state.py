import streamlit as st
from modules.state import initialize_state
import pandas as pd

def test_initialize_state_creates_df():
    st.session_state.clear()
    initialize_state()
    assert "df" in st.session_state
    assert isinstance(st.session_state.df, pd.DataFrame)
    expected_columns = [
        "Rua", "Número", "Cidade", "Estado",
        "Área", "Vagas", "Tipo", "Latitude", "Longitude"
    ]
    assert list(st.session_state.df.columns) == expected_columns