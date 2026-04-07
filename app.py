from __future__ import annotations

from pathlib import Path

import streamlit as st

from chart_pipeline import ChartPipeline
from chart_utils import build_plotly_figure, load_csv_dataset, summarize_dataframe


st.set_page_config(page_title="VAIA Dataset Assistant", layout="wide")

PROJECT_DIR = Path(__file__).resolve().parent
SAMPLE_DATASET_PATH = PROJECT_DIR / "sample_data" / "sample_sales_data.csv"


@st.cache_resource
def load_pipeline() -> ChartPipeline:
    return ChartPipeline()


@st.cache_data
def load_sample_dataset():
    return load_csv_dataset(SAMPLE_DATASET_PATH)


@st.cache_data
def load_sample_dataset_bytes() -> bytes:
    return SAMPLE_DATASET_PATH.read_bytes()


def resolve_dataset(uploaded_file, use_sample_dataset: bool):
    try:
        if uploaded_file is not None:
            return load_csv_dataset(uploaded_file.getvalue()), uploaded_file.name, None

        if use_sample_dataset:
            return load_sample_dataset(), SAMPLE_DATASET_PATH.name, None

        return None, None, None
    except Exception as exc:
        return None, None, str(exc)


pipeline = load_pipeline()

st.title("VAIA - Visualizacao assistida por IA para datasets")
st.caption(
    "Faça upload de um CSV financeiro, escreva seu pedido em linguagem natural e "
    "receba uma especificação de gráfico baseada apenas nas colunas reais do dataset."
)

with st.sidebar:
    st.subheader("Dataset")
    use_sample_dataset = st.checkbox("Usar dataset de exemplo embutido", value=True)
    st.download_button(
        "Baixar dataset de exemplo",
        data=load_sample_dataset_bytes(),
        file_name=SAMPLE_DATASET_PATH.name,
        mime="text/csv",
    )

    st.subheader("Prompts sugeridos")
    st.write("Compare total sales by country in a bar chart and split by product line.")
    st.write("Show the sales trend over time in a line chart.")
    st.write("Show how each product line contributes to total sales in a pie chart.")


uploaded_file = st.file_uploader("Upload de dataset CSV", type=["csv"])
dataset, dataset_name, dataset_error = resolve_dataset(uploaded_file, use_sample_dataset)

if dataset_error:
    st.error(f"Não foi possível carregar o dataset: {dataset_error}")
elif dataset is None:
    st.info("Envie um arquivo CSV ou marque a opção para usar o dataset de exemplo.")
else:
    summary = summarize_dataframe(dataset)

    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Linhas", summary["row_count"])
    col_b.metric("Colunas", summary["column_count"])
    col_c.metric("Dataset ativo", dataset_name)

    with st.expander("Pré-visualização do dataset", expanded=True):
        st.dataframe(dataset.head(20), use_container_width=True)

    with st.expander("Resumo do dataset"):
        st.json(summary)


user_prompt = st.text_area(
    "Pedido em linguagem natural",
    height=120,
    placeholder="Exemplo: Compare total sales by country in a bar chart and split by product line.",
)

generate = st.button("Gerar visualização", type="primary")

if generate:
    if dataset is None:
        st.error("Carregue um dataset CSV antes de gerar o gráfico.")
    elif not user_prompt.strip():
        st.error("Digite um pedido para gerar o gráfico.")
    else:
        try:
            result = pipeline.generate_visualization(dataset, user_prompt)
            figure = build_plotly_figure(result.plot_frame, result.spec)

            st.info(f"Fonte da especificação: {result.source}")
            st.plotly_chart(figure, use_container_width=True)

            spec_col, data_col = st.columns(2)

            with spec_col:
                st.subheader("Especificação JSON")
                st.json(result.spec.to_dict())

            with data_col:
                st.subheader("Dados agregados usados no gráfico")
                st.dataframe(result.plot_frame, use_container_width=True)

            with st.expander("Resposta bruta do modelo"):
                st.code(result.raw_response or "Sem resposta bruta do modelo.", language="json")

            if result.warnings:
                st.warning("\n".join(result.warnings))
        except Exception as exc:
            st.error(f"Não foi possível gerar a visualização: {exc}")
