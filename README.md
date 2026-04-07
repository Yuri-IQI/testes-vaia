# VAIA - Visualizacao Assistida por IA

Este repositorio reune experimentos de integracao entre um modelo pequeno de IA
e bibliotecas de visualizacao de dados em Python e JavaScript.

O objetivo e transformar pedidos em linguagem natural, como "bar chart with values
sales: 12, support: 7, product: 15", em visualizacoes funcionais.

O projeto cobre tres abordagens:

1. `app.py`: aplicacao Streamlit que gera um JSON de grafico e renderiza com Plotly.
2. `matplot.py`: script de linha de comando que gera codigo Matplotlib e tenta
   executar novamente caso a execucao falhe.
3. `api.py` + `sample_client/`: API com FastAPI e um cliente web em D3.js.

## Como funciona

O fluxo principal usa o modelo `Qwen/Qwen2.5-Coder-1.5B-Instruct` por meio do
arquivo `code_assistant.py`.

Para manter o projeto funcional mesmo sem o modelo carregado, existe um fallback
heuristico que interpreta o prompt e monta a estrutura do grafico localmente.

Isso significa que:

- com o modelo configurado, o projeto tenta usar IA para gerar a resposta
- sem o modelo, a aplicacao continua funcionando com regras locais

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

A interface permite digitar um prompt em linguagem natural, gerar o grafico e
inspecionar tanto o JSON final quanto a resposta bruta.

## Matplotlib

Execute:

```bash
python matplot.py --prompt "line chart with values jan: 5, feb: 8, mar: 13"
```

O script salva a imagem em `outputs/matplotlib_chart.png` por padrao e mostra o
codigo usado para gerar a figura.

## API + D3.js

Suba a API:

```bash
uvicorn api:app --reload
```

Em outro terminal, abra o cliente web:

```bash
cd sample_client
python -m http.server 8080
```

Depois acesse:

```text
http://localhost:8080
```

O cliente envia o prompt para a API e renderiza o grafico com D3.js.

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
`-- sample_client
    |-- index.html
    `-- main.js
```

## Observacoes

- O carregamento do modelo pode consumir bastante memoria.
- Se o modelo nao estiver disponivel localmente, o fallback heuristico sera usado.
- O cliente `sample_client` consome o endpoint `POST /generate` e exibe tambem
  o snippet JavaScript retornado pela API.
