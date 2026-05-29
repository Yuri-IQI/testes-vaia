Mudar env de unicode no cmd:
```
set PYTHONUTF8=1
```

no powershell:
```
$env:PYTHONUTF8 = "1"
```

Comando para treinar o modelo:
```
python -m train.py
```

Teste com matplot:
```
python -m matplot.py --prompt "make a chart" --adapter financial_adapter
```

pip install torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu124


Como rodar projeto de testes

# Só unitários (rápido, sem modelo):
& $python -m pytest tests/ --ignore=tests/integration/ -v

# Só integração (lento, carrega o Qwen):
& $python -m pytest tests/integration/ -v -s

# Tudo:
& $python -m pytest -v -s


$python = "C:.../.venv\Scripts\python.exe"
& $python -m pytest tests/integration/ -v -s --tb=short