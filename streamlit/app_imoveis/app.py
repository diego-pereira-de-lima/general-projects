import streamlit as st
from modules.forms import render_form
from modules.map import render_map
from modules.state import initialize_state

st.set_page_config(page_title="Mapa de Imóveis", layout="wide")
st.title("📍 Mapa de Imóveis com Ícones Locais")

initialize_state()
render_form()
render_map()
