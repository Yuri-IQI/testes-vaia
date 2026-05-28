from __future__ import annotations

import os
from pathlib import Path

import streamlit as st
from peft import PeftModel

from code_assistant import CodeAssistant
from generator.chart_pipeline import ChartPipeline
from generator.dataset import load_csv_dataset, summarize_dataframe
from generator.renderer import build_plotly_figure

st.set_page_config(page_title="VAIA - Financial Dataset Assistant", layout="wide")

PROJECT_DIR = Path(__file__).resolve().parent

SAMPLE_DATASET_PATH = (
    PROJECT_DIR
    / "sample_data"
    / os.getenv("DEFAULT_DATASET_NAME", "finance_economics_dataset.csv")
)
DEFAULT_ADAPTER    = os.getenv("DEFAULT_ADAPTER", "financial_adapter")
DEFAULT_MODEL_NAME = os.getenv("BASE_MODEL", "Qwen/Qwen2.5-0.5B-Instruct")

SUGGESTED_PROMPTS = [
    "Show the evolution of crude oil prices over time.",
    "Compare average close price by stock index.",
    "Show the distribution of trading volume.",
    "Is there a correlation between gold price and real estate index?",
    "Show the spread of GDP growth by stock index.",
    "What is the share of total retail sales by stock index?",
    "Show trading volume over time grouped by stock index.",
    "Show the top 5 stock indexes by average corporate profits.",
    "Is there a relationship between inflation rate and unemployment rate?",
    "Show the variance of interest rates across stock indexes.",
]


class FineTunedAssistant(CodeAssistant):
    def __init__(self, adapter_path: str | None = None, model_name: str = DEFAULT_MODEL_NAME) -> None:
        super().__init__(model_name=model_name)
        self.adapter_path = adapter_path

    def _ensure_loaded(self) -> None:
        super()._ensure_loaded()
        if self.adapter_path and Path(self.adapter_path).exists():
            self._model = PeftModel.from_pretrained(self._model, self.adapter_path)
            self._model = self._model.merge_and_unload()


@st.cache_resource
def load_pipeline() -> ChartPipeline:
    assistant = FineTunedAssistant(
        adapter_path=DEFAULT_ADAPTER,
        model_name=DEFAULT_MODEL_NAME,
    )
    return ChartPipeline(assistant=assistant)

@st.cache_data
def load_sample_dataset():
    return load_csv_dataset(SAMPLE_DATASET_PATH)


@st.cache_data
def load_sample_dataset_bytes() -> bytes:
    return SAMPLE_DATASET_PATH.read_bytes()


def resolve_dataset(uploaded_file, use_sample: bool):
    try:
        if uploaded_file is not None:
            return load_csv_dataset(uploaded_file.getvalue()), uploaded_file.name, None
        if use_sample:
            return load_sample_dataset(), SAMPLE_DATASET_PATH.name, None
        return None, None, None
    except Exception as exc:
        return None, None, str(exc)

with st.sidebar:
    st.header("Model")
    st.caption(f"**Base model:** {DEFAULT_MODEL_NAME}")
    adapter_exists = Path(DEFAULT_ADAPTER).exists()
    st.caption(
        f"**Adapter:** {DEFAULT_ADAPTER} — {'found' if adapter_exists else 'not found, using base model'}"
    )

    st.divider()

    st.header("Dataset")
    use_sample = st.checkbox("Use built-in sample dataset", value=True)
    st.download_button(
        "Download sample dataset",
        data=load_sample_dataset_bytes(),
        file_name=SAMPLE_DATASET_PATH.name,
        mime="text/csv",
    )

    st.divider()

    st.header("Suggested prompts")
    for prompt in SUGGESTED_PROMPTS:
        st.caption(f"• {prompt}")

st.title("VAIA — Financial Dataset Assistant")
st.caption(
    "Upload a CSV, describe what you want to see in natural language, "
    "and get a chart built exclusively from the dataset's real columns."
)

pipeline = load_pipeline()

uploaded_file = st.file_uploader("Upload CSV dataset", type=["csv"])
dataset, dataset_name, dataset_error = resolve_dataset(uploaded_file, use_sample)

if dataset_error:
    st.error(f"Could not load dataset: {dataset_error}")
elif dataset is None:
    st.info("Upload a CSV file or enable the sample dataset option in the sidebar.")
else:
    summary = summarize_dataframe(dataset)

    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Rows",    summary["row_count"])
    col_b.metric("Columns", summary["column_count"])
    col_c.metric("Dataset", dataset_name)

    with st.expander("Dataset preview", expanded=True):
        st.dataframe(dataset.head(20), use_container_width=True)

    with st.expander("Dataset summary"):
        st.json(summary)

user_prompt = st.text_area(
    "Natural language request",
    height=100,
    placeholder="Example: show crude oil price over time grouped by stock index.",
)

generate = st.button("Generate visualization", type="primary")

if generate:
    if dataset is None:
        st.error("Load a dataset before generating a chart.")
    elif not user_prompt.strip():
        st.error("Enter a request to generate a chart.")
    else:
        with st.spinner("Generating visualization…"):
            try:
                result = pipeline.generate_visualization(dataset, user_prompt)

                if result.spec.chart_type == "histogram" and result.spec.render_options.nbins is None:
                    unique = dataset[result.spec.data.metric].nunique()
                    result.spec.render_options.nbins = 20 if unique <= 30 else 40 if unique <= 200 else 60

                figure = build_plotly_figure(result.plot_frame, result.spec)

                source_label = {
                    "model":    "Model",
                    "fallback": "Heuristic fallback",
                }.get(result.source, result.source)

                st.info(f"Specification source: {source_label}")

                if result.warnings:
                    for warning in result.warnings:
                        st.warning(warning)

                st.plotly_chart(figure, use_container_width=True)

                spec_col, data_col = st.columns(2)

                with spec_col:
                    st.subheader("JSON specification")
                    st.json(result.spec.to_dict())

                with data_col:
                    st.subheader("Aggregated data")
                    st.dataframe(result.plot_frame, use_container_width=True)

                with st.expander("Raw model response"):
                    st.code(result.raw_response or "No raw response.", language="json")

            except Exception as exc:
                st.error(f"Could not generate visualization: {exc}")
                st.exception(exc)