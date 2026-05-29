# Resultados dos Testes de Integração — Baseline (sem fine-tuning)

**Data:** 29/05/2026  
**Modelo:** Qwen/Qwen2.5-0.5B-Instruct (base, sem adapter LoRA)  
**Adapter:** `financial_adapter/` — não treinado (apenas README presente)  
**Duração total:** 45 minutos (2724s)  
**Resultado geral:** 23 passed / 16 failed

---

## Resumo por grupo

| Grupo | Tipo correto | Fonte: modelo | Fonte: fallback | Consistência entre variações |
|---|---|---|---|---|
| BAR (4 prompts)  | 4/4 ✅ | 0/4 ❌ | 4/4 | ✅ consistente (via fallback) |
| LINE (4 prompts) | 4/4 ✅ | 0/4 ❌ | 4/4 | ✅ consistente (via fallback) |
| PIE (4 prompts)  | 2/4 ❌ | 0/4 ❌ | 4/4 | ❌ inconsistente (pie/histogram/bar) |

**Taxa de acerto direto do modelo (source = "model"):** 0% — o modelo base não gerou nenhum JSON válido.  
**Taxa de uso do fallback heurístico:** 100%.

---

## Análise das respostas brutas do modelo

O modelo base gerou saídas completamente incoerentes em todos os prompts. Exemplos reais capturados:

```
样本samples_sample样本(samplessamplessamplessample...
"]];
"]];
"]];
高高,高高,祯,高Sheet,rio,排气学家,urette二uya...
```

Padrões observados:
- Repetição infinita de tokens (`"]];`, `samplesamplesample...`)
- Tokens em chinês, árabe e outros idiomas sem relação com o prompt
- Ausência total de estrutura JSON

**Diagnóstico:** o modelo base Qwen (0.5B) sem fine-tuning não possui conhecimento do formato de especificação JSON do VAIA. A ausência do adapter treinado (`financial_adapter/`) é a causa direta — o `train.py` precisa ser executado para gerar os pesos LoRA.

---

## Análise do fallback heurístico

Com o modelo falhando em 100% dos casos, o sistema dependeu inteiramente do `fallback_inferrer.py`, que detecta o tipo de gráfico por palavras-chave no prompt.

### Onde o fallback funcionou

| Tipo | Por quê funcionou |
|---|---|
| BAR | Prompts contêm "bar chart", "bar graph", "bars" — mapeados diretamente por `BAR_HINTS` |
| LINE | Prompts contêm "line chart", "line graph", "over time", "timeline" — cobertos por `LINE_HINTS` |

### Onde o fallback falhou

| Prompt | Tipo esperado | Tipo obtido | Causa |
|---|---|---|---|
| "Display the close price **distribution** by stock index as a pie" | pie | histogram | `"distribution"` está em `HISTOGRAM_HINTS` |
| "Show the **proportion** of close price per stock index in a pie" | pie | bar | `"proportion"` não está em `PIE_HINTS` |

Os prompts de pie que **funcionaram** no fallback foram os que continham as palavras "pie chart" ou "pie" explicitamente, que estão mapeadas em `PIE_HINTS`. Os que usaram linguagem semântica ("distribution", "proportion") foram classificados incorretamente.

---

## Testes que passaram (23)

Todos os 23 testes aprovados correspondem a casos em que o fallback heurístico produziu o tipo correto:

- `TestModelBarPrompts::test_chart_type_e_bar` — 4/4 (fallback acertou o tipo)
- `TestModelBarPrompts::test_dimensao_e_stock_index` — 3/4 (fallback escolheu Stock Index)
- `TestModelLinePrompts::test_chart_type_e_line` — 4/4 (fallback acertou o tipo)
- `TestModelLinePrompts::test_dimensao_e_date` — 4/4 (fallback escolheu Date para séries temporais)
- `TestModelPiePrompts::test_chart_type_e_pie` — 2/4 (apenas prompts com "pie" explícito)
- `TestConsistenciaEntreVariacoes::test_bar_consistencia_e_fallback` — ✅
- `TestConsistenciaEntreVariacoes::test_line_consistencia_e_fallback` — ✅

## Testes que falharam (16)

| Teste | Motivo |
|---|---|
| `test_nao_usou_fallback` (BAR × 4) | Modelo gerou lixo → 100% fallback |
| `test_nao_usou_fallback` (LINE × 4) | Modelo gerou lixo → 100% fallback |
| `test_nao_usou_fallback` (PIE × 4) | Modelo gerou lixo → 100% fallback |
| `test_metrica_e_close_price` (BAR × 1) | Fallback escolheu "Crude Oil Price" em vez de "Close Price" |
| `test_chart_type_e_pie` (PIE × 2) | Fallback classificou "distribution" como histogram e "proportion" como bar |
| `test_pie_consistencia_e_fallback` | Fallback gerou 3 tipos diferentes (pie, histogram, bar) para o mesmo grupo |

---

## Conclusões

### 1. O fine-tuning é indispensável

O modelo base é incapaz de gerar o formato de especificação JSON do VAIA. Sem o adapter LoRA treinado, o modelo produz saídas sem estrutura e sem relação com o prompt. Isso confirma que o fine-tuning com os exemplos do `examples.py` é o componente central do sistema — não um incremento opcional.

### 2. O fallback é eficaz para linguagem direta, frágil para linguagem semântica

O mecanismo heurístico funciona bem quando o prompt usa as mesmas palavras-chave que os hints (`BAR_HINTS`, `LINE_HINTS`, `PIE_HINTS`). Falha quando o usuário usa sinônimos semânticos como "distribution" ou "proportion" para pedir um pie chart. Isso representa uma limitação documentada do fallback que o fine-tuning deve suprir.

### 3. Próximo passo: execução do fine-tuning

Após rodar `python train.py` e gerar os pesos em `financial_adapter/`, os mesmos testes devem ser re-executados. O resultado esperado é:

- `test_nao_usou_fallback` passando — modelo gerando JSON válido
- `test_pie_consistencia_e_fallback` passando — modelo consistente entre variações semânticas
- Taxa de `source == "model"` aumentando de 0% para um valor mensurável

A comparação entre este baseline e os resultados pós-fine-tuning constitui a evidência experimental central do projeto.

---

## Comando utilizado para gerar estes resultados

```powershell
$python = "C:\Users\Pedro\Documents\Codigos\python\IA-VAIA\.venv\Scripts\python.exe"
& $python -m pytest tests/integration/ -v -s --tb=short
```
