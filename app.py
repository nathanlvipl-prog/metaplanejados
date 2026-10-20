import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Meta Casa - Cozinha & Closet", page_icon="🏡", layout="wide")

st.title("🏡 Meta Casa: Controle para Cozinha & Closet (Janeiro)")
st.markdown("Cada gasto ou uso de cartão reduz a margem dos **R$ 5.000,00** previstos. Vamos focar na economia com a Letícia!")

# Inicializar estado da sessão para armazenar os gastos
if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=['Data', 'Descrição', 'Categoria', 'Valor (R$)'])

# Teto / Alvo para a mobília
meta_mobilia = 5000.00

# Sidebar para registrar novos gastos ou faturas de cartão
st.sidebar.header("➕ Registrar Gasto / Cartão")
with st.sidebar.form("form_gasto"):
    data_gasto = st.date_input("Data do Gasto", datetime.date.today())
    desc_gasto = st.text_input("Descrição (Ex: Nubank, Supermercado, Loja)")
    cat_gasto = st.selectbox("Categoria", ["Cartão de Crédito", "Sobrevivência", "Consumo / Casa", "Outros"])
    valor_gasto = st.number_input("Valor (R$)", min_value=0.01, format="%.2f")
    submit = st.form_submit_button("Adicionar Lançamento")
    
    if submit:
        novo_dado = pd.DataFrame([[data_gasto, desc_gasto, cat_gasto, valor_gasto]], columns=['Data', 'Descrição', 'Categoria', 'Valor (R$)'])
        st.session_state.expenses = pd.concat([st.session_state.expenses, novo_dado], ignore_index=True)
        st.success("Lançamento adicionado com sucesso!")

# Cálculos
total_gasto = st.session_state.expenses['Valor (R$)'].sum() if not st.session_state.expenses.empty else 0.0
saldo_restante = meta_mobilia - total_gasto
percentual_progresso = min(1.0, total_gasto / meta_mobilia) if meta_mobilia > 0 else 0.0

# Métricas Principais na Tela
col1, col2, col3 = st.columns(3)
col1.metric("Orçamento Alvo (Mobília)", f"R$ {meta_mobilia:,.2f}")
col2.metric("Total Acumulado de Gastos", f"R$ {total_gasto:,.2f}", delta=f"-R$ {total_gasto:,.2f}", delta_color="inverse")
col3.metric("Margem Restante da Meta", f"R$ {saldo_restante:,.2f}")

# Barra de Progresso visual para incentivar a economia
st.progress(percentual_progresso, text=f"Comprometimento do teto: {percentual_progresso*100:.1f}%")

if total_gargo_atingido := (total_gasto >= meta_mobilia):
    st.error("🚨 Atenção! Os gastos atingiram ou ultrapassaram o teto estipulado para a mobília!")
else:
    st.info(f"💡 Faltam R$ {saldo_restante:,.2f} de margem para mantermos o projeto da cozinha e do closet blindado em janeiro.")

# Tabela de Extrato dos Lançamentos
st.subheader("📋 Extrato de Gastos e Cartões")
if not st.session_state.expenses.empty:
    st.dataframe(st.session_state.expenses, use_container_width=True)
    
    if st.button("🗑️ Limpar Todos os Registros"):
        st.session_state.expenses = pd.DataFrame(columns=['Data', 'Descrição', 'Categoria', 'Valor (R$)'])
        st.rerun()
else:
    st.info("Nenhum gasto lançado ainda neste ciclo. Use o menu lateral para começar a registrar.")