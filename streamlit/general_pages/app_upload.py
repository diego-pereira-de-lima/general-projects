from vega_datasets import data
import streamlit as st
import altair as alt
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import streamlit as st
import pandas as pd
from io import StringIO



def page_homepage(df):
    st.header("This is your data explorer.")
    st.write("Please select a page on the left.")
    st.write(df)

def page_exploration(df):
    st.title("Data Exploration")
    #x_axis = st.selectbox("Choose a variable for the x-axis", df.columns, index=3)
    y_axis = st.selectbox("Escolha a variavel para o y-axis", ['MAE','DTW'], index=0)
    agencia = st.selectbox("Escolha a variavel para a target",df.AGENCIA.unique(), index=0)
    
    visualize_data(df,  y_axis,agencia)
    visualize_data2(df)


@st.cache_data
def load_data(uploaded_file):
    #df = data.cars()
    df = pd.read_excel(uploaded_file, decimal =',')
    return df

def visualize_data(df, y_axis,agencia):
    # graph = alt.Chart(df).mark_circle(size=60).encode(
    #     x=x_axis,
    #     y=y_axis,
    #     color='Origin',
    #     tooltip=['Name', 'Origin', 'Horsepower', 'Miles_per_Gallon']
    # ).interactive()
    # st.write(graph)

    graph = alt.Chart(df[df['AGENCIA']==agencia]).mark_line().encode(
    x='DATA:T', 
    y=y_axis,
)
    st.write(graph)

def visualize_data2(df):

    col1, col2= st.columns(2)

    with col1:

        # graph = px.histogram(df, x="Miles_per_Gallon",width=300, height=400)
        # graph.update_layout(bargap=0.2)
        # st.write(graph)

        graph=alt.Chart(df).mark_bar().encode(alt.X("MAE", bin=True),
        y='count()',)
        st.write(graph)
    with col2:

        # graph = px.histogram(df, x="Miles_per_Gallon",width=300, height=400)
        # graph.update_layout(bargap=0.2)
        # st.write(graph)
        graph=alt.Chart(df).mark_bar().encode(alt.X("DTW", bin=True),
        y='count()',)
        st.write(graph)


def main():

    page = st.sidebar.selectbox("Menu", ["Homepage", "Exploration"])
    uploaded_file = st.file_uploader("Carregar arquivo", type = 'xlsx')
    if uploaded_file is not None:  
        
        if page == "Homepage":
            df=load_data(uploaded_file)
            page_homepage(df)
        elif page == "Exploration":
            df=load_data(uploaded_file)
            page_exploration(df)

            vec_opt = ['mean', 'median', 'max', 'min']
            vec_columns = st.multiselect(
            "Escolha as colunas?",
            df.columns)
            
            x_axis = st.selectbox("Escolha a variavel para o x-axis", vec_opt, index=3)

            if st.button('Calcular'):
                if x_axis=='mean':
                    st.write(df[vec_columns].mean())
                elif  x_axis=='median':
                    st.write(df[vec_columns].median())
                elif  x_axis=='max':
                    st.write(df[vec_columns].max())
                elif  x_axis=='min':
                    st.write(df[vec_columns].min())
if __name__ == "__main__":
    main()