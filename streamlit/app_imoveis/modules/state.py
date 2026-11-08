
import streamlit as st
import pandas as pd

def initialize_state():
    if "df" not in st.session_state:
        st.session_state.df = pd.DataFrame(columns=[
            "Rua", "Número", "Cidade", "Estado",
            "Área", "Vagas", "Tipo", "Latitude", "Longitude"
        ])
