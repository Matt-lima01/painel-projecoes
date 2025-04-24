
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Projeções Pizzaria", layout="wide")
st.title("📊 Projeções Financeiras - Pizzaria")

@st.cache_data
def carregar_dados():
    return pd.DataFrame([
        {'Trimestre': 0, 'Cenário': 'Atual', 'Faturamento': 41400, 'Lucro': 21984},
        {'Trimestre': 3, 'Cenário': 'Atual', 'Faturamento': 44850, 'Lucro': 23856},
        {'Trimestre': 6, 'Cenário': 'Atual', 'Faturamento': 48300, 'Lucro': 25728},
        {'Trimestre': 9, 'Cenário': 'Atual', 'Faturamento': 51750, 'Lucro': 27600},
        {'Trimestre': 12, 'Cenário': 'Atual', 'Faturamento': 55200, 'Lucro': 29472},
        {'Trimestre': 15, 'Cenário': 'Atual', 'Faturamento': 58650, 'Lucro': 31344},
        {'Trimestre': 18, 'Cenário': 'Atual', 'Faturamento': 62100, 'Lucro': 33216},
        {'Trimestre': 0, 'Cenário': 'Fidelização 60%', 'Faturamento': 41400, 'Lucro': 21984},
        {'Trimestre': 3, 'Cenário': 'Fidelização 60%', 'Faturamento': 44850, 'Lucro': 23856},
        {'Trimestre': 6, 'Cenário': 'Fidelização 60%', 'Faturamento': 48300, 'Lucro': 25728},
        {'Trimestre': 9, 'Cenário': 'Fidelização 60%', 'Faturamento': 51750, 'Lucro': 27600},
        {'Trimestre': 12, 'Cenário': 'Fidelização 60%', 'Faturamento': 55200, 'Lucro': 29472},
        {'Trimestre': 15, 'Cenário': 'Fidelização 60%', 'Faturamento': 58650, 'Lucro': 31344},
        {'Trimestre': 18, 'Cenário': 'Fidelização 60%', 'Faturamento': 62100, 'Lucro': 33216},
        {'Trimestre': 0, 'Cenário': 'Ticket Médio R$75', 'Faturamento': 45000, 'Lucro': 24300},
        {'Trimestre': 3, 'Cenário': 'Ticket Médio R$75', 'Faturamento': 48750, 'Lucro': 26300},
        {'Trimestre': 6, 'Cenário': 'Ticket Médio R$75', 'Faturamento': 52500, 'Lucro': 28300},
        {'Trimestre': 9, 'Cenário': 'Ticket Médio R$75', 'Faturamento': 56250, 'Lucro': 30300},
        {'Trimestre': 12, 'Cenário': 'Ticket Médio R$75', 'Faturamento': 60000, 'Lucro': 32300},
        {'Trimestre': 15, 'Cenário': 'Ticket Médio R$75', 'Faturamento': 63750, 'Lucro': 34300},
        {'Trimestre': 18, 'Cenário': 'Ticket Médio R$75', 'Faturamento': 67500, 'Lucro': 36300},
    ])

df = carregar_dados()
cenario = st.selectbox("Selecione o Cenário", df["Cenário"].unique())
df_filtrado = df[df["Cenário"] == cenario]

col1, col2 = st.columns(2)

with col1:
    st.subheader("Faturamento por Trimestre")
    st.plotly_chart(px.bar(df_filtrado, x="Trimestre", y="Faturamento", text="Faturamento"), use_container_width=True)

with col2:
    st.subheader("Lucro Líquido por Trimestre")
    st.plotly_chart(px.line(df_filtrado, x="Trimestre", y="Lucro", markers=True), use_container_width=True)

st.subheader("📋 Tabela Completa")
st.dataframe(df_filtrado)
