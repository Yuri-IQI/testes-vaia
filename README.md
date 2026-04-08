# VAIA - Visualizacao Assistida por IA para datasets reais

O `testes-vaia` agora funciona como um assistente de visualizacao orientado a
dataset real.

Em vez de inventar `labels` e `values` a partir do prompt, o sistema:

1. recebe um dataset CSV
2. carrega os dados com `pandas`
3. resume a estrutura do dataframe
4. envia esse resumo junto com o pedido do usuario para a IA
5. recebe uma especificacao JSON baseada apenas em colunas existentes
6. valida essa especificacao
7. agrega os dados e gera um grafico `line`, `bar` ou `pie`

O projeto preserva a essencia original do VAIA:
usar IA para traduzir linguagem natural em uma especificacao de visualizacao.

## O que o projeto faz agora

- Upload de dataset CSV na interface principal
- Gera apenas `line`, `bar` e `pie`
- Usa apenas colunas reais do dataset
- Não inventa valores
- Valida colunas, agregacoes e combinacoes invalidas
- Faz fallback heuristico se o modelo nao estiver disponivel

## Formato da especificacao gerada

```json
{
  "type": "line",
  "data": {
    "dimension": "ORDERDATE",
    "metric": "SALES",
    "aggregation": "sum",
    "color": "PRODUCTLINE"
  },
  "title": "Sales trend by product line",
  "description": "Shows how sales evolve over time by product line.",
  "explanation": "A line chart is appropriate for time-based trends."
}
```

## Dataset de exemplo

O repositorio inclui `sample_data/sample_sales_data.csv`, um dataset sintetico
de vendas com colunas inspiradas em exemplos classicos de dados comerciais.

Ele existe para facilitar comparacoes com a abordagem baseada em dataset que
voce descreveu anteriormente.

## Configuracao do ambiente

Crie e ative um ambiente virtual:

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Linux / Mac:

```bash
source venv/bin/activate
```

Instale as dependencias:

```bash
pip install -r requirements.txt
```

## Streamlit

Execute:

```bash
streamlit run app.py
```

Fluxo:

- envie um CSV ou use o dataset de exemplo embutido
- escreva um pedido em linguagem natural
- veja o grafico, a especificacao JSON e os dados agregados usados

Exemplos de prompts:

- `Compare total sales by country in a bar chart and split by product line.`
- `Show the sales trend over time in a line chart.`
- `Show how each product line contributes to total sales in a pie chart.`
- `Show the average sales by deal size in a bar chart.`
- `Count orders by status in a bar chart.`

## Matplotlib

Execute:

```bash
python matplot.py --dataset sample_data/sample_sales_data.csv --prompt "Compare total sales by country in a bar chart and split by product line."
```

O script gera a especificacao a partir do dataset, renderiza o grafico com
Matplotlib e salva o resultado em `outputs/dataset_chart.png`.

## API + D3.js

Suba a API:

```bash
uvicorn api:app --reload
```

Principais endpoints:

- `GET /health`
- `GET /examples`
- `GET /sample-dataset`
- `POST /generate`

O endpoint `POST /generate` recebe um JSON com:

- `prompt`
- `csv_text`
- `filename`

Em outro terminal, abra o cliente web:

```bash
cd sample_client
python -m http.server 8080
```

Depois acesse:

```text
http://localhost:8080
```

O cliente web permite subir um CSV, ler o conteudo localmente, enviar esse
conteudo para a API e renderizar o resultado com D3.js.

## Estrutura do projeto

```text
.
|-- api.py
|-- app.py
|-- chart_pipeline.py
|-- chart_utils.py
|-- code_assistant.py
|-- examples.py
|-- json_parser.py
|-- matplot.py
|-- requirements.txt
|-- sample_data
|   `-- sample_sales_data.csv
`-- sample_client
    |-- index.html
    `-- main.js
```

## Como a IA e usada

O modelo recebe:

- resumo do dataframe
- tipos de coluna
- amostra de valores
- pedido do usuario

Ele nao recebe o dataset completo.

O prompt do sistema foi restringido para:

- usar apenas colunas existentes
- escolher apenas `line`, `bar` e `pie`
- escolher apenas `sum`, `mean` e `count`
- nao inventar colunas nem valores
- evitar `color` em `pie`

## Fallback

Se o modelo nao estiver disponivel ou gerar uma resposta invalida, o projeto
usa uma heuristica local para:

- escolher o tipo de grafico
- identificar colunas mais provaveis
- aplicar uma agregacao coerente

Assim o fluxo continua funcional mesmo sem o modelo carregado.

## Limitacoes atuais

- Apenas CSV e suportado no upload neste momento.
- A qualidade da especificacao depende da clareza do prompt e da qualidade do resumo do dataset.
- O fallback e util, mas menos inteligente que o modelo.

## Proximos passos naturais

- adicionar suporte a XLSX e JSON
- melhorar a deteccao de colunas temporais
- suportar mais opcoes visuais no schema
- adicionar testes automatizados
