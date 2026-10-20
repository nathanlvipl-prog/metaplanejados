import streamlit as st
import pandas as pd
import datetime

st.set_page_config(
    page_title="Meta Casa - Fluxo de Caixa & Mobília",
    page_icon="🏠",
    layout="wide"
)

# Inicializar estado das variáveis
if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=['Data', 'Descrição', 'Categoria', 'Valor (R$)'])

if 'renda_base' not in st.session_state:
    st.session_state.renda_base = 7000.00

if 'saidas_base' not in st.session_state:
    st.session_state.saidas_base = 6000.00

if 'saldo_anterior' not in st.session_state:
    st.session_state.saldo_anterior = 0.00

st.title("🏠 Meta Casa: Fluxo de Caixa & Mobília")
st.subheader("🎯 Cozinha Planejada e Closet (Janeiro)")

# Barra Lateral para Configurações e Lançamentos
st.sidebar.header("⚙️ Planejamento Base do Mês")
st.session_state.renda_base = st.sidebar.number_input("Entradas Previstas (R$)", value=st.session_state.renda_base, step=100.00, format="%.2f")
st.session_state.saidas_base = st.sidebar.number_input("Contas Fixas Previstas (R$)", value=st.session_state.saidas_base, step=100.00, format="%.2f")
st.session_state.saldo_anterior = st.sidebar.number_input("Saldo Acumulado de Meses Anteriores (R$)", value=st.session_state.saldo_anterior, step=50.00, format="%.2f")

st.sidebar.divider()
st.sidebar.header("➕ Registrar Gasto / Cartão")
with st.sidebar.form("form_gasto", clear_on_submit=True):
    data_gasto = st.date_input("Data", datetime.date.today())
    desc_gasto = st.text_input("Descrição", placeholder="Ex: Fatura Cartão, Supermercado...")
    cat_gasto = st.selectbox("Categoria", ["Cartão de Crédito", "Alimentação", "Casa / Consumo", "Outros"])
    valor_gasto = st.number_input("Valor (R$)", min_value=0.01, step=10.00, format="%.2f")
    submit = st.form_submit_button("Adicionar Gasto", use_container_width=True)
    
    if submit:
        if desc_gasto.strip() == "":
            st.sidebar.error("Informe a descrição do gasto.")
        else:
            novo = pd.DataFrame([[data_gasto, desc_gasto, cat_gasto, valor_gasto]], columns=['Data', 'Descrição', 'Categoria', 'Valor (R$)'])
            st.session_state.expenses = pd.concat([st.session_state.expenses, novo], ignore_index=True)
            st.sidebar.success("Gasto adicionado e descontado!")

# Cálculos do Fluxo
total_gastos_extras = st.session_state.expenses['Valor (R$)'].sum() if not st.session_state.expenses.empty else 0.0
total_saidas_geral = st.session_state.saidas_base + total_gastos_extras
sobra_mes = st.session_state.renda_base - total_saidas_geral
saldo_total_acumulado = st.session_state.saldo_anterior + sobra_mes
meta_mobilia = 5000.00
progresso_mobilia = min(1.0, max(0.0, saldo_total_acumulado / meta_mobilia)) if meta_mobilia > 0 else 0.0

# Exibição de Métricas Principais na Tela
col1, col2, col3, col4 = st.columns(4)
col1.metric("📥 Entradas Previstas", f"R$ {st.session_state.renda_base:,.2f}")
col2.metric("📤 Total de Saídas", f"R$ {total_saidas_geral:,.2f}", delta=f"-R$ {total_gastos_extras:,.2f} em extras", delta_color="inverse")
col3.metric("💰 Sobra do Mês Atual", f"R$ {sobra_mes:,.2f}", delta="Meta de economia")
col4.metric("🌟 Saldo Acumulado Total", f"R$ {saldo_total_acumulado:,.2f}")

st.divider()

# Barra de Progresso e Alvo da Mobília
st.subheader("🔨 Fundo para Cozinha Planejada & Closet (Meta: R$ 5.000,00)")
st.progress(progresso_mobilia, text=f"Progresso do Fundo de Mobília: R$ {saldo_total_acumulado:,.2f} de R$ {meta_mobilia:,.2f} ({progresso_mobilia*100:.1f}%)")

if saldo_total_acumulado >= meta_mobilia:
    st.success("🎉 Excelente! O saldo acumulado já cobre totalmente a compra da cozinha e do closet em janeiro!")
elif saldo_total_acumulado > 0:
    falta_meta = meta_mobilia - saldo_total_acumulado
    st.info(f"💡 Faltam **R$ {falta_meta:,.2f}** acumulados para atingir o teto de R$ 5.000,00. Cada gasto extra reduz essa sobra!")
else:
    st.warning("⚠️ Atenção: As saídas do mês ultrapassaram as entradas. É preciso segurar os gastos para construir o saldo da mobília!")

st.divider()

# Tabela Detalhada de Extrato
st.subheader("📋 Lançamentos e Gastos Extras do Mês")
if not st.session_state.expenses.empty:
    st.dataframe(
        st.session_state.expenses,
        use_container_width=True,
        column_config={
            "Data": st.column_config.DateColumn("Data", format="DD/MM/YYYY"),
            "Valor (R$)": st.column_config.NumberColumn("Valor (R$)", format="R$ %.2f")
        }
    )
    if st.button("🗑️ Limpar Todos os Gastos Registrados"):
        st.session_state.expenses = pd.DataFrame(columns=['Data', 'Descrição', 'Categoria', 'Valor (R$)'])
        st.rerun()
else:
    st.caption("Nenhum gasto extra registrado neste mês. Utilize o painel à esquerda para lançar os cartões e despesas diárias.")
