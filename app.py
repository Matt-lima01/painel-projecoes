
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="ERP Du-Nada", layout="wide")

# Menu lateral com identidade da marca
st.sidebar.image("https://img.icons8.com/color/96/pizza.png", width=70)
st.sidebar.markdown("## Du-Nada Pizzaria")
menu = st.sidebar.radio("Menu", [
    "Dashboard",
    "Produtos",
    "Estoque",
    "Vendas",
    "Simulador",
    "Financeiro"
])

# Inicialização dos dados
if "produtos" not in st.session_state: st.session_state.produtos = []
if "insumos" not in st.session_state: st.session_state.insumos = []
if "vendas" not in st.session_state: st.session_state.vendas = []

# Dashboard
if menu == "Dashboard":
    st.title("📊 Dashboard Geral")
    vendas = pd.DataFrame(st.session_state.vendas)
    if not vendas.empty:
        receita = vendas["Valor"].sum()
        custo = vendas["Custo"].sum()
        lucro = receita - custo
        ticket = receita / len(vendas)
        cmv = (custo / receita) * 100
        st.metric("Faturamento", f"R$ {receita:,.2f}")
        st.metric("Lucro Bruto", f"R$ {lucro:,.2f}")
        st.metric("Ticket Médio", f"R$ {ticket:,.2f}")
        st.metric("CMV Global", f"{cmv:.2f}%")
    else:
        st.info("Registre vendas para visualizar os indicadores.")

# Produtos
elif menu == "Produtos":
    st.title("🍕 Cadastro de Produtos e Ficha Técnica")
    with st.form("produto_form"):
        nome = st.text_input("Nome do Produto")
        preco = st.number_input("Preço de Venda", 0.0)
        ingredientes = st.multiselect("Ingredientes", [i["Ingrediente"] for i in st.session_state.insumos])
        custo_total = 0
        for i in ingredientes:
            ing = next(x for x in st.session_state.insumos if x["Ingrediente"] == i)
            qtd = st.number_input(f"Qtd de {i} ({ing['Unidade']})", 0.0, key=i)
            custo_total += qtd * ing["Preço Unit"]
        if st.form_submit_button("Cadastrar Produto"):
            cmv = (custo_total / preco) * 100 if preco > 0 else 0
            st.session_state.produtos.append({
                "Produto": nome, "Preço": preco, "Custo": round(custo_total, 2), "CMV": round(cmv, 2)
            })
            st.success("Produto cadastrado com sucesso.")
    st.dataframe(pd.DataFrame(st.session_state.produtos))

# Estoque
elif menu == "Estoque":
    st.title("📦 Controle de Estoque")
    with st.form("insumo_form"):
        nome = st.text_input("Ingrediente")
        unidade = st.selectbox("Unidade", ["kg", "litro", "unid", "pacote"])
        preco_unit = st.number_input("Preço Unitário", 0.0)
        if st.form_submit_button("Cadastrar Insumo"):
            st.session_state.insumos.append({
                "Ingrediente": nome, "Unidade": unidade, "Preço Unit": preco_unit
            })
            st.success("Ingrediente adicionado.")
    st.dataframe(pd.DataFrame(st.session_state.insumos))

# Vendas
elif menu == "Vendas":
    st.title("🧾 Registro de Vendas")
    produtos = pd.DataFrame(st.session_state.produtos)
    if produtos.empty:
        st.warning("Cadastre produtos antes de registrar vendas.")
    else:
        with st.form("venda_form"):
            nome = st.selectbox("Produto", produtos["Produto"])
            item = produtos[produtos["Produto"] == nome].iloc[0]
            if st.form_submit_button("Registrar Venda"):
                st.session_state.vendas.append({
                    "Produto": nome,
                    "Valor": item["Preço"],
                    "Custo": item["Custo"]
                })
                st.success("Venda registrada com sucesso.")
    st.dataframe(pd.DataFrame(st.session_state.vendas))

# Simulador
elif menu == "Simulador":
    st.title("📈 Simulador de Crescimento")
    pct = st.slider("Aumento de vendas (%)", 0, 100, 20)
    vendas = pd.DataFrame(st.session_state.vendas)
    if not vendas.empty:
        receita = vendas["Valor"].sum()
        lucro = receita - vendas["Custo"].sum()
        nova_receita = receita * (1 + pct / 100)
        novo_lucro = lucro * (1 + pct / 100)
        st.metric("Receita Atual", f"R$ {receita:,.2f}")
        st.metric("Receita Projetada", f"R$ {nova_receita:,.2f}")
        st.metric("Lucro Projetado", f"R$ {novo_lucro:,.2f}")
    else:
        st.info("Registre vendas para usar o simulador.")

# Financeiro
elif menu == "Financeiro":
    st.title("💰 Painel Financeiro")
    vendas = pd.DataFrame(st.session_state.vendas)
    if not vendas.empty:
        receita = vendas["Valor"].sum()
        custo = vendas["Custo"].sum()
        despesas_fixas = 3200
        lucro_bruto = receita - custo
        lucro_liquido = lucro_bruto - despesas_fixas
        st.metric("Receita Total", f"R$ {receita:,.2f}")
        st.metric("CMV Total", f"R$ {custo:,.2f}")
        st.metric("Despesas Fixas", f"R$ {despesas_fixas:,.2f}")
        st.metric("Lucro Líquido", f"R$ {lucro_liquido:,.2f}")
    else:
        st.info("Sem dados financeiros ainda.")
