import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gestão Pizzaria - CMV Inteligente", layout="wide")
st.title("📊 Painel de Gestão com CMV Inteligente")

aba = st.sidebar.radio("Navegação", [
    "Insumos",
    "Produtos e CMV",
    "CMV Global",
])

# Sessões
if "insumos" not in st.session_state:
    st.session_state["insumos"] = []

if "produtos" not in st.session_state:
    st.session_state["produtos"] = []

# Insumos
if aba == "Insumos":
    st.header("📦 Cadastro de Insumos")
    with st.form("form_insumo"):
        nome = st.text_input("Nome do Ingrediente")
        preco_unit = st.number_input("Preço por unidade (R$)", min_value=0.0, step=0.1)
        unidade = st.selectbox("Unidade", ["kg", "litro", "unid", "pacote"])
        adicionar = st.form_submit_button("Cadastrar Insumo")
        if adicionar:
            st.session_state["insumos"].append({
                "Ingrediente": nome, "Preço Unitário": preco_unit, "Unidade": unidade
            })
            st.success("Insumo cadastrado!")
    st.subheader("Insumos Cadastrados")
    st.dataframe(pd.DataFrame(st.session_state["insumos"]))

# Produtos e CMV
if aba == "Produtos e CMV":
    st.header("🍕 Cadastro de Produtos com Custo")
    insumos = [i["Ingrediente"] for i in st.session_state["insumos"]]
    with st.form("form_produto"):
        nome_produto = st.text_input("Nome do Produto")
        preco_venda = st.number_input("Preço de Venda", min_value=0.0)
        custo_total = st.number_input("Custo Total (soma dos insumos usados)", min_value=0.0)
        cadastrar = st.form_submit_button("Cadastrar Produto")
        if cadastrar:
            cmv = (custo_total / preco_venda) * 100 if preco_venda > 0 else 0
            st.session_state["produtos"].append({
                "Produto": nome_produto,
                "Preço de Venda": preco_venda,
                "Custo Total": custo_total,
                "CMV (%)": round(cmv, 2)
            })
            st.success("Produto cadastrado!")
    st.subheader("Cardápio com CMV")
    st.dataframe(pd.DataFrame(st.session_state["produtos"]))

# CMV Global
if aba == "CMV Global":
    st.header("📈 Diagnóstico do CMV Global")
    produtos = pd.DataFrame(st.session_state["produtos"])
    if not produtos.empty:
        receita_total = produtos["Preço de Venda"].sum()
        custo_total = produtos["Custo Total"].sum()
        cmv_global = (custo_total / receita_total) * 100 if receita_total > 0 else 0

        if cmv_global <= 35:
            cor = "green"
            status = "Excelente"
        elif cmv_global <= 44:
            cor = "orange"
            status = "Atenção"
        else:
            cor = "red"
            status = "Alerta"

        st.markdown(f"<h2 style='color:{cor}'>CMV Global: {cmv_global:.2f}% - {status}</h2>", unsafe_allow_html=True)
        st.metric("Receita Total", f"R${receita_total:.2f}")
        st.metric("Custo Total", f"R${custo_total:.2f}")
    else:
        st.info("Cadastre produtos primeiro para calcular o CMV.")