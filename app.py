
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="ERP Du-Nada", layout="wide")

# Menu lateral
st.sidebar.image("https://img.icons8.com/color/96/pizza.png", width=70)
st.sidebar.markdown("## Du-Nada Pizzaria")
menu = st.sidebar.radio("Menu", [
    "Dashboard",
    "Produtos",
    "Estoque",
    "Vendas",
    "Funcionários",
    "Simulador",
    "Financeiro"
])

# Inicializar dados
for var in ["produtos", "insumos", "vendas", "funcionarios"]:
    if var not in st.session_state:
        st.session_state[var] = []

# Dashboard
if menu == "Dashboard":
    st.title("📊 Dashboard Geral")
    vendas = pd.DataFrame(st.session_state.vendas)
    if not vendas.empty:
        receita = vendas["Valor"].sum()
        custo = vendas["Custo"].sum()
        lucro = receita - custo
        cmv = (custo / receita) * 100 if receita > 0 else 0
        color = "green" if cmv < 35 else "orange" if cmv < 50 else "red"
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Faturamento", f"R$ {receita:,.2f}")
        col2.metric("Lucro Bruto", f"R$ {lucro:,.2f}")
        col3.metric("Ticket Médio", f"R$ {receita / len(vendas):,.2f}")
        col4.markdown(f"<h3 style='color:{color}'>CMV: {cmv:.2f}%</h3>", unsafe_allow_html=True)
    else:
        st.info("Registre vendas para visualizar os indicadores.")

# Produtos
elif menu == "Produtos":
    st.title("🍕 Cadastro de Produtos")
    with st.form("form_produto"):
        nome = st.text_input("Nome")
        preco = st.number_input("Preço", 0.0)
        ingredientes = st.multiselect("Ingredientes", [i["Ingrediente"] for i in st.session_state.insumos])
        custo_total = 0
        for i in ingredientes:
            ing = next(x for x in st.session_state.insumos if x["Ingrediente"] == i)
            qtd = st.number_input(f"{i} ({ing['Unidade']})", 0.0, key=i)
            custo_total += qtd * ing["Preço Unit"]
        if st.form_submit_button("Salvar"):
            cmv = (custo_total / preco) * 100 if preco > 0 else 0
            st.session_state.produtos.append({
                "Produto": nome, "Preço": preco, "Custo": custo_total, "CMV": cmv
            })
            st.success("Produto cadastrado!")
    st.dataframe(pd.DataFrame(st.session_state.produtos))

# Estoque
elif menu == "Estoque":
    st.title("📦 Estoque")
    with st.form("form_estoque"):
        nome = st.text_input("Ingrediente")
        unidade = st.selectbox("Unidade", ["kg", "litro", "unid", "pacote"])
        preco_unit = st.number_input("Preço Unit", 0.0)
        if st.form_submit_button("Adicionar"):
            st.session_state.insumos.append({"Ingrediente": nome, "Unidade": unidade, "Preço Unit": preco_unit})
            st.success("Insumo cadastrado!")
    st.dataframe(pd.DataFrame(st.session_state.insumos))

# Vendas
elif menu == "Vendas":
    st.title("🧾 Registro de Vendas")
    produtos = pd.DataFrame(st.session_state.produtos)
    if produtos.empty:
        st.warning("Cadastre produtos primeiro.")
    else:
        with st.form("form_venda"):
            nome = st.selectbox("Produto Vendido", produtos["Produto"])
            item = produtos[produtos["Produto"] == nome].iloc[0]
            if st.form_submit_button("Registrar Venda"):
                st.session_state.vendas.append({
                    "Produto": nome, "Valor": item["Preço"], "Custo": item["Custo"]
                })
                st.success("Venda registrada.")
    st.dataframe(pd.DataFrame(st.session_state.vendas))

# Funcionários
elif menu == "Funcionários":
    st.title("👥 Equipe da Pizzaria")
    with st.form("form_func"):
        nome = st.text_input("Nome")
        cargo = st.selectbox("Cargo", ["Pizzaiolo", "Atendente", "Entregador", "Gerente"])
        salario = st.number_input("Salário Mensal", 0.0)
        bonus = st.number_input("Bônus", 0.0)
        if st.form_submit_button("Cadastrar"):
            st.session_state.funcionarios.append({
                "Nome": nome, "Cargo": cargo, "Salário": salario, "Bônus": bonus
            })
            st.success("Funcionário cadastrado.")
    st.dataframe(pd.DataFrame(st.session_state.funcionarios))

# Simulador
elif menu == "Simulador":
    st.title("📈 Simulador")
    pct = st.slider("Crescimento (%)", 0, 100, 20)
    vendas = pd.DataFrame(st.session_state.vendas)
    if not vendas.empty:
        receita = vendas["Valor"].sum()
        nova = receita * (1 + pct / 100)
        st.metric("Atual", f"R$ {receita:,.2f}")
        st.metric("Projetado", f"R$ {nova:,.2f}")
    else:
        st.info("Sem vendas registradas.")

# Financeiro
elif menu == "Financeiro":
    st.title("💰 Financeiro")
    vendas = pd.DataFrame(st.session_state.vendas)
    folha = sum([f["Salário"] + f["Bônus"] for f in st.session_state.funcionarios])
    if not vendas.empty:
        receita = vendas["Valor"].sum()
        custo = vendas["Custo"].sum()
        lucro = receita - custo - folha
        col1, col2, col3 = st.columns(3)
        col1.metric("Receita", f"R$ {receita:,.2f}")
        col2.metric("Custos", f"R$ {custo + folha:,.2f}")
        col3.metric("Lucro Líquido", f"R$ {lucro:,.2f}")
    else:
        st.info("Sem dados financeiros.")
