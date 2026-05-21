desenrola_summary = {
  "row_count": 10412,
  "column_count": 7,
  "numeric_columns": [
    "TIPO_DESENROLA",
    "NUMERO_OPERACOES",
    "VOLUME_OPERACOES"
  ],
  "categorical_columns": [
    "UNIDADE_FEDERACAO",
    "COD_CONGLOMERADO_FINANCEIRO",
    "NOME_CONGLOMERADO_FINANCEIRO"
  ],
  "datetime_columns": [
    "DATA_BASE"
  ],
  "columns": [
    {
      "name": "DATA_BASE",
      "dtype": "datetime64[ns]",
      "semantic_type": "datetime",
      "non_null": 10412,
      "unique_values": 31,
      "sample_values": [
        "2023-09-01T00:00:00",
        "2023-09-01T00:00:00",
        "2023-09-01T00:00:00",
        "2023-09-01T00:00:00"
      ]
    },
    {
      "name": "TIPO_DESENROLA",
      "dtype": "int64",
      "semantic_type": "numeric",
      "non_null": 10412,
      "unique_values": 3,
      "sample_values": [
        2,
        2,
        2,
        2
      ],
      "min": 1,
      "max": 3
    },
    {
      "name": "UNIDADE_FEDERACAO",
      "dtype": "object",
      "semantic_type": "categorical",
      "non_null": 10412,
      "unique_values": 27,
      "sample_values": [
        "AC",
        "AC",
        "AC",
        "AC"
      ]
    },
    {
      "name": "COD_CONGLOMERADO_FINANCEIRO",
      "dtype": "object",
      "semantic_type": "categorical",
      "non_null": 10412,
      "unique_values": 73,
      "sample_values": [
        "49906",
        "10045",
        "49944",
        "51626"
      ]
    },
    {
      "name": "NOME_CONGLOMERADO_FINANCEIRO",
      "dtype": "object",
      "semantic_type": "categorical",
      "non_null": 10412,
      "unique_values": 76,
      "sample_values": [
        "BB",
        "BRADESCO",
        "BTG PACTUAL",
        "CAIXA ECONÔMICA FEDERAL"
      ]
    },
    {
      "name": "NUMERO_OPERACOES",
      "dtype": "int64",
      "semantic_type": "numeric",
      "non_null": 10412,
      "unique_values": 1288,
      "sample_values": [
        140,
        15,
        7,
        81
      ],
      "min": 1,
      "max": 46391
    },
    {
      "name": "VOLUME_OPERACOES",
      "dtype": "float64",
      "semantic_type": "numeric",
      "non_null": 10412,
      "unique_values": 10265,
      "sample_values": [
        1418395.99,
        83829.79,
        37788.79,
        246145.92
      ],
      "min": 0.01,
      "max": 215271484.82
    }
  ],
  "sample_rows": [
    {
      "DATA_BASE": "2023-09-01T00:00:00",
      "TIPO_DESENROLA": 2,
      "UNIDADE_FEDERACAO": "AC",
      "COD_CONGLOMERADO_FINANCEIRO": "49906",
      "NOME_CONGLOMERADO_FINANCEIRO": "BB",
      "NUMERO_OPERACOES": 140,
      "VOLUME_OPERACOES": 1418395.99
    },
    {
      "DATA_BASE": "2023-09-01T00:00:00",
      "TIPO_DESENROLA": 2,
      "UNIDADE_FEDERACAO": "AC",
      "COD_CONGLOMERADO_FINANCEIRO": "10045",
      "NOME_CONGLOMERADO_FINANCEIRO": "BRADESCO",
      "NUMERO_OPERACOES": 15,
      "VOLUME_OPERACOES": 83829.79
    },
    {
      "DATA_BASE": "2023-09-01T00:00:00",
      "TIPO_DESENROLA": 2,
      "UNIDADE_FEDERACAO": "AC",
      "COD_CONGLOMERADO_FINANCEIRO": "49944",
      "NOME_CONGLOMERADO_FINANCEIRO": "BTG PACTUAL",
      "NUMERO_OPERACOES": 7,
      "VOLUME_OPERACOES": 37788.79
    },
    {
      "DATA_BASE": "2023-09-01T00:00:00",
      "TIPO_DESENROLA": 2,
      "UNIDADE_FEDERACAO": "AC",
      "COD_CONGLOMERADO_FINANCEIRO": "51626",
      "NOME_CONGLOMERADO_FINANCEIRO": "CAIXA ECONÔMICA FEDERAL",
      "NUMERO_OPERACOES": 81,
      "VOLUME_OPERACOES": 246145.92
    },
    {
      "DATA_BASE": "2023-09-01T00:00:00",
      "TIPO_DESENROLA": 2,
      "UNIDADE_FEDERACAO": "AC",
      "COD_CONGLOMERADO_FINANCEIRO": "51884",
      "NOME_CONGLOMERADO_FINANCEIRO": "INTER",
      "NUMERO_OPERACOES": 4,
      "VOLUME_OPERACOES": 12306.86
    }
  ]
}