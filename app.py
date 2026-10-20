import streamlit as st
import pandas as pd
import datetime

# Configuração da página com layout limpo e moderno
st.set_page_config(
    page_title="Meta Casa - Cozinha & Closet",
    page_icon="🏠",
    layout="wide"
)

# Estilização CSS para cartões e métricas
st.markdown("""
    <style>
    .stMetric {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #2e7d32;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .stProgress > div > div > div > div {
        background-color: #2e7d32;
    }
    </style>
""", unsafe_allow_html=True)

# Título Principal e Subtítulo
st.title("🏠 Meta Casa: Planejados 2027")
st.subheader("🎯 Em busca da cozinha planejada e do closet")

st.markdown("Cada gasto lançado reduz diretamente a margem dos **R$ 5.000,00** estipulados para a meta.")

# Inicializar estado dos lançamentos
if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=['Data', 'Descrição', 'Categoria', 'Valor (R$)'])

meta_total = 5000.00

# Sidebar - Form de Cadastro
st.sidebar.header("➕ Registrar Novo Gasto")
with st.sidebar.form("form_gasto", clear_on_submit=True):
    data_gasto = st.date_input("Data do Gasto", datetime.date.today())
    desc_gasto = st.text_input("Descrição do Gasto", placeholder="Ex: Fatura Nubank, Feira, Material...")
    cat_gasto = st.selectbox("Categoria", ["Cartão de Crédito", "Alimentação & Feira", "Casa / Consumo", "Outros Gastos"])
    valor_gasto = st.number_input("Valor (R$)", min_value=0.01, step=10.0, format="%.2f")
    
    submit = st.form_submit_button(" Confirmar Lançamento", use_container_width=True)
    
    if submit:
        if desc_gasto.strip() == "":
            st.sidebar.error("Por favor, informe a descrição do gasto.")
        else:
            novo_registro = pd.DataFrame([[data_gasto, desc_gasto, cat_gasto, valor_gasto]], columns=['Data', 'Descrição', 'Categoria', 'Valor (R$)'])
            st.session_state.expenses = pd.concat([st.session_state.expenses, novo_registro], ignore_index=True)
            st.sidebar.success("Lançamento adicionado!")

# Cálculos do Dashboard
total_gasto = st.session_state.expenses['Valor (R$)'].sum() if not st.session_state.expenses.empty else 0.0
saldo_restante = meta_total - total_gasto
percentual_usado = min(1.0, total_gasto / meta_total) if meta_total > 0 else 0.0

st.divider()

# Métricas Visuais (Cards)
col1, col2, col3 = st.columns(3)
col1.metric("📌 Orçamento Meta", f"R$ {meta_total:,.2f}")
col2.metric("💸 Total Gastos", f"R$ {total_gasto:,.2f}", delta=f"-R$ {total_gasto:,.2f}" if total_gasto > 0 else "R$ 0,00", delta_color="inverse")
col3.metric("✨ Margem Restante", f"R$ {saldo_restante:,.2f}")

# Barra de Progresso
st.write("")
st.progress(percentual_usado, text=f"Comprometimento do orçamento: {percentual_usado*100:.1f}%")

if saldo_restante <= 0:
    st.error("🚨 ATENÇÃO: O teto de R$ 5.000,00 foi totalmente atingido!")
elif saldo_restante < 1000:
    st.warning(f"⚠️ Alerta: Restam apenas R$ {saldo_restante:,.2f} de margem para o projeto!")
else:
    st.info(f"💡 Margem disponível de **R$ {saldo_restante:,.2f}** para manter o projeto da cozinha e do closet 100% protegido.")

st.divider()

# Tabela Interativa de Extrato
st.subheader("📋 Extrato Detalhado de Lançamentos")

if not st.session_state.expenses.empty:
    st.dataframe(
        st.session_state.expenses, 
        use_container_width=True, 
        column_config={
            "Data": st.column_config.DateColumn("Data", format="DD/MM/YYYY"),
            "Valor (R$)": st.column_config.NumberColumn("Valor (R$)", format="R$ %.2f")
        }
    )
    
    col_btn1, col_btn2 = st.columns([1, 4])
    with col_btn1:
        if st.button("🗑️ Limpar Extrato", use_container_width=True):
            st.session_state.expenses = pd.DataFrame(columns=['Data', 'Descrição', 'Categoria', 'Valor (R$)'])
            st.rerun()
else:
    st.caption("Nenhum gasto registrado até o momento. Utilize o painel à esquerda para realizar lançamentos.")
