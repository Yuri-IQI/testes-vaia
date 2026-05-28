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