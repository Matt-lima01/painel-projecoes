import streamlit as st
import pandas as pd

st.set_page_config(page_title="Painel de Gestão da Pizzaria", layout="wide")
st.title("🍕 Painel Central de Gestão - Pizzaria Estilo Pizza Prime")

# Navegação
aba = st.sidebar.radio("Navegação", [
    "Dados da Pizzaria",
    "Equipe",
    "Produtos e CMV",
    "Financeiro",
    "Projeções"
])

# Sessões salvas
if "funcionarios" not in st.session_state:
    st.session_state["funcionarios"] = []
if "produtos" not in st.session_state:
    st.session_state["produtos"] = []
if "financeiro" not in st.session_state:
    st.session_state["financeiro"] = {"ticket": 69, "pedidos": 600, "fixo": 1200}

# Aba 1: Dados da Pizzaria
if aba == "Dados da Pizzaria":
    st.header("📍 Informações da Pizzaria")
    nome = st.text_input("Nome da Pizzaria", "Du-Nada Pizzaria")
    endereco = st.text_input("Endereço", "Tv. Tancredo Neves - Cabanagem")
    tipo = st.selectbox("Tipo de operação", ["Delivery", "Salão", "Ambos"])
    st.success(f"{nome} cadastrada como operação '{tipo}' em {endereco}.")

# Aba 2: Equipe
if aba == "Equipe":
    st.header("👨‍🍳 Cadastro de Funcionários")
    with st.form("cad_func"):
        nome = st.text_input("Nome do Funcionário")
        cargo = st.selectbox("Cargo", ["Pizzaiolo", "Atendente", "Entregador", "Gerente"])
        salario = st.number_input("Salário", min_value=0.0, step=100.0)
        bonus = st.number_input("Bônus Variável", min_value=0.0, step=50.0)
        enviar = st.form_submit_button("Cadastrar")
        if enviar:
            st.session_state["funcionarios"].append({
                "Nome": nome, "Cargo": cargo, "Salário": salario, "Bônus": bonus
            })
            st.success("Funcionário cadastrado com sucesso!")
    st.subheader("Equipe Atual")
    st.dataframe(pd.DataFrame(st.session_state["funcionarios"]))

# Aba 3: Produtos e CMV
if aba == "Produtos e CMV":
    st.header("📦 Cadastro de Produtos e Cálculo de CMV")
    with st.form("cad_prod"):
        nome = st.text_input("Produto")
        preco = st.number_input("Preço de Venda", min_value=0.0, step=1.0)
        custo = st.number_input("Custo dos Ingredientes", min_value=0.0, step=1.0)
        add = st.form_submit_button("Adicionar")
        if add:
            cmv = (custo / preco) * 100 if preco > 0 else 0
            st.session_state["produtos"].append({
                "Produto": nome, "Preço": preco, "Custo": custo, "CMV (%)": round(cmv, 2)
            })
            st.success("Produto adicionado com sucesso!")
    st.subheader("Cardápio e CMV")
    st.dataframe(pd.DataFrame(st.session_state["produtos"]))

# Aba 4: Financeiro
if aba == "Financeiro":
    st.header("💰 Dados Financeiros")
    ticket = st.number_input("Ticket Médio (R$)", value=st.session_state["financeiro"]["ticket"])
    pedidos = st.number_input("Pedidos por mês", value=st.session_state["financeiro"]["pedidos"])
    fixo = st.number_input("Custo Fixo Mensal (R$)", value=st.session_state["financeiro"]["fixo"])
    st.session_state["financeiro"] = {"ticket": ticket, "pedidos": pedidos, "fixo": fixo}
    receita = ticket * pedidos
    lucro_bruto = receita * 0.56
    lucro_liquido = lucro_bruto - fixo
    st.metric("Faturamento Mensal", f"R${receita:.2f}")
    st.metric("Lucro Bruto (CMV 44%)", f"R${lucro_bruto:.2f}")
    st.metric("Lucro Líquido", f"R${lucro_liquido:.2f}")

# Aba 5: Projeções
if aba == "Projeções":
    st.header("📈 Simulador Estratégico")
    aumento_pct = st.slider("Aumento nas vendas (%)", 0, 50, 10)
    fidel_pct = st.slider("Fidelização de clientes (%)", 48, 80, 55)
    base = st.session_state["financeiro"]
    receita_proj = base["ticket"] * base["pedidos"] * (1 + aumento_pct / 100)
    lucro_proj = receita_proj * (1 - 0.44) - base["fixo"]
    st.subheader("Resultados Simulados")
    st.metric("Nova Receita", f"R${receita_proj:.2f}")
    st.metric("Lucro Projetado", f"R${lucro_proj:.2f}")
    st.write(f"Com {fidel_pct}% de clientes recorrentes e {aumento_pct}% de vendas a mais.")