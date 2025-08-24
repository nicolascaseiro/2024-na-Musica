import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("https://raw.githubusercontent.com/nicolascaseiro/2024-na-Musica/refs/heads/main/2024%20na%20M%C3%BAsica.csv", encoding='utf-8')

df['Gêneros_lista'] = df['Gêneros'].dropna().apply(lambda x: [g.strip() for g in x.split(',')])
df_exploded = df.explode('Gêneros_lista')

st.title("Dashboard de Músicas")

generos = sorted(df_exploded['Gêneros_lista'].dropna().unique())
artistas = sorted(df['Artista'].dropna().unique())

genero_selecionado = st.sidebar.multiselect('Filtrar por Gênero:', generos)
artista_selecionado = st.sidebar.multiselect('Filtrar por Artista:', artistas)

df_filtrado = df_exploded.copy()

if genero_selecionado:
    df_filtrado = df_filtrado[df_filtrado['Gêneros_lista'].isin(genero_selecionado)]
if artista_selecionado:
    df_filtrado = df_filtrado[df_filtrado['Artista'].isin(artista_selecionado)]

st.write(f"Total músicas: {df_filtrado.shape[0]}")

fig = px.bar(df_filtrado.groupby('Gêneros_lista')['Popularidade'].mean().reset_index(),
             x='Gêneros_lista', y='Popularidade', title='Popularidade média por gênero')
st.plotly_chart(fig)
