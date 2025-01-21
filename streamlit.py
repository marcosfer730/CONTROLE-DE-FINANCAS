import streamlit as st 
import pandas as pd
import plotly.express as px
from io import BytesIO
import xlsxwriter
import json
from datetime import datetime

# Função para inicializar os dados
@st.cache_data
def initialize_data():
    return pd.DataFrame(columns=["Tipo", "Categoria", "Valor", "Data"])

# Função para adicionar uma nova transação
def add_transaction(data, tipo, categoria, valor, data_transacao):
    new_row = {"Tipo": tipo, "Categoria": categoria, "Valor": valor, "Data": data_transacao}
    return pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)

# Função para carregar dados de arquivo
def load_data(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    elif file.name.endswith(".xlsx"):
        return pd.read_excel(file)
    else:
        st.error("Formato de arquivo não suportado. Use CSV ou Excel.")
        return None

# Função para salvar dados em JSON (persistência)
def save_data_to_json(data, filename="data.json"):
    data.to_json(filename, orient="records", lines=True)

# Função para carregar dados de JSON
def load_data_from_json(filename="data.json"):
    try:
        return pd.read_json(filename, orient="records", lines=True)
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame(columns=["Tipo", "Categoria", "Valor", "Data"])

# Categorias predefinidas para transações
CATEGORIAS_PREDEFINIDAS = [
    "Salário", "Alimentação", "Transporte", "Moradia", "Saúde", "Lazer", "Educação", "Outros"
]

# Interface principal
def main():
    st.title("📊 Gerenciador de Finanças Pessoais")
    st.markdown("""Bem-vindo ao seu gerenciador de finanças! Adicione receitas, despesas fixas e visualize seu saldo com gráficos dinâmicos.""")

    # Inicializa os dados
    if "data" not in st.session_state:
        st.session_state.data = initialize_data()
    if "fixed_expenses" not in st.session_state:
        st.session_state.fixed_expenses = initialize_data()

    # Sidebar para adicionar transações
    st.sidebar.header("📋 Adicionar Transação")
    with st.sidebar.form("form_adicionar"):
        tipo = st.radio("Tipo", options=["Receita", "Despesa"], index=0)
        categoria = st.selectbox("Categoria", options=CATEGORIAS_PREDEFINIDAS)
        valor = st.number_input("Valor (R$)", min_value=0.01, step=0.01)
        data_transacao = st.date_input("Data")
        submitted = st.form_submit_button("Adicionar")
        
        if submitted:
            if categoria and valor > 0:
                st.session_state.data = add_transaction(
                    st.session_state.data, tipo, categoria, valor, data_transacao
                )
                st.success("Transação adicionada com sucesso!")
                save_data_to_json(st.session_state.data)
            else:
                st.error("Por favor, preencha todos os campos corretamente.")

    # Sidebar para despesas fixas
    st.sidebar.header("🏠 Adicionar Despesa Fixa")
    with st.sidebar.form("form_despesas_fixas"):
        cat_fixa = st.text_input("Categoria Fixa", placeholder="Ex: Aluguel, Internet, etc.")
        valor_fixo = st.number_input("Valor Fixo (R$)", min_value=0.01, step=0.01)
        fixo_submitted = st.form_submit_button("Adicionar Despesa Fixa")
        
        if fixo_submitted:
            if cat_fixa and valor_fixo > 0:
                st.session_state.fixed_expenses = add_transaction(
                    st.session_state.fixed_expenses, "Despesa Fixa", cat_fixa, valor_fixo, "Fixo"
                )
                st.success("Despesa fixa adicionada com sucesso!")
                save_data_to_json(st.session_state.fixed_expenses)
            else:
                st.error("Por favor, preencha todos os campos corretamente.")

    # Opção de carregar arquivos
    st.sidebar.header("📂 Carregar Arquivo")
    file = st.sidebar.file_uploader("Selecione um arquivo CSV ou Excel")
    if file:
        loaded_data = load_data(file)
        if loaded_data is not None:
            st.session_state.data = pd.concat([st.session_state.data, loaded_data], ignore_index=True)
            st.success("Dados carregados com sucesso!")
            save_data_to_json(st.session_state.data)

    # Exibir tabela e resumo
    st.header("📈 Resumo Financeiro")
    df = st.session_state.data
    df["Valor"] = df["Valor"].astype(float)
    
    total_receitas = df[df["Tipo"] == "Receita"]["Valor"].sum()
    total_despesas = df[df["Tipo"] == "Despesa"]["Valor"].sum()
    despesas_fixas = st.session_state.fixed_expenses["Valor"].sum()
    saldo = total_receitas - total_despesas - despesas_fixas

    st.metric("Saldo Atual", f"R$ {saldo:.2f}")
    col1, col2, col3 = st.columns(3)
    col1.metric("Receitas Totais", f"R$ {total_receitas:.2f}")
    col2.metric("Despesas Variáveis", f"R$ {total_despesas:.2f}")
    col3.metric("Despesas Fixas", f"R$ {despesas_fixas:.2f}")

    # Tabela interativa de transações
    st.subheader("📋 Todas as Transações")

    # Exibir e editar dados
    for i, row in df.iterrows():
        with st.expander(f"{row['Categoria']}"):  # Usar a categoria como título
            tipo_edit = st.radio(f"Tipo da transação {i + 1}", options=["Receita", "Despesa"], index=0 if row['Tipo'] == "Receita" else 1)

            # Verificar se a categoria existe na lista, caso contrário, adicionar como nova
            if row['Categoria'] not in CATEGORIAS_PREDEFINIDAS:
                categoria_edit = st.text_input(f"Categoria {i + 1}", value=row['Categoria'])
            else:
                categoria_edit = st.selectbox(f"Categoria {i + 1}", options=CATEGORIAS_PREDEFINIDAS, index=CATEGORIAS_PREDEFINIDAS.index(row['Categoria']))

            valor_edit = st.number_input(f"Valor (R$) {i + 1}", min_value=0.01, step=0.01, value=row["Valor"])
            data_transacao_edit = st.date_input(f"Data {i + 1}", value=pd.to_datetime(row["Data"]))
            submitted_edit = st.button(f"Salvar Alterações {i + 1}")
            
            if submitted_edit:
                df.at[i, 'Tipo'] = tipo_edit
                df.at[i, 'Categoria'] = categoria_edit
                df.at[i, 'Valor'] = valor_edit
                df.at[i, 'Data'] = data_transacao_edit
                st.session_state.data = df
                st.success(f"Transação {i + 1} editada com sucesso!")
                save_data_to_json(df)
    
    st.dataframe(df, use_container_width=True)

    # Gráficos e tabelas lado a lado
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📉 Evolução do Saldo ao Longo do Tempo")
        # Calcular o saldo de forma dinâmica para cada transação
        df["Data"] = pd.to_datetime(df["Data"], errors='coerce')  # Garantir que todas as datas são datetime
        df_sorted = df.sort_values("Data")
        
        # Calcular saldo por transação
        saldo_dinamico = []
        saldo_atual = 0  # Inicia o saldo com zero
        for i, row in df_sorted.iterrows():
            if row['Tipo'] == 'Receita':
                saldo_atual += row['Valor']
            elif row['Tipo'] == 'Despesa':
                saldo_atual -= row['Valor']
            saldo_dinamico.append(saldo_atual)
        
        df_sorted["Saldo"] = saldo_dinamico

        # Gerar gráfico de linha para evolução do saldo
        fig_line = px.line(df_sorted, x="Data", y="Saldo", title="Evolução do Saldo")
        st.plotly_chart(fig_line, use_container_width=True)

    with col2:
        st.subheader("🍕 Distribuição das Despesas por Categoria")
        # Gráfico de Pizza
        despesas = df[df["Tipo"] == "Despesa"]
        despesas_category = despesas.groupby("Categoria")["Valor"].sum().reset_index()
        
        fig_pie = px.pie(despesas_category, names="Categoria", values="Valor", title="Distribuição das Despesas")
        st.plotly_chart(fig_pie, use_container_width=True)

    # Exportar dados
    st.sidebar.header("💾 Exportar Dados")
    export_format = st.sidebar.radio("Formato", options=["CSV", "Excel", "JSON"])
    if st.sidebar.button("Exportar"):
        if export_format == "CSV":
            st.sidebar.download_button(
                label="Baixar CSV",
                data=st.session_state.data.to_csv(index=False),
                file_name="transacoes.csv",
                mime="text/csv",
            )
        elif export_format == "Excel":
            towrite = BytesIO()
            with pd.ExcelWriter(towrite, engine="xlsxwriter") as writer:
                st.session_state.data.to_excel(writer, index=False, sheet_name="Transações")
                st.session_state.fixed_expenses.to_excel(writer, index=False, sheet_name="Despesas Fixas")
                writer.save()
                towrite.seek(0)
            st.sidebar.download_button(
                label="Baixar Excel",
                data=towrite,
                file_name="transacoes.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        elif export_format == "JSON":
            st.sidebar.download_button(
                label="Baixar JSON",
                data=st.session_state.data.to_json(orient="records", lines=True),
                file_name="transacoes.json",
                mime="application/json"
            )

if __name__ == "__main__":
    main()
