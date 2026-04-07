from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from chart_pipeline import ChartPipeline


st.set_page_config(page_title="VAIA", layout="wide")


@st.cache_resource
def load_pipeline() -> ChartPipeline:
    return ChartPipeline()


def render_chart(chart) -> go.Figure:
    figure = go.Figure()

    if chart.chart_type == "bar":
        figure.add_bar(x=chart.labels, y=chart.values, marker_color="#2563eb")
    elif chart.chart_type == "line":
        figure.add_scatter(
            x=chart.labels,
            y=chart.values,
            mode="lines+markers",
            line={"color": "#0f766e", "width": 3},
            marker={"size": 8},
        )
    elif chart.chart_type == "pie":
        figure.add_pie(labels=chart.labels, values=chart.values, hole=0.25)

    figure.update_layout(
        title=chart.title,
        template="plotly_white",
        margin={"l": 24, "r": 24, "t": 60, "b": 24},
    )

    return figure


pipeline = load_pipeline()

st.title("VAIA - Visualizacao Assistida por IA")
st.caption(
    "Descreva um grafico em linguagem natural. O sistema tenta usar o modelo "
    "Qwen localmente e faz fallback para uma heuristica quando necessario."
)

with st.sidebar:
    st.subheader("Sugestoes")
    st.write("bar chart with values sales: 12, support: 7, product: 15")
    st.write("line chart with values jan: 5, feb: 8, mar: 13")
    st.write("pie chart with values cats: 4, dogs: 6, birds: 2")


user_input = st.text_area(
    "Prompt",
    height=120,
    placeholder="Exemplo: line chart with values jan: 5, feb: 8, mar: 13",
)

generate = st.button("Gerar grafico", type="primary")

if generate:
    if not user_input.strip():
        st.error("Digite um prompt para gerar o grafico.")
    else:
        result = pipeline.generate_chart(user_input)

        st.info(f"Fonte da resposta: {result.source}")
        st.plotly_chart(render_chart(result.chart), use_container_width=True)

        col_json, col_raw = st.columns(2)

        with col_json:
            st.subheader("JSON final")
            st.json(result.chart.to_dict())

        with col_raw:
            st.subheader("Resposta bruta")
            st.code(result.raw_response or "Sem resposta bruta do modelo.", language="json")

        if result.warnings:
            st.warning("\n".join(result.warnings))
