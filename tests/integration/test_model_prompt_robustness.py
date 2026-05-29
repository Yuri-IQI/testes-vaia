"""
test_model_prompt_robustness.py — Testes de Robustez de Prompt com Modelo Real

ATENÇÃO: estes são testes de INTEGRAÇÃO. Eles carregam o modelo Qwen real
(com ou sem adapter LoRA) e fazem chamadas reais de inferência.

Tempo estimado: 1-5 minutos dependendo do hardware (GPU vs CPU).
Requisito: modelo baixado via Hugging Face (ocorre automaticamente na
primeira execução) e, opcionalmente, adapter treinado em financial_adapter/.

Como rodar APENAS estes testes:
    $python -m pytest tests/integration/ -v -s --tb=short

Como rodar APENAS testes unitários (rápidos, sem modelo):
    $python -m pytest tests/ --ignore=tests/integration/ -v

Como rodar TUDO:
    $python -m pytest -v -s

-----------------------------------------------------------------------
Dataset usado: finance_economics_dataset.csv
Colunas relevantes:
  - Temporal:    Date
  - Categórica:  Stock Index  (valores: "Dow Jones", "S&P 500", ...)
  - Numéricas:   Close Price, Crude Oil Price (USD per Barrel),
                 GDP Growth (%), Gold Price (USD per Ounce), etc.

Os prompts usam APENAS essas colunas para garantir que o modelo pode
resolver sem inventar colunas inexistentes.

O que estes testes medem que os testes com mock NÃO medem:
- Se o modelo Qwen realmente entende variações de linguagem natural
- Se o adapter LoRA melhora a consistência vs o modelo base
- Qual a taxa real de acerto por tipo de gráfico e por variação de prompt
- Com que frequência o modelo cai no fallback heurístico
-----------------------------------------------------------------------
"""

from pathlib import Path
import pandas as pd
import pytest

from generator.dataset import load_csv_dataset


# ---------------------------------------------------------------------------
# Dataset real — o mesmo que o modelo foi treinado para usar
# ---------------------------------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent

@pytest.fixture(scope="module")
def frame() -> pd.DataFrame:
    """
    Usa o finance_economics_dataset.csv real.
    Colunas usadas nos testes:
      - Date         (temporal)
      - Stock Index  (categórica: "Dow Jones", "S&P 500", "FTSE 100", ...)
      - Close Price  (numérica)
      - Crude Oil Price (USD per Barrel) (numérica)
      - GDP Growth (%) (numérica)
    """
    path = PROJECT_DIR / "sample_data" / "finance_economics_dataset.csv"
    return load_csv_dataset(path)


# ---------------------------------------------------------------------------
# Grupos de prompts — usam APENAS colunas reais do dataset
# ---------------------------------------------------------------------------

# Grupo 1: Bar chart — Close Price por Stock Index
BAR_PROMPTS = [
    "Show the average close price by stock index in a bar chart",
    "Display average closing prices per stock index as a bar chart",
    "Compare the mean close price across stock indexes using bars",
    "Present a bar graph of close price grouped by stock index",
]

# Grupo 2: Line chart — Close Price ao longo de Date
LINE_PROMPTS = [
    "Show the close price trend over time as a line chart",
    "Display how close price evolved over time using a line graph",
    "Plot close price over time in a line chart",
    "Show me a timeline of the close price",
]

# Grupo 3: Pie chart — participação do Close Price por Stock Index
PIE_PROMPTS = [
    "Show each stock index share of total close price in a pie chart",
    "Display the close price distribution by stock index as a pie",
    "What percentage of close price does each stock index represent? Use a pie chart",
    "Show the proportion of close price per stock index in a pie",
]


# ---------------------------------------------------------------------------
# Helper — formata o resultado para exibição e rastreamento
# ---------------------------------------------------------------------------

def _log_resultado(prompt: str, result) -> None:
    """Imprime uma linha de diagnóstico por resultado (visível com pytest -s)."""
    fallback_flag = " ⚠ FALLBACK" if result.source == "fallback" else ""
    print(
        f"\n  [{result.source}{fallback_flag}] {prompt!r}\n"
        f"    → type={result.spec.chart_type}"
        f"  metric={result.spec.data.metric}"
        f"  dim={result.spec.data.dimension}"
    )
    if result.warnings:
        for w in result.warnings:
            print(f"    ⚠ warning: {w}")


def _campos_estruturais(spec) -> dict:
    return {
        "type":        spec.chart_type,
        "metric":      spec.data.metric,
        "dimension":   spec.data.dimension,
        "aggregation": spec.data.aggregation,
    }


# ---------------------------------------------------------------------------
# Testes: Bar chart com modelo real
# ---------------------------------------------------------------------------

@pytest.mark.integration
class TestModelBarPrompts:
    """
    Prompts pedem bar chart de Close Price por Stock Index.
    Ambas as colunas existem no dataset — o modelo não precisa inventar nada.
    """

    @pytest.mark.parametrize("prompt", BAR_PROMPTS)
    def test_chart_type_e_bar(self, prompt, frame, real_pipeline):
        result = real_pipeline.generate_visualization(frame, prompt)
        _log_resultado(prompt, result)

        assert result.spec.chart_type == "bar", (
            f"Prompt: '{prompt}'\n"
            f"Esperado type=bar | Obtido: {result.spec.chart_type}\n"
            f"Source: {result.source} | Warnings: {result.warnings}"
        )

    @pytest.mark.parametrize("prompt", BAR_PROMPTS)
    def test_metrica_e_close_price(self, prompt, frame, real_pipeline):
        result = real_pipeline.generate_visualization(frame, prompt)

        assert result.spec.data.metric == "Close Price", (
            f"Prompt: '{prompt}'\n"
            f"Esperado metric='Close Price' | Obtido: '{result.spec.data.metric}'"
        )

    @pytest.mark.parametrize("prompt", BAR_PROMPTS)
    def test_dimensao_e_stock_index(self, prompt, frame, real_pipeline):
        result = real_pipeline.generate_visualization(frame, prompt)

        assert result.spec.data.dimension == "Stock Index", (
            f"Prompt: '{prompt}'\n"
            f"Esperado dimension='Stock Index' | Obtido: '{result.spec.data.dimension}'"
        )

    @pytest.mark.parametrize("prompt", BAR_PROMPTS)
    def test_nao_usou_fallback(self, prompt, frame, real_pipeline):
        result = real_pipeline.generate_visualization(frame, prompt)

        assert result.source == "model", (
            f"Prompt: '{prompt}'\n"
            f"O modelo não gerou JSON válido — caiu no fallback heurístico.\n"
            f"Warnings: {result.warnings}\n"
            f"Resposta bruta do modelo:\n{result.raw_response[:400]}"
        )


# ---------------------------------------------------------------------------
# Testes: Line chart com modelo real
# ---------------------------------------------------------------------------

@pytest.mark.integration
class TestModelLinePrompts:
    """
    Prompts pedem line chart de Close Price ao longo de Date.
    """

    @pytest.mark.parametrize("prompt", LINE_PROMPTS)
    def test_chart_type_e_line(self, prompt, frame, real_pipeline):
        result = real_pipeline.generate_visualization(frame, prompt)
        _log_resultado(prompt, result)

        assert result.spec.chart_type == "line", (
            f"Prompt: '{prompt}'\n"
            f"Esperado type=line | Obtido: {result.spec.chart_type}\n"
            f"Source: {result.source} | Warnings: {result.warnings}"
        )

    @pytest.mark.parametrize("prompt", LINE_PROMPTS)
    def test_dimensao_e_date(self, prompt, frame, real_pipeline):
        result = real_pipeline.generate_visualization(frame, prompt)

        assert result.spec.data.dimension == "Date", (
            f"Prompt: '{prompt}'\n"
            f"Esperado dimension='Date' | Obtido: '{result.spec.data.dimension}'"
        )

    @pytest.mark.parametrize("prompt", LINE_PROMPTS)
    def test_nao_usou_fallback(self, prompt, frame, real_pipeline):
        result = real_pipeline.generate_visualization(frame, prompt)

        assert result.source == "model", (
            f"Prompt: '{prompt}'\n"
            f"O modelo caiu no fallback.\n"
            f"Warnings: {result.warnings}\n"
            f"Resposta bruta:\n{result.raw_response[:400]}"
        )


# ---------------------------------------------------------------------------
# Testes: Pie chart com modelo real
# ---------------------------------------------------------------------------

@pytest.mark.integration
class TestModelPiePrompts:
    """
    Prompts pedem pie chart de Close Price por Stock Index.
    """

    @pytest.mark.parametrize("prompt", PIE_PROMPTS)
    def test_chart_type_e_pie(self, prompt, frame, real_pipeline):
        result = real_pipeline.generate_visualization(frame, prompt)
        _log_resultado(prompt, result)

        assert result.spec.chart_type == "pie", (
            f"Prompt: '{prompt}'\n"
            f"Esperado type=pie | Obtido: {result.spec.chart_type}\n"
            f"Source: {result.source} | Warnings: {result.warnings}"
        )

    @pytest.mark.parametrize("prompt", PIE_PROMPTS)
    def test_nao_usou_fallback(self, prompt, frame, real_pipeline):
        result = real_pipeline.generate_visualization(frame, prompt)

        assert result.source == "model", (
            f"Prompt: '{prompt}'\n"
            f"O modelo caiu no fallback.\n"
            f"Warnings: {result.warnings}\n"
            f"Resposta bruta:\n{result.raw_response[:400]}"
        )


# ---------------------------------------------------------------------------
# Teste de consistência entre variações + relatório de fallback
# ---------------------------------------------------------------------------

@pytest.mark.integration
class TestConsistenciaEntreVariacoes:
    """
    Verifica se o modelo produz o MESMO tipo de gráfico para TODAS as
    variações de um grupo. Também produz um relatório de fallback por grupo,
    mostrando quais prompts o modelo conseguiu resolver sem heurística.

    Este é o dado central para o artigo: taxa de consistência e taxa de
    acerto direto (sem fallback) por grupo de intenção.
    """

    def _rodar_grupo(self, prompts, frame, pipeline, label):
        resultados = []
        for prompt in prompts:
            result = pipeline.generate_visualization(frame, prompt)
            resultados.append(result)
            _log_resultado(prompt, result)

        # Relatório de fallback
        total   = len(resultados)
        modelos = sum(1 for r in resultados if r.source == "model")
        fallbacks = total - modelos
        print(
            f"\n  --- Relatório {label} ---\n"
            f"  Total de prompts : {total}\n"
            f"  Resolvidos pelo modelo  : {modelos}/{total} ({100*modelos//total}%)\n"
            f"  Caíram no fallback      : {fallbacks}/{total} ({100*fallbacks//total}%)"
        )
        return resultados

    def test_bar_consistencia_e_fallback(self, frame, real_pipeline):
        resultados = self._rodar_grupo(BAR_PROMPTS, frame, real_pipeline, "BAR")
        tipos = [r.spec.chart_type for r in resultados]

        assert len(set(tipos)) == 1, (
            f"O modelo gerou tipos DIFERENTES para variações do mesmo pedido de bar.\n"
            f"Resultado por prompt:\n"
            + "\n".join(f"  '{p}' → {t} [{r.source}]"
                        for p, t, r in zip(BAR_PROMPTS, tipos, resultados))
        )

    def test_line_consistencia_e_fallback(self, frame, real_pipeline):
        resultados = self._rodar_grupo(LINE_PROMPTS, frame, real_pipeline, "LINE")
        tipos = [r.spec.chart_type for r in resultados]

        assert len(set(tipos)) == 1, (
            f"O modelo gerou tipos DIFERENTES para variações do mesmo pedido de line.\n"
            f"Resultado por prompt:\n"
            + "\n".join(f"  '{p}' → {t} [{r.source}]"
                        for p, t, r in zip(LINE_PROMPTS, tipos, resultados))
        )

    def test_pie_consistencia_e_fallback(self, frame, real_pipeline):
        resultados = self._rodar_grupo(PIE_PROMPTS, frame, real_pipeline, "PIE")
        tipos = [r.spec.chart_type for r in resultados]

        assert len(set(tipos)) == 1, (
            f"O modelo gerou tipos DIFERENTES para variações do mesmo pedido de pie.\n"
            f"Resultado por prompt:\n"
            + "\n".join(f"  '{p}' → {t} [{r.source}]"
                        for p, t, r in zip(PIE_PROMPTS, tipos, resultados))
        )
