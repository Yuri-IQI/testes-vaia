# Visualização Assistida por IA (VAIA)

Este repositório contém experimentos de integração de um modelo de IA leve  
(**Qwen/Qwen2.5-Coder-1.5B-Instruct**) com bibliotecas de visualização de dados em Python e JavaScript.

O objetivo é avaliar a capacidade do modelo de gerar código para criação de gráficos a partir de descrições em linguagem natural.

---

# Configuração do Ambiente

Antes de executar qualquer script, é necessário criar e ativar um ambiente virtual.

```bash
python -m venv venv
```

Ative o ambiente virtual:

Linux / Mac:
```bash
source venv/bin/activate
```

Windows:
```bash
venv\Scripts\activate
```

Em seguida, instale as dependências:

```bash
pip install -r requirements.txt
```

---

# Matplotlib

No arquivo `matplot.py` há um script simples que utiliza um loop para enviar um prompt ao assistente.  
Caso ocorra algum erro durante a execução do código gerado, o script tenta novamente informando a mensagem de erro ao modelo.

Nesse script, o prompt é definido diretamente no código na chamada da função `execute_code`, junto de um número máximo de tentativas.  
Devido a esse processo iterativo de geração e execução de código, esse script costuma demorar mais que os demais.

Para executá-lo:

```bash
python -m matplot.py
```

---

# Streamlit

No arquivo `app.py` existe uma aplicação simples construída com **Streamlit**.

Ela cria uma interface web onde é possível inserir um prompt em linguagem natural para gerar um gráfico.  
O gráfico gerado é exibido na página juntamente com o código utilizado para produzi-lo.

Para executar a aplicação:

```bash
streamlit run app.py
```

---

# API + D3.js

O arquivo `api.py` contém uma API construída com **FastAPI** que disponibiliza um endpoint para geração de código utilizando o modelo de IA.

A ideia dessa abordagem é permitir que o código gerado pela IA seja utilizado em uma página web para criar visualizações gráficas com **D3.js**.  
Um exemplo de cliente web pode ser encontrado na pasta `sample_client`.

Essa abordagem apresenta maior complexidade em comparação às anteriores, principalmente devido a:

- dificuldade de padronizar as respostas do modelo
- necessidade de estruturar corretamente os dados para que o código JavaScript consiga renderizar os gráficos

---

## Executando a API

Inicie a API com:

```bash
uvicorn api:app --reload
```

---

## Executando o cliente web de exemplo

Abra outro terminal e execute:

```bash
cd sample_client
python -m http.server 8080
```

Depois acesse no navegador:

```
http://localhost:8080
```

---

# Estrutura do Projeto

```
.
├── api.py
├── app.py
├── matplot.py
├── code_assistant.py
├── requirements.txt
└── sample_client
    ├── index.html
    └── main.js
```

---

# Modelo Utilizado

O projeto utiliza o modelo:

**Qwen/Qwen2.5-Coder-1.5B-Instruct**

Esse é um modelo leve voltado para geração de código, capaz de produzir scripts para bibliotecas de visualização de dados a partir de descrições em linguagem natural.

---

# Objetivo

O objetivo principal deste repositório é investigar o uso de **modelos de linguagem pequenos (SLMs)** na geração automática de visualizações de dados e avaliar diferentes abordagens de integração com ferramentas de visualização.
