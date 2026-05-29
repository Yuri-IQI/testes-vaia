"""
test_prompt_robustness.py — Testes de Variação de Prompt

Objetivo: verificar se o modelo produz specs semanticamente equivalentes
para prompts diferentes que expressam a mesma intenção.

Conceito: um modelo robusto não deve mudar o tipo de gráfico, a dimensão
ou a métrica só porque o usuário trocou "show" por "display". Apenas campos
cosméticos (title, description) podem variar livremente.

Estratégia de validação: comparação estrutural dos campos que definem
o gráfico — type, dimension, metric e aggregation. Campos como title
e description são ignorados propositalmente.
"""

import pytest


# ---------------------------------------------------------------------------
# Helpers de comparação estrutural
# ---------------------------------------------------------------------------

def _campos_estruturais(spec_dict: dict) -> dict:
    """
    Extrai apenas os campos que definem o gráfico em si,
    ignorando campos cosméticos (title, description, explanation).
    """
    data = spec_dict.get("data", {})
    return {
        "type":        spec_dict.get("type"),
        "dimension":   data.get("dimension"),
        "metric":      data.get("metric"),
        "aggregation": data.get("aggregation"),
        "color":       data.get("color"),
    }


def _specs_sao_equivalentes(resultado: dict, esperado: dict) -> bool:
    """Retorna True se os dois specs descrevem o mesmo gráfico."""
    return _campos_estruturais(resultado) == _campos_estruturais(esperado)


# ---------------------------------------------------------------------------
# Grupos de prompts — cada grupo expressa UMA única intenção
# ---------------------------------------------------------------------------

# Grupo 1: Bar chart — Sales por Country
BAR_PROMPTS = [
    "Show total sales by country in a bar chart",
    "Display sales per country as a bar chart",
    "Compare sales across countries using bars",
    "Present a bar graph of sales grouped by country",
]

# Grupo 2: Line chart — Sales ao longo do tempo (Date)
LINE_PROMPTS = [
    "Show the sales trend over time as a line chart",
    "Display how sales evolved over time using a line graph",
    "Plot sales over time in a line chart",
    "Show me a timeline of sales",
]

# Grupo 3: Pie chart — participação de Sales por Country
PIE_PROMPTS = [
    "Show each country's share of total sales in a pie chart",
    "Display the sales distribution by country as a pie",
    "What percentage of sales does each country represent? Use a pie chart",
    "Show the proportion of sales per country in a pie",
]


# ---------------------------------------------------------------------------
# Testes: Bar chart
# ---------------------------------------------------------------------------

class TestBarPromptVariation:
    """
    Todos os prompts do grupo BAR_PROMPTS devem produzir um spec
    com type=bar, dimension=Country, metric=Sales, aggregation=sum.
    """

    @pytest.mark.parametrize("prompt", BAR_PROMPTS)
    def test_tipo_e_bar(self, prompt, sample_frame, bar_spec, make_pipeline):
        pipeline = make_pipeline(bar_spec)
        result = pipeline.generate_visualization(sample_frame, prompt)

        assert result.spec.chart_type == "bar", (
            f"Prompt: '{prompt}'\n"
            f"Esperado: bar | Obtido: {result.spec.chart_type}"
        )

    @pytest.mark.parametrize("prompt", BAR_PROMPTS)
    def test_dimensao_e_country(self, prompt, sample_frame, bar_spec, make_pipeline):
        pipeline = make_pipeline(bar_spec)
        result = pipeline.generate_visualization(sample_frame, prompt)

        assert result.spec.data.dimension == "Country", (
            f"Prompt: '{prompt}'\n"
            f"Esperado: Country | Obtido: {result.spec.data.dimension}"
        )

    @pytest.mark.parametrize("prompt", BAR_PROMPTS)
    def test_metrica_e_sales(self, prompt, sample_frame, bar_spec, make_pipeline):
        pipeline = make_pipeline(bar_spec)
        result = pipeline.generate_visualization(sample_frame, prompt)

        assert result.spec.data.metric == "Sales", (
            f"Prompt: '{prompt}'\n"
            f"Esperado: Sales | Obtido: {result.spec.data.metric}"
        )

    @pytest.mark.parametrize("prompt", BAR_PROMPTS)
    def test_spec_completo_equivalente(self, prompt, sample_frame, bar_spec, make_pipeline):
        """Teste integrado: verifica todos os campos estruturais de uma vez."""
        pipeline = make_pipeline(bar_spec)
        result = pipeline.generate_visualization(sample_frame, prompt)

        assert _specs_sao_equivalentes(result.spec.to_dict(), bar_spec), (
            f"Prompt: '{prompt}'\n"
            f"Esperado: {_campos_estruturais(bar_spec)}\n"
            f"Obtido:   {_campos_estruturais(result.spec.to_dict())}"
        )


# ---------------------------------------------------------------------------
# Testes: Line chart
# ---------------------------------------------------------------------------

class TestLinePromptVariation:
    """
    Todos os prompts do grupo LINE_PROMPTS devem produzir um spec
    com type=line, dimension=Date, metric=Sales, aggregation=sum.
    """

    @pytest.mark.parametrize("prompt", LINE_PROMPTS)
    def test_tipo_e_line(self, prompt, sample_frame, line_spec, make_pipeline):
        pipeline = make_pipeline(line_spec)
        result = pipeline.generate_visualization(sample_frame, prompt)

        assert result.spec.chart_type == "line", (
            f"Prompt: '{prompt}'\n"
            f"Esperado: line | Obtido: {result.spec.chart_type}"
        )

    @pytest.mark.parametrize("prompt", LINE_PROMPTS)
    def test_dimensao_e_date(self, prompt, sample_frame, line_spec, make_pipeline):
        pipeline = make_pipeline(line_spec)
        result = pipeline.generate_visualization(sample_frame, prompt)

        assert result.spec.data.dimension == "Date", (
            f"Prompt: '{prompt}'\n"
            f"Esperado: Date | Obtido: {result.spec.data.dimension}"
        )

    @pytest.mark.parametrize("prompt", LINE_PROMPTS)
    def test_spec_completo_equivalente(self, prompt, sample_frame, line_spec, make_pipeline):
        pipeline = make_pipeline(line_spec)
        result = pipeline.generate_visualization(sample_frame, prompt)

        assert _specs_sao_equivalentes(result.spec.to_dict(), line_spec), (
            f"Prompt: '{prompt}'\n"
            f"Esperado: {_campos_estruturais(line_spec)}\n"
            f"Obtido:   {_campos_estruturais(result.spec.to_dict())}"
        )


# ---------------------------------------------------------------------------
# Testes: Pie chart
# ---------------------------------------------------------------------------

class TestPiePromptVariation:
    """
    Todos os prompts do grupo PIE_PROMPTS devem produzir um spec
    com type=pie, dimension=Country, metric=Sales, aggregation=sum.
    """

    @pytest.mark.parametrize("prompt", PIE_PROMPTS)
    def test_tipo_e_pie(self, prompt, sample_frame, pie_spec, make_pipeline):
        pipeline = make_pipeline(pie_spec)
        result = pipeline.generate_visualization(sample_frame, prompt)

        assert result.spec.chart_type == "pie", (
            f"Prompt: '{prompt}'\n"
            f"Esperado: pie | Obtido: {result.spec.chart_type}"
        )

    @pytest.mark.parametrize("prompt", PIE_PROMPTS)
    def test_spec_completo_equivalente(self, prompt, sample_frame, pie_spec, make_pipeline):
        pipeline = make_pipeline(pie_spec)
        result = pipeline.generate_visualization(sample_frame, prompt)

        assert _specs_sao_equivalentes(result.spec.to_dict(), pie_spec), (
            f"Prompt: '{prompt}'\n"
            f"Esperado: {_campos_estruturais(pie_spec)}\n"
            f"Obtido:   {_campos_estruturais(result.spec.to_dict())}"
        )


# ---------------------------------------------------------------------------
# Teste de regressão: campos cosméticos podem variar
# ---------------------------------------------------------------------------

class TestCamposCosmeticosVariam:
    """
    Garante que o sistema NÃO rejeita specs com title/description
    diferentes — esses campos são cosméticos e devem variar livremente.
    """

    def test_titles_diferentes_nao_quebram_equivalencia(
        self, sample_frame, bar_spec, make_pipeline
    ):
        spec_titulo_diferente = {**bar_spec, "title": "Um título completamente diferente"}
        pipeline = make_pipeline(spec_titulo_diferente)
        result = pipeline.generate_visualization(sample_frame, BAR_PROMPTS[0])

        # A equivalência estrutural deve ser mantida mesmo com título diferente
        assert _specs_sao_equivalentes(result.spec.to_dict(), bar_spec)
