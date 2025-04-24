
# Estrutura completa do Painel ERP Profissional - Du-Nada Pizzaria

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="ERP Du-Nada Pizzaria", layout="wide")

# Sidebar com logo e menu
st.sidebar.image("https://img.icons8.com/color/96/pizza.png", width=70)
st.sidebar.title("Du-Nada Pizzaria")
menu = st.sidebar.radio("Menu", [
    "Dashboard Geral",
    "Produtos e Ficha Técnica",
    "Estoque",
    "Equipe",
    "Clientes",
    "Simuladores",
    "Financeiro"
])

# Sessões para armazenar dados temporários
if "produtos" not in st.session_state:
    st.session_state.produtos = []
if "insumos" not in st.session_state:
    st.session_state.insumos = []
if "clientes" not in st.session_state:
    st.session_state.clientes = []
if "funcionarios" not in st.session_state:
    st.session_state.funcionarios = []

# Dashboard Geral
if menu == "Dashboard Geral":
    st.title("📊 Visão Geral do Negócio")
    receita = sum([p['Preço'] for p in st.session_state.produtos])
    custo = sum([p['Custo'] for p in st.session_state.produtos])
    cmv = (custo / receita) * 100 if receita > 0 else 0
    lucro = receita - custo

    st.metric("Faturamento Estimado", f"R$ {receita:,.2f}")
    st.metric("Lucro Bruto Estimado", f"R$ {lucro:,.2f}")
    st.metric("CMV Global", f"{cmv:.2f}%")

    fig = px.pie(values=[52, 48], names=["Novos Clientes", "Recorrentes"], title="Origem das Vendas")
    st.plotly_chart(fig, use_container_width=True)

# Produtos e Ficha Técnica
elif menu == "Produtos e Ficha Técnica":
    st.title("🍕 Cadastro de Produtos e CMV")
    with st.form("form_produto"):
        nome = st.text_input("Nome do Produto")
        preco = st.number_input("Preço de Venda", min_value=0.0, step=0.1)
        custo = st.number_input("Custo Total de Insumos", min_value=0.0, step=0.1)
        cadastrar = st.form_submit_button("Cadastrar")
        if cadastrar:
            cmv = (custo / preco) * 100 if preco > 0 else 0
            st.session_state.produtos.append({"Produto": nome, "Preço": preco, "Custo": custo, "CMV": round(cmv, 2)})
            st.success("Produto cadastrado com sucesso!")
    st.dataframe(pd.DataFrame(st.session_state.produtos))

# Estoque
elif menu == "Estoque":
    st.title("📦 Controle de Estoque")
    with st.form("form_estoque"):
        ingrediente = st.text_input("Nome do Ingrediente")
        unidade = st.selectbox("Unidade", ["kg", "litro", "unid", "pacote"])
        preco_unit = st.number_input("Preço Unitário", min_value=0.0)
        quantidade = st.number_input("Quantidade em Estoque", min_value=0.0)
        adicionar = st.form_submit_button("Adicionar")
        if adicionar:
            st.session_state.insumos.append({"Ingrediente": ingrediente, "Unidade": unidade, "Preço Unit": preco_unit, "Qtd": quantidade})
            st.success("Ingrediente adicionado!")
    st.dataframe(pd.DataFrame(st.session_state.insumos))

# Equipe
elif menu == "Equipe":
    st.title("👥 Equipe da Pizzaria")
    with st.form("form_func"):
        nome = st.text_input("Nome do Funcionário")
        cargo = st.selectbox("Cargo", ["Pizzaiolo", "Atendente", "Entregador", "Gerente"])
        salario = st.number_input("Salário Mensal", min_value=0.0)
        bonus = st.number_input("Bônus Mensal", min_value=0.0)
        cadastrar = st.form_submit_button("Cadastrar Funcionário")
        if cadastrar:
            st.session_state.funcionarios.append({"Nome": nome, "Cargo": cargo, "Salário": salario, "Bônus": bonus})
            st.success("Funcionário cadastrado!")
    st.dataframe(pd.DataFrame(st.session_state.funcionarios))

# Clientes
elif menu == "Clientes":
    st.title("📇 Gestão de Clientes e Fidelização")
    with st.form("form_cliente"):
        nome = st.text_input("Nome do Cliente")
        recorrente = st.checkbox("É cliente recorrente?")
        cadastrar = st.form_submit_button("Cadastrar Cliente")
        if cadastrar:
            st.session_state.clientes.append({"Nome": nome, "Recorrente": recorrente})
            st.success("Cliente cadastrado!")
    st.dataframe(pd.DataFrame(st.session_state.clientes))

# Simuladores
elif menu == "Simuladores":
    st.title("📈 Simulador Estratégico")
    aumento = st.slider("Aumento estimado de vendas (%)", 0, 50, 10)
    fidel = st.slider("Fidelização prevista (%)", 48, 80, 52)
    receita_atual = sum([p['Preço'] for p in st.session_state.produtos])
    nova_receita = receita_atual * (1 + aumento / 100)
    lucro = nova_receita * 0.56
    st.metric("Nova Receita Estimada", f"R$ {nova_receita:,.2f}")
    st.metric("Lucro Estimado", f"R$ {lucro:,.2f}")
    st.metric("Clientes Recorrentes", f"{fidel}%")

# Financeiro
elif menu == "Financeiro":
    st.title("💰 Painel Financeiro Completo")
    receita = sum([p['Preço'] for p in st.session_state.produtos])
    custo = sum([p['Custo'] for p in st.session_state.produtos])
    folha = sum([f['Salário'] + f['Bônus'] for f in st.session_state.funcionarios])
    despesas_fixas = folha + 1200  # exemplo com R$1200 fixos
    lucro_liquido = receita - custo - despesas_fixas

    col1, col2, col3 = st.columns(3)
    col1.metric("Receita Total", f"R$ {receita:,.2f}")
    col2.metric("Custos Totais", f"R$ {custo + despesas_fixas:,.2f}")
    col3.metric("Lucro Líquido", f"R$ {lucro_liquido:,.2f}")
