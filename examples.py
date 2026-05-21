import json
from summarizer.summaries.summary_dados_desenrola import desenrola_summary

SUMMARY = desenrola_summary

EXAMPLES = [
    {
        "request": "Mostre a evolução do volume de operações ao longo do tempo.",
        "response": {
            "type": "line",
            "data": {"dimension": "DATA_BASE", "metric": "VOLUME_OPERACOES", "aggregation": "sum"},
            "title": "Volume de operações ao longo do tempo",
            "description": "Mostra como o volume total renegociado evoluiu mês a mês.",
            "explanation": "Gráfico de linha é ideal para tendências temporais usando DATA_BASE.",
        },
    },
    {
        "request": "Como o número de operações variou ao longo dos meses?",
        "response": {
            "type": "line",
            "data": {"dimension": "DATA_BASE", "metric": "NUMERO_OPERACOES", "aggregation": "sum"},
            "title": "Número de operações por mês",
            "description": "Evolução mensal da quantidade de operações do Desenrola.",
            "explanation": "Linha temporal com DATA_BASE como dimensão e NUMERO_OPERACOES como métrica.",
        },
    },
    {
        "request": "Tendência do volume médio por mês separado por tipo do Desenrola.",
        "response": {
            "type": "line",
            "data": {"dimension": "DATA_BASE", "metric": "VOLUME_OPERACOES", "aggregation": "mean", "color": "TIPO_DESENROLA"},
            "title": "Volume médio por mês e tipo do Desenrola",
            "description": "Compara a evolução do volume médio entre os dois tipos ao longo do tempo.",
            "explanation": "Cor separa os dois tipos do programa mantendo a linha do tempo como eixo principal.",
        },
    },

    {
        "request": "Qual estado tem o maior volume de operações?",
        "response": {
            "type": "bar",
            "data": {"dimension": "UNIDADE_FEDERACAO", "metric": "VOLUME_OPERACOES", "aggregation": "sum"},
            "title": "Volume total de operações por estado",
            "description": "Compara o volume renegociado em cada unidade da federação.",
            "explanation": "Barras permitem comparar totais entre categorias como estados.",
        },
    },
    {
        "request": "Compare o número de operações por banco.",
        "response": {
            "type": "bar",
            "data": {"dimension": "NOME_CONGLOMERADO_FINANCEIRO", "metric": "NUMERO_OPERACOES", "aggregation": "sum"},
            "title": "Número de operações por conglomerado financeiro",
            "description": "Total de operações renegociadas por instituição financeira.",
            "explanation": "Barras por instituição tornam clara a participação de cada banco.",
        },
    },
    {
        "request": "Volume por estado separado por tipo do Desenrola em barras.",
        "response": {
            "type": "bar",
            "data": {"dimension": "UNIDADE_FEDERACAO", "metric": "VOLUME_OPERACOES", "aggregation": "sum", "color": "TIPO_DESENROLA"},
            "title": "Volume por estado e tipo do Desenrola",
            "description": "Compara o volume em cada estado separando os dois tipos do programa.",
            "explanation": "Cor para TIPO_DESENROLA dentro de cada barra de estado.",
        },
    },
    {
        "request": "Número de operações por banco separado por tipo.",
        "response": {
            "type": "bar",
            "data": {"dimension": "NOME_CONGLOMERADO_FINANCEIRO", "metric": "NUMERO_OPERACOES", "aggregation": "sum", "color": "TIPO_DESENROLA"},
            "title": "Operações por banco e tipo do Desenrola",
            "description": "Quantidade de operações por instituição financeira separadas por tipo.",
            "explanation": "Agrupamento por cor revela como cada banco distribui seus dois tipos de operação.",
        },
    },

    {
        "request": "Qual a participação de cada banco no volume total?",
        "response": {
            "type": "pie",
            "data": {"dimension": "NOME_CONGLOMERADO_FINANCEIRO", "metric": "VOLUME_OPERACOES", "aggregation": "sum"},
            "title": "Participação dos bancos no volume total",
            "description": "Proporção do volume renegociado por conglomerado financeiro.",
            "explanation": "Pizza evidencia a composição e dominância de cada banco no total.",
        },
    },
    {
        "request": "Como o volume se divide entre os tipos do Desenrola?",
        "response": {
            "type": "pie",
            "data": {"dimension": "TIPO_DESENROLA", "metric": "VOLUME_OPERACOES", "aggregation": "sum"},
            "title": "Distribuição do volume por tipo do Desenrola",
            "description": "Proporção do volume total entre os tipos 1 e 2 do programa.",
            "explanation": "Pizza é adequada para mostrar a divisão entre dois grupos.",
        },
    },
    {
        "request": "Mostre a fatia de cada estado no número total de operações.",
        "response": {
            "type": "pie",
            "data": {"dimension": "UNIDADE_FEDERACAO", "metric": "NUMERO_OPERACOES", "aggregation": "sum"},
            "title": "Participação dos estados no número de operações",
            "description": "Proporção de operações por unidade da federação.",
            "explanation": "Pizza mostra a composição geográfica das operações do Desenrola.",
        },
    },
]


def format_for_training() -> list[dict]:
    formatted = []
    for ex in EXAMPLES:
        user_input = (
            f"Dataset summary:\n{json.dumps(SUMMARY, indent=2, ensure_ascii=False)}\n\n"
            f'User request: "{ex["request"]}"\n\n'
            "Return only valid JSON."
        )
        formatted.append({
            "text": (
                "### Instruction:\n"
                "You are a chart specification assistant. "
                "Given a dataset summary and a user request, return a valid JSON chart spec.\n\n"
                f"### Input:\n{user_input}\n\n"
                f"### Response:\n{json.dumps(ex['response'], indent=2, ensure_ascii=False)}"
            )
        })
    return formatted

def build_examples_block() -> str:
    lines = []
    for ex in EXAMPLES:
        lines.append(f"User request: {ex['request']}")
        lines.append("JSON response:")
        lines.append(json.dumps(ex["response"], indent=2, ensure_ascii=False))
        lines.append("")
    return "\n".join(lines).strip()