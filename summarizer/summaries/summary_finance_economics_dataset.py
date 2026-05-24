dataset_summary = {
  "row_count": 3000,
  "column_count": 24,
  "numeric_columns": [
    "Open Price",
    "Close Price",
    "Daily High",
    "Daily Low",
    "Trading Volume",
    "GDP Growth (%)",
    "Inflation Rate (%)",
    "Unemployment Rate (%)",
    "Interest Rate (%)",
    "Consumer Confidence Index",
    "Government Debt (Billion USD)",
    "Corporate Profits (Billion USD)",
    "Forex USD/EUR",
    "Forex USD/JPY",
    "Crude Oil Price (USD per Barrel)",
    "Gold Price (USD per Ounce)",
    "Real Estate Index",
    "Retail Sales (Billion USD)",
    "Bankruptcy Rate (%)",
    "Mergers & Acquisitions Deals",
    "Venture Capital Funding (Billion USD)",
    "Consumer Spending (Billion USD)"
  ],
  "categorical_columns": [
    "Stock Index"
  ],
  "datetime_columns": [
    "Date"
  ],
  "columns": [
    {
      "name": "Date",
      "dtype": "datetime64[ns]",
      "semantic_type": "datetime",
      "non_null": 3000,
      "unique_values": 3000,
      "sample_values": [
        "2000-01-01T00:00:00",
        "2000-01-02T00:00:00",
        "2000-01-03T00:00:00",
        "2000-01-04T00:00:00"
      ]
    },
    {
      "name": "Stock Index",
      "dtype": "object",
      "semantic_type": "categorical",
      "non_null": 3000,
      "unique_values": 3,
      "sample_values": [
        "Dow Jones",
        "S&P 500",
        "Dow Jones",
        "Dow Jones"
      ]
    },
    {
      "name": "Open Price",
      "dtype": "float64",
      "semantic_type": "numeric",
      "non_null": 3000,
      "unique_values": 2987,
      "sample_values": [
        2128.75,
        2046.82,
        1987.92,
        4625.02
      ],
      "min": 1000.05,
      "max": 4998.23
    },
    {
      "name": "Close Price",
      "dtype": "float64",
      "semantic_type": "numeric",
      "non_null": 3000,
      "unique_values": 2981,
      "sample_values": [
        2138.48,
        2036.18,
        1985.26,
        4660.47
      ],
      "min": 954.52,
      "max": 5034.129999999999
    },
    {
      "name": "Daily High",
      "dtype": "float64",
      "semantic_type": "numeric",
      "non_null": 3000,
      "unique_values": 2994,
      "sample_values": [
        2143.7,
        2082.83,
        2022.28,
        4665.26
      ],
      "min": 1012.13,
      "max": 5076.19
    },
    {
      "name": "Daily Low",
      "dtype": "float64",
      "semantic_type": "numeric",
      "non_null": 3000,
      "unique_values": 2992,
      "sample_values": [
        2100.55,
        2009.53,
        1978.37,
        4595.46
      ],
      "min": 917.17,
      "max": 4977.06
    },
    {
      "name": "Trading Volume",
      "dtype": "int64",
      "semantic_type": "numeric",
      "non_null": 3000,
      "unique_values": 3000,
      "sample_values": [
        2670411,
        690220415,
        315284661,
        13098297
      ],
      "min": 1636024,
      "max": 999977078
    },
    {
      "name": "GDP Growth (%)",
      "dtype": "float64",
      "semantic_type": "numeric",
      "non_null": 3000,
      "unique_values": 1312,
      "sample_values": [
        -0.37,
        3.19,
        5.54,
        10.0
      ],
      "min": -5.0,
      "max": 10.0
    },
    {
      "name": "Inflation Rate (%)",
      "dtype": "float64",
      "semantic_type": "numeric",
      "non_null": 3000,
      "unique_values": 959,
      "sample_values": [
        6.06,
        4.95,
        9.13,
        3.77
      ],
      "min": 0.01,
      "max": 10.0
    },
    {
      "name": "Unemployment Rate (%)",
      "dtype": "float64",
      "semantic_type": "numeric",
      "non_null": 3000,
      "unique_values": 1169,
      "sample_values": [
        6.1,
        6.62,
        2.6,
        2.2
      ],
      "min": 2.0,
      "max": 15.0
    },
    {
      "name": "Interest Rate (%)",
      "dtype": "float64",
      "semantic_type": "numeric",
      "non_null": 3000,
      "unique_values": 915,
      "sample_values": [
        6.06,
        2.19,
        0.82,
        3.71
      ],
      "min": 0.5,
      "max": 10.0
    },
    {
      "name": "Consumer Confidence Index",
      "dtype": "int64",
      "semantic_type": "numeric",
      "non_null": 3000,
      "unique_values": 70,
      "sample_values": [
        114,
        101,
        92,
        112
      ],
      "min": 50,
      "max": 119
    },
    {
      "name": "Government Debt (Billion USD)",
      "dtype": "int64",
      "semantic_type": "numeric",
      "non_null": 3000,
      "unique_values": 2850,
      "sample_values": [
        27271,
        16160,
        29962,
        12745
      ],
      "min": 503,
      "max": 29991
    },
    {
      "name": "Corporate Profits (Billion USD)",
      "dtype": "int64",
      "semantic_type": "numeric",
      "non_null": 3000,
      "unique_values": 2208,
      "sample_values": [
        1645,
        1008,
        4562,
        4183
      ],
      "min": 100,
      "max": 4999
    },
    {
      "name": "Forex USD/EUR",
      "dtype": "float64",
      "semantic_type": "numeric",
      "non_null": 3000,
      "unique_values": 71,
      "sample_values": [
        1.04,
        1.0,
        0.83,
        0.95
      ],
      "min": 0.8,
      "max": 1.5
    },
    {
      "name": "Forex USD/JPY",
      "dtype": "float64",
      "semantic_type": "numeric",
      "non_null": 3000,
      "unique_values": 2414,
      "sample_values": [
        119.87,
        98.22,
        80.13,
        149.15
      ],
      "min": 80.01,
      "max": 149.96
    },
    {
      "name": "Crude Oil Price (USD per Barrel)",
      "dtype": "float64",
      "semantic_type": "numeric",
      "non_null": 3000,
      "unique_values": 2667,
      "sample_values": [
        47.2,
        52.84,
        78.8,
        28.18
      ],
      "min": 20.04,
      "max": 149.87
    },
    {
      "name": "Gold Price (USD per Ounce)",
      "dtype": "float64",
      "semantic_type": "numeric",
      "non_null": 3000,
      "unique_values": 2972,
      "sample_values": [
        1052.34,
        1957.73,
        2339.49,
        1308.54
      ],
      "min": 800.16,
      "max": 2499.66
    },
    {
      "name": "Real Estate Index",
      "dtype": "float64",
      "semantic_type": "numeric",
      "non_null": 3000,
      "unique_values": 2887,
      "sample_values": [
        390.23,
        346.23,
        439.46,
        213.07
      ],
      "min": 100.13,
      "max": 499.92
    },
    {
      "name": "Retail Sales (Billion USD)",
      "dtype": "int64",
      "semantic_type": "numeric",
      "non_null": 3000,
      "unique_values": 2582,
      "sample_values": [
        2229,
        4156,
        340,
        8456
      ],
      "min": 107,
      "max": 9998
    },
    {
      "name": "Bankruptcy Rate (%)",
      "dtype": "float64",
      "semantic_type": "numeric",
      "non_null": 3000,
      "unique_values": 952,
      "sample_values": [
        2.12,
        1.4,
        0.79,
        4.22
      ],
      "min": 0.01,
      "max": 10.0
    },
    {
      "name": "Mergers & Acquisitions Deals",
      "dtype": "int64",
      "semantic_type": "numeric",
      "non_null": 3000,
      "unique_values": 50,
      "sample_values": [
        3,
        21,
        48,
        16
      ],
      "min": 0,
      "max": 49
    },
    {
      "name": "Venture Capital Funding (Billion USD)",
      "dtype": "float64",
      "semantic_type": "numeric",
      "non_null": 3000,
      "unique_values": 2596,
      "sample_values": [
        76.64,
        5.67,
        39.43,
        12.83
      ],
      "min": 0.1,
      "max": 99.99
    },
    {
      "name": "Consumer Spending (Billion USD)",
      "dtype": "int64",
      "semantic_type": "numeric",
      "non_null": 3000,
      "unique_values": 2734,
      "sample_values": [
        4589,
        10101,
        13665,
        5192
      ],
      "min": 101,
      "max": 14990
    }
  ],
  "sample_rows": [
    {
      "Date": "2000-01-01T00:00:00",
      "Stock Index": "Dow Jones",
      "Open Price": 2128.75,
      "Close Price": 2138.48,
      "Daily High": 2143.7,
      "Daily Low": 2100.55,
      "Trading Volume": 2670411,
      "GDP Growth (%)": -0.37,
      "Inflation Rate (%)": 6.06,
      "Unemployment Rate (%)": 6.1,
      "Interest Rate (%)": 6.06,
      "Consumer Confidence Index": 114,
      "Government Debt (Billion USD)": 27271,
      "Corporate Profits (Billion USD)": 1645,
      "Forex USD/EUR": 1.04,
      "Forex USD/JPY": 119.87,
      "Crude Oil Price (USD per Barrel)": 47.2,
      "Gold Price (USD per Ounce)": 1052.34,
      "Real Estate Index": 390.23,
      "Retail Sales (Billion USD)": 2229,
      "Bankruptcy Rate (%)": 2.12,
      "Mergers & Acquisitions Deals": 3,
      "Venture Capital Funding (Billion USD)": 76.64,
      "Consumer Spending (Billion USD)": 4589
    },
    {
      "Date": "2000-01-02T00:00:00",
      "Stock Index": "S&P 500",
      "Open Price": 2046.82,
      "Close Price": 2036.18,
      "Daily High": 2082.83,
      "Daily Low": 2009.53,
      "Trading Volume": 690220415,
      "GDP Growth (%)": 3.19,
      "Inflation Rate (%)": 4.95,
      "Unemployment Rate (%)": 6.62,
      "Interest Rate (%)": 2.19,
      "Consumer Confidence Index": 101,
      "Government Debt (Billion USD)": 16160,
      "Corporate Profits (Billion USD)": 1008,
      "Forex USD/EUR": 1.0,
      "Forex USD/JPY": 98.22,
      "Crude Oil Price (USD per Barrel)": 52.84,
      "Gold Price (USD per Ounce)": 1957.73,
      "Real Estate Index": 346.23,
      "Retail Sales (Billion USD)": 4156,
      "Bankruptcy Rate (%)": 1.4,
      "Mergers & Acquisitions Deals": 21,
      "Venture Capital Funding (Billion USD)": 5.67,
      "Consumer Spending (Billion USD)": 10101
    },
    {
      "Date": "2000-01-03T00:00:00",
      "Stock Index": "Dow Jones",
      "Open Price": 1987.92,
      "Close Price": 1985.26,
      "Daily High": 2022.28,
      "Daily Low": 1978.37,
      "Trading Volume": 315284661,
      "GDP Growth (%)": 5.54,
      "Inflation Rate (%)": 9.13,
      "Unemployment Rate (%)": 2.6,
      "Interest Rate (%)": 0.82,
      "Consumer Confidence Index": 92,
      "Government Debt (Billion USD)": 29962,
      "Corporate Profits (Billion USD)": 4562,
      "Forex USD/EUR": 0.83,
      "Forex USD/JPY": 80.13,
      "Crude Oil Price (USD per Barrel)": 78.8,
      "Gold Price (USD per Ounce)": 2339.49,
      "Real Estate Index": 439.46,
      "Retail Sales (Billion USD)": 340,
      "Bankruptcy Rate (%)": 0.79,
      "Mergers & Acquisitions Deals": 48,
      "Venture Capital Funding (Billion USD)": 39.43,
      "Consumer Spending (Billion USD)": 13665
    },
    {
      "Date": "2000-01-04T00:00:00",
      "Stock Index": "Dow Jones",
      "Open Price": 4625.02,
      "Close Price": 4660.47,
      "Daily High": 4665.26,
      "Daily Low": 4595.46,
      "Trading Volume": 13098297,
      "GDP Growth (%)": 10.0,
      "Inflation Rate (%)": 3.77,
      "Unemployment Rate (%)": 2.2,
      "Interest Rate (%)": 3.71,
      "Consumer Confidence Index": 112,
      "Government Debt (Billion USD)": 12745,
      "Corporate Profits (Billion USD)": 4183,
      "Forex USD/EUR": 0.95,
      "Forex USD/JPY": 149.15,
      "Crude Oil Price (USD per Barrel)": 28.18,
      "Gold Price (USD per Ounce)": 1308.54,
      "Real Estate Index": 213.07,
      "Retail Sales (Billion USD)": 8456,
      "Bankruptcy Rate (%)": 4.22,
      "Mergers & Acquisitions Deals": 16,
      "Venture Capital Funding (Billion USD)": 12.83,
      "Consumer Spending (Billion USD)": 5192
    },
    {
      "Date": "2000-01-05T00:00:00",
      "Stock Index": "S&P 500",
      "Open Price": 1998.18,
      "Close Price": 1982.18,
      "Daily High": 2044.31,
      "Daily Low": 1966.44,
      "Trading Volume": 385306746,
      "GDP Growth (%)": 1.53,
      "Inflation Rate (%)": 2.2,
      "Unemployment Rate (%)": 8.2,
      "Interest Rate (%)": 4.56,
      "Consumer Confidence Index": 99,
      "Government Debt (Billion USD)": 22293,
      "Corporate Profits (Billion USD)": 3440,
      "Forex USD/EUR": 1.43,
      "Forex USD/JPY": 113.71,
      "Crude Oil Price (USD per Barrel)": 92.2,
      "Gold Price (USD per Ounce)": 2210.08,
      "Real Estate Index": 405.49,
      "Retail Sales (Billion USD)": 1596,
      "Bankruptcy Rate (%)": 2.21,
      "Mergers & Acquisitions Deals": 34,
      "Venture Capital Funding (Billion USD)": 86.37,
      "Consumer Spending (Billion USD)": 10688
    }
  ]
}