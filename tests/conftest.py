"""
conftest.py — Fixtures compartilhadas entre todos os testes.

O pytest carrega este arquivo automaticamente antes de qualquer teste.
Tudo que for definido aqui fica disponível em qualquer arquivo de teste
sem precisar importar explicitamente.
"""

import json
import pytest
import pandas as pd
from unittest.mock import MagicMock

from generator.chart_pipeline import ChartPipeline


# ---------------------------------------------------------------------------
# Dataset compartilhado
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_frame() -> pd.DataFrame:
    """
    Dataset mínimo mas realista, com uma coluna numérica (Sales),
    uma categórica (Country) e uma de data (Date).
    Cobre todos os tipos de gráfico suportados pelo VAIA.
    """
    return pd.DataFrame({
        "Sales":   [100.0, 200.0, 150.0, 300.0, 80.0],
        "Country": ["BR",  "US",  "DE",  "US",  "BR"],
        "Date":    pd.to_datetime(["2024-01", "2024-02", "2024-03", "2024-04", "2024-05"]),
    })


# ---------------------------------------------------------------------------
# Specs JSON válidos (um por tipo de gráfico)
# ---------------------------------------------------------------------------

@pytest.fixture
def bar_spec() -> dict:
    return {
        "type": "bar",
        "data": {
            "dimension": "Country",
            "metric": "Sales",
            "metric_secondary": None,
            "aggregation": "sum",
            "color": None,
            "filters": {},
        },
        "render_options": {
            "log_scale_y": False,
            "show_trend_line": False,
            "nbins": None,
            "top_n": None,
        },
        "title": "Total Sales by Country",
        "description": "Bar chart comparing total sales per country.",
        "explanation": "Bar charts are ideal for comparing discrete categories.",
    }


@pytest.fixture
def line_spec() -> dict:
    return {
        "type": "line",
        "data": {
            "dimension": "Date",
            "metric": "Sales",
            "metric_secondary": None,
            "aggregation": "sum",
            "color": None,
            "filters": {},
        },
        "render_options": {
            "log_scale_y": False,
            "show_trend_line": False,
            "nbins": None,
            "top_n": None,
        },
        "title": "Sales Over Time",
        "description": "Line chart showing sales trend over time.",
        "explanation": "Line charts are suitable for time series data.",
    }


@pytest.fixture
def pie_spec() -> dict:
    return {
        "type": "pie",
        "data": {
            "dimension": "Country",
            "metric": "Sales",
            "metric_secondary": None,
            "aggregation": "sum",
            "color": None,
            "filters": {},
        },
        "render_options": {
            "log_scale_y": False,
            "show_trend_line": False,
            "nbins": None,
            "top_n": None,
        },
        "title": "Sales Share by Country",
        "description": "Pie chart showing each country's share of total sales.",
        "explanation": "Pie charts show proportional contribution.",
    }


# ---------------------------------------------------------------------------
# Factory: pipeline com modelo mockado
# ---------------------------------------------------------------------------

@pytest.fixture
def make_pipeline():
    """
    Retorna uma função que cria um ChartPipeline cujo modelo (assistant)
    é um MagicMock configurado para retornar o JSON fornecido.

    Uso nos testes:
        pipeline = make_pipeline(bar_spec)
        result = pipeline.generate_visualization(frame, prompt)
    """
    def _factory(spec: dict) -> ChartPipeline:
        assistant = MagicMock()
        assistant.generate_text.return_value = json.dumps(spec)
        return ChartPipeline(assistant=assistant)

    return _factory
