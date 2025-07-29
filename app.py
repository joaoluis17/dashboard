import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Gestão de Projetos", layout="wide")

st.title("📊 Dashboard de Gestão de Projetos")

uploaded_file = st.file_uploader("Faça upload da planilha (.csv ou .xlsx)", type=["csv", "xlsx"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, encoding='utf-8')
        else:
            df = pd.read_excel(uploaded_file)

        # ✅ Verifique se os cabeçalhos obrigatórios estão presentes
        colunas_esperadas = [
            "Ano/Mês", "Sprint", "Classificacao", "Projeto",
            "Responsável", "PT (Devs)", "PT (QA)", "URL", "status renato"
        ]

        if not all(col in df.columns for col in colunas_esperadas):
            st.error("❌ Arquivo inválido. As seguintes colunas são obrigatórias:\n" + ", ".join(colunas_esperadas))
        else:
            st.success("✅ Arquivo carregado com sucesso!")

            # Filtros
            sprint_selecionada = st.selectbox("Selecione o Sprint", df["Sprint"].unique())
            df_sprint = df[df["Sprint"] == sprint_selecionada]

            st.subheader("📌 Visão Geral da Sprint")

            # Gráfico por Responsável
            fig_responsavel = px.bar(
                df_sprint.groupby("Responsável")[["PT (Devs)", "PT (QA)"]].sum().reset_index(),
                x="Responsável",
                y=["PT (Devs)", "PT (QA)"],
                title="Esforço por Responsável",
                barmode="group",
                text_auto=True
            )
            st.plotly_chart(fig_responsavel, use_container_width=True)

            # Gráfico por Projeto
            fig_projeto = px.bar(
                df_sprint.groupby("Projeto")[["PT (Devs)", "PT (QA)"]].sum().reset_index(),
                x="Projeto",
                y=["PT (Devs)", "PT (QA)"],
                title="Esforço por Projeto",
                barmode="group",
                text_auto=True
            )
            st.plotly_chart(fig_projeto, use_container_width=True)

            # Tabela de detalhes
            st.subheader("🔎 Detalhamento por Card")
            st.dataframe(df_sprint[[
                "Ano/Mês", "Sprint", "Classificacao", "Projeto", "Responsável", "PT (Devs)", "PT (QA)", "status renato", "URL"
            ]])

    except Exception as e:
        st.error(f"❌ Erro ao processar o arquivo: {e}")
