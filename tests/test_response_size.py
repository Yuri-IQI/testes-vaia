"""
test_response_size.py — Testes de Tamanho de Resposta

Objetivo: verificar como a pipeline se comporta com respostas de diferentes
tamanhos — desde JSONs completos até respostas truncadas ou muito longas.

Dois ângulos de teste:

1. COMPORTAMENTO DO PARSER (json_parser.py)
   Testa se o extract_json consegue lidar com respostas reais que o modelo
   poderia gerar: com prefixo, com sufixo, truncadas, completamente inválidas.
   Esses testes NÃO dependem do modelo — são unitários puros.

2. COMPORTAMENTO DA PIPELINE
   Testa como a ChartPipeline reage quando o modelo retorna respostas
   de tamanhos variados: completa, truncada, vazia, gigante.
   O modelo é mockado para retornar strings de tamanhos controlados.

Por que isso importa: o parâmetro max_new_tokens=600 na pipeline pode
truncar o JSON se o modelo gerar muitos tokens de "aquecimento" antes do {.
Esses testes documentam os limites do sistema atual.
"""

import json
import pytest

from json_parser import extract_json, parse_json
from generator.chart_pipeline import ChartPipeline
from unittest.mock import MagicMock


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _truncate_at_chars(text: str, n_chars: int) -> str:
    """Simula truncamento por limite de tokens (aprox. 3.5 chars/token)."""
    return text[:n_chars]


def _make_pipeline_returning(raw_response: str) -> ChartPipeline:
    assistant = MagicMock()
    assistant.generate_text.return_value = raw_response
    return ChartPipeline(assistant=assistant)


# ---------------------------------------------------------------------------
# Fixtures locais
# ---------------------------------------------------------------------------

@pytest.fixture
def full_json_str(bar_spec) -> str:
    """JSON completo e válido serializado como string."""
    return json.dumps(bar_spec, indent=2)


# ---------------------------------------------------------------------------
# Bloco 1: Parser com resposta completa e bem formada
# ---------------------------------------------------------------------------

class TestParserRespostaCompleta:
    """
    O parser deve extrair o JSON corretamente quando a resposta
    é um JSON limpo, sem ruído ao redor.
    """

    def test_json_puro_e_extraido(self, full_json_str):
        assert extract_json(full_json_str) is not None

    def test_json_puro_e_parseado(self, full_json_str):
        extracted = extract_json(full_json_str)
        parsed = parse_json(extracted)
        assert isinstance(parsed, dict)
        assert parsed["type"] == "bar"

    def test_json_minificado_e_extraido(self, bar_spec):
        """JSON sem espaços (como modelos frequentemente geram)."""
        minified = json.dumps(bar_spec, separators=(",", ":"))
        assert extract_json(minified) is not None


# ---------------------------------------------------------------------------
# Bloco 2: Parser com ruído ao redor do JSON (respostas "verbosas")
# ---------------------------------------------------------------------------

class TestParserComRuidoAoRedor:
    """
    Modelos frequentemente adicionam texto antes ou depois do JSON.
    O parser deve ser robusto o suficiente para ignorar esse ruído.
    """

    def test_prefixo_de_texto_e_ignorado(self, full_json_str):
        response = "Here is the JSON specification:\n\n" + full_json_str
        assert extract_json(response) is not None

    def test_sufixo_de_texto_e_ignorado(self, full_json_str):
        response = full_json_str + "\n\nThis chart shows sales by country."
        result = extract_json(response)
        assert result is not None

    def test_prefixo_e_sufixo_combinados(self, full_json_str):
        response = (
            "Based on your request, here is the spec:\n"
            + full_json_str
            + "\n\nLet me know if you need adjustments."
        )
        assert extract_json(response) is not None

    def test_multiplos_jsons_retorna_o_primeiro_valido(self, bar_spec, line_spec):
        """
        Se o modelo retornar dois JSONs (ex: exemplo + resposta),
        o parser deve retornar o primeiro JSON válido.
        """
        response = json.dumps(bar_spec) + "\n\nAlternatively:\n" + json.dumps(line_spec)
        extracted = extract_json(response)
        parsed = parse_json(extracted)
        assert parsed["type"] == "bar"


# ---------------------------------------------------------------------------
# Bloco 3: Parser com resposta truncada
# ---------------------------------------------------------------------------

class TestParserRespostaTruncada:
    """
    Respostas truncadas (max_new_tokens muito baixo) resultam em JSONs
    incompletos. O parser deve retornar None em vez de falhar com exceção.
    """

    def test_json_truncado_no_meio_nao_retorna_spec_completo(self, full_json_str, bar_spec):
        # Corta o JSON ao meio — simula max_new_tokens ≈ 30 tokens.
        # O extract_json pode encontrar um sub-objeto JSON válido (ex: o campo "data")
        # mas esse sub-objeto NÃO deve ser aceito como um spec completo pelo spec_resolver,
        # pois não tem o campo "type" obrigatório.
        import pandas as pd
        truncated = _truncate_at_chars(full_json_str, len(full_json_str) // 2)
        extracted = extract_json(truncated)

        if extracted is not None:
            parsed = parse_json(extracted)
            # Um sub-objeto válido não deve ter "type" — logo não é um spec válido
            frame = pd.DataFrame({"Sales": [100.0], "Country": ["BR"]})
            from generator.spec_resolver import resolve_and_validate_visualization_payload
            normalized, error = resolve_and_validate_visualization_payload(parsed or {}, frame)
            assert normalized is None, (
                "Um JSON truncado ao meio não deve produzir um spec completo e válido"
            )

    def test_json_truncado_no_primeiro_quarto_retorna_none(self, full_json_str):
        # Corta muito cedo — simula max_new_tokens ≈ 10 tokens
        truncated = _truncate_at_chars(full_json_str, len(full_json_str) // 4)
        assert extract_json(truncated) is None

    def test_json_com_apenas_chave_abre_retorna_none(self):
        assert extract_json("{") is None

    def test_resposta_vazia_retorna_none(self):
        assert extract_json("") is None

    def test_texto_puro_sem_json_retorna_none(self):
        assert extract_json("I cannot generate a chart for this request.") is None


# ---------------------------------------------------------------------------
# Bloco 4: Pipeline com respostas de tamanhos variados
# ---------------------------------------------------------------------------

class TestPipelineComRespostasVariadas:
    """
    Testa como a ChartPipeline inteira (com mock) reage a respostas
    de diferentes tamanhos vindas do modelo.
    """

    def test_pipeline_processa_json_completo(self, sample_frame, bar_spec):
        pipeline = _make_pipeline_returning(json.dumps(bar_spec))
        result = pipeline.generate_visualization(sample_frame, "bar chart of sales by country")

        assert result.source == "model"
        assert result.spec.chart_type == "bar"

    def test_pipeline_usa_fallback_com_resposta_vazia(self, sample_frame):
        pipeline = _make_pipeline_returning("")
        result = pipeline.generate_visualization(sample_frame, "bar chart of sales by country")

        # Sem JSON válido, a pipeline deve usar o inferidor heurístico
        assert result.source == "fallback"

    def test_pipeline_usa_fallback_com_resposta_truncada(self, sample_frame, bar_spec):
        full = json.dumps(bar_spec)
        truncated = _truncate_at_chars(full, len(full) // 2)
        pipeline = _make_pipeline_returning(truncated)
        result = pipeline.generate_visualization(sample_frame, "bar chart of sales by country")

        assert result.source == "fallback"

    def test_pipeline_processa_json_com_prefixo_longo(self, sample_frame, bar_spec):
        """
        Simula modelo verboso que gera muito texto antes do JSON.
        O tamanho total da resposta é maior, mas o JSON está lá.
        """
        prefixo = "Sure! " * 50  # ~300 caracteres de prefixo
        response = prefixo + json.dumps(bar_spec)
        pipeline = _make_pipeline_returning(response)
        result = pipeline.generate_visualization(sample_frame, "bar chart of sales by country")

        assert result.source == "model"
        assert result.spec.chart_type == "bar"

    def test_pipeline_registra_warnings_para_resposta_invalida(self, sample_frame):
        pipeline = _make_pipeline_returning("not a json at all")
        result = pipeline.generate_visualization(sample_frame, "bar chart of sales by country")

        # Deve ter ao menos um warning registrado sobre a falha
        assert len(result.warnings) > 0

    def test_pipeline_com_json_de_tipo_invalido_usa_fallback(self, sample_frame, bar_spec):
        """
        JSON válido sintaticamente, mas com type não suportado.
        O spec_resolver rejeita, a pipeline deve cair no fallback.
        """
        spec_invalido = {**bar_spec, "type": "table"}
        pipeline = _make_pipeline_returning(json.dumps(spec_invalido))
        result = pipeline.generate_visualization(sample_frame, "bar chart of sales by country")

        assert result.source == "fallback"

    def test_pipeline_com_coluna_inexistente_usa_fallback(self, sample_frame, bar_spec):
        """
        JSON com coluna que não existe no dataset.
        O spec_resolver rejeita por coluna inválida.
        """
        spec_invalido = {
            **bar_spec,
            "data": {**bar_spec["data"], "dimension": "COLUNA_QUE_NAO_EXISTE"},
        }
        pipeline = _make_pipeline_returning(json.dumps(spec_invalido))
        result = pipeline.generate_visualization(sample_frame, "bar chart")

        assert result.source == "fallback"
