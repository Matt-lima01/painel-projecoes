
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="ERP Du-Nada", layout="wide")

# Sidebar
st.sidebar.image("https://img.icons8.com/color/96/pizza.png", width=70)
st.sidebar.markdown("## Du-Nada Pizzaria")
menu = st.sidebar.radio("Menu", [
    "Dashboard",
    "Produtos e Ficha Técnica",
    "Estoque",
    "Registrar Venda",
    "Simulador",
    "Financeiro"
])

# Sessões
if "insumos" not in st.session_state:
    st.session_state.insumos = []
if "produtos" not in st.session_state:
    st.session_state.produtos = []
if "vendas" not in st.session_state:
    st.session_state.vendas = []

# Dashboard
if menu == "Dashboard":
    st.title("📊 Visão Geral da Pizzaria")
    vendas = pd.DataFrame(st.session_state.vendas)
    if not vendas.empty:
        total_receita = vendas["Valor"].sum()
        total_cmv = vendas["Custo"].sum()
        lucro = total_receita - total_cmv
        ticket = total_receita / len(vendas) if len(vendas) > 0 else 0

        st.metric("Faturamento", f"R$ {total_receita:.2f}")
        st.metric("Lucro Bruto", f"R$ {lucro:.2f}")
        st.metric("Ticket Médio", f"R$ {ticket:.2f}")

        st.subheader("Vendas por Produto")
        fig = px.bar(vendas.groupby("Produto")["Valor"].sum().reset_index(), x="Produto", y="Valor")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Sem vendas registradas ainda.")

# Produtos e Ficha Técnica
elif menu == "Produtos e Ficha Técnica":
    st.title("🍕 Cadastro de Produtos com Ficha Técnica")
    insumos_nomes = [i["Ingrediente"] for i in st.session_state.insumos]
    with st.form("produto_form"):
        nome = st.text_input("Nome do Produto")
        preco = st.number_input("Preço de Venda", 0.0)
        ingredientes = st.multiselect("Ingredientes", options=insumos_nomes)
        custo_total = 0
        for i in ingredientes:
            ing = next(item for item in st.session_state.insumos if item["Ingrediente"] == i)
            qtd = st.number_input(f"Qtd usada de {i} ({ing['Unidade']})", 0.0, key=i)
            custo_total += qtd * ing["Preço Unit"]
        cadastrar = st.form_submit_button("Cadastrar Produto")
        if cadastrar:
            cmv = (custo_total / preco) * 100 if preco > 0 else 0
            st.session_state.produtos.append({"Produto": nome, "Preço": preco, "Custo": round(custo_total, 2), "CMV (%)": round(cmv, 2)})
            st.success("Produto cadastrado!")
    st.subheader("Produtos Cadastrados")
    st.dataframe(pd.DataFrame(st.session_state.produtos))

# Estoque
elif menu == "Estoque":
    st.title("📦 Controle de Estoque")
    with st.form("estoque_form"):
        nome = st.text_input("Nome do Ingrediente")
        unidade = st.selectbox("Unidade", ["kg", "litro", "unid", "pacote"])
        preco_unit = st.number_input("Preço Unitário", 0.0)
        cadastrar = st.form_submit_button("Cadastrar Insumo")
        if cadastrar:
            st.session_state.insumos.append({"Ingrediente": nome, "Unidade": unidade, "Preço Unit": preco_unit})
            st.success("Insumo cadastrado!")
    st.dataframe(pd.DataFrame(st.session_state.insumos))

# Registrar Venda
elif menu == "Registrar Venda":
    st.title("🧾 Registro de Venda")
    produtos = pd.DataFrame(st.session_state.produtos)
    if produtos.empty:
        st.warning("Cadastre produtos primeiro.")
    else:
        with st.form("venda_form"):
            produto_nome = st.selectbox("Produto Vendido", produtos["Produto"].tolist())
            produto = produtos[produtos["Produto"] == produto_nome].iloc[0]
            registrar = st.form_submit_button("Registrar Venda")
            if registrar:
                st.session_state.vendas.append({
                    "Produto": produto_nome,
                    "Valor": produto["Preço"],
                    "Custo": produto["Custo"]
                })
                st.success("Venda registrada!")
    st.dataframe(pd.DataFrame(st.session_state.vendas))

# Simulador
elif menu == "Simulador":
    st.title("📈 Simulador Estratégico")
    pct = st.slider("Aumento esperado de vendas (%)", 0, 100, 10)
    vendas = pd.DataFrame(st.session_state.vendas)
    if not vendas.empty:
        receita = vendas["Valor"].sum()
        nova = receita * (1 + pct / 100)
        st.metric("Receita Atual", f"R$ {receita:.2f}")
        st.metric("Receita com Crescimento", f"R$ {nova:.2f}")
    else:
        st.info("Registre vendas para simular.")

# Financeiro
elif menu == "Financeiro":
    st.title("💰 Visão Financeira")
    vendas = pd.DataFrame(st.session_state.vendas)
    if not vendas.empty:
        receita = vendas["Valor"].sum()
        custo = vendas["Custo"].sum()
        lucro = receita - custo
        st.metric("Receita Total", f"R$ {receita:.2f}")
        st.metric("Custo Total", f"R$ {custo:.2f}")
        st.metric("Lucro Bruto", f"R$ {lucro:.2f}")
    else:
        st.info("Sem dados financeiros.")
