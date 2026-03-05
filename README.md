# Visualização Assistida por IA (VAIA)

Esse repositório contém testes de integração de um modelo de IA leve (Qwen/Qwen2.5-Coder-1.5B-Instruct) a bibliotecas de visualização de dados.

Antes de executar qualquer script é necessário entrar em um ambiente virtual:
```
python -m venv venv
source venv/bin/activate   # linux/mac
venv\Scripts\activate      # windows
```
e instalar as dependências no requirements.txt

```
pip install -r requirements.txt
```

## Matplotlib
No arquivo matplot.py, existe um script simples que utiliza um loop para enviar um promp para o assistente e tentar novamente informando uma mensagem de erro caso algum problema aconteça.
Nesse script o prompt é informado no código na chamada da função execute_code, junto de um número máximo de tentativas, por conta dessa forma de gerar os gráficos esse script custuma demorar mais que os demais.

Para executa-lo, apenas rode:
```
python -m matplot.py
```

## Streamlit
Em app.py, se encontra um script que utiliza o streamlit para criar uma página onde é possível informar um prompt para gerar um gráfico que aparecerá na tela junto do código que o gerou.

Para executa-lo, apenas rode:
```
streamlit run app.py
```

## API + D3.js
Em api.py se encontra um código que disponibiliza uma chamada a geração de prompt da IA por meio de um endpoint do FastAPI.
A intenção aqui é que fosse possível utilizar o código gerado pela IA em uma página web, que se encontra na pasta sample_client, e renderizar uma visualização gráfica por meio do D3.js.
No entanto, essa abordagem apresenta uma complicação maior que os anteriores, devido a dificuldade de padronizar as respostas da IA e de preparar o código dos gráficos para recebe-la.

Para testar essa abordagem, inicie a api com o comando:
```
uvicorn api:app --reload
```

e em seguida inicie o sample_client com:
```
cd sample_client

python -m http.server 8080
```
