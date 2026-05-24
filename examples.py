import json
from summarizer.summaries.summary_finance_economics_dataset import dataset_summary

SUMMARY = dataset_summary

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

EXAMPLES = [
    {
        "request": "Show the evolution of trading volume over time.",
        "response": {
            "type": "line",
            "data": {"dimension": "Date", "metric": "Trading Volume", "aggregation": "sum"},
            "title": "Trading volume over time",
            "description": "Displays how the total stock trading volume changed over time.",
            "explanation": "Line charts are ideal for identifying trends across dates.",
        },
    },
    {
        "request": "How did the average closing price change over time?",
        "response": {
            "type": "line",
            "data": {"dimension": "Date", "metric": "Close Price", "aggregation": "mean"},
            "title": "Average closing price over time",
            "description": "Shows the average stock closing price evolution across the dataset timeline.",
            "explanation": "A line chart highlights temporal movement in market prices.",
        },
    },
    {
        "request": "Compare the average opening price over time by stock index.",
        "response": {
            "type": "line",
            "data": {
                "dimension": "Date",
                "metric": "Open Price",
                "aggregation": "mean",
                "color": "Stock Index"
            },
            "title": "Average opening price by stock index",
            "description": "Compares opening price trends between stock indexes over time.",
            "explanation": "Using color by Stock Index separates the trends for each market index.",
        },
    },
    {
        "request": "Show the trend of GDP growth over time.",
        "response": {
            "type": "line",
            "data": {"dimension": "Date", "metric": "GDP Growth (%)", "aggregation": "mean"},
            "title": "GDP growth trend over time",
            "description": "Displays how GDP growth rates evolved across the timeline.",
            "explanation": "A temporal line chart is appropriate for macroeconomic indicators.",
        },
    },
    {
        "request": "Compare inflation rates over time by stock index.",
        "response": {
            "type": "line",
            "data": {
                "dimension": "Date",
                "metric": "Inflation Rate (%)",
                "aggregation": "mean",
                "color": "Stock Index"
            },
            "title": "Inflation rate by stock index",
            "description": "Shows inflation trends separated by stock index categories.",
            "explanation": "Colored lines help compare inflation behavior across groups.",
        },
    },

    {
        "request": "Which stock index has the highest average trading volume?",
        "response": {
            "type": "bar",
            "data": {
                "dimension": "Stock Index",
                "metric": "Trading Volume",
                "aggregation": "mean"
            },
            "title": "Average trading volume by stock index",
            "description": "Compares average trading activity across stock indexes.",
            "explanation": "Bar charts are effective for categorical comparisons.",
        },
    },
    {
        "request": "Compare the average close price by stock index.",
        "response": {
            "type": "bar",
            "data": {
                "dimension": "Stock Index",
                "metric": "Close Price",
                "aggregation": "mean"
            },
            "title": "Average close price by stock index",
            "description": "Shows the average closing price for each stock index.",
            "explanation": "Bars clearly compare average values between categories.",
        },
    },
    {
        "request": "Show government debt by stock index.",
        "response": {
            "type": "bar",
            "data": {
                "dimension": "Stock Index",
                "metric": "Government Debt (Billion USD)",
                "aggregation": "mean"
            },
            "title": "Government debt by stock index",
            "description": "Compares average government debt levels associated with each stock index.",
            "explanation": "Bar charts allow easy comparison of macroeconomic metrics across groups.",
        },
    },
    {
        "request": "Compare corporate profits by stock index.",
        "response": {
            "type": "bar",
            "data": {
                "dimension": "Stock Index",
                "metric": "Corporate Profits (Billion USD)",
                "aggregation": "mean"
            },
            "title": "Corporate profits by stock index",
            "description": "Displays average corporate profits grouped by stock index.",
            "explanation": "Bars emphasize differences between financial market categories.",
        },
    },
    {
        "request": "Compare consumer spending by stock index.",
        "response": {
            "type": "bar",
            "data": {
                "dimension": "Stock Index",
                "metric": "Consumer Spending (Billion USD)",
                "aggregation": "mean"
            },
            "title": "Consumer spending by stock index",
            "description": "Shows average consumer spending values across stock indexes.",
            "explanation": "Categorical comparisons are best represented using bars.",
        },
    },

    {
        "request": "What is the market share of each stock index in total trading volume?",
        "response": {
            "type": "pie",
            "data": {
                "dimension": "Stock Index",
                "metric": "Trading Volume",
                "aggregation": "sum"
            },
            "title": "Trading volume share by stock index",
            "description": "Displays the proportion of total trading volume for each stock index.",
            "explanation": "Pie charts are useful for visualizing proportional contributions.",
        },
    },
    {
        "request": "Show the distribution of mergers and acquisitions deals by stock index.",
        "response": {
            "type": "pie",
            "data": {
                "dimension": "Stock Index",
                "metric": "Mergers & Acquisitions Deals",
                "aggregation": "sum"
            },
            "title": "M&A deals distribution by stock index",
            "description": "Shows how merger and acquisition deals are distributed across stock indexes.",
            "explanation": "Pie charts highlight the composition of total deals.",
        },
    },
    {
        "request": "How is venture capital funding distributed among stock indexes?",
        "response": {
            "type": "pie",
            "data": {
                "dimension": "Stock Index",
                "metric": "Venture Capital Funding (Billion USD)",
                "aggregation": "sum"
            },
            "title": "Venture capital funding distribution",
            "description": "Displays the share of venture capital funding across stock indexes.",
            "explanation": "Pie charts reveal proportional allocation among categories.",
        },
    },
    {
        "request": "Show the proportion of consumer spending by stock index.",
        "response": {
            "type": "pie",
            "data": {
                "dimension": "Stock Index",
                "metric": "Consumer Spending (Billion USD)",
                "aggregation": "sum"
            },
            "title": "Consumer spending share by stock index",
            "description": "Displays how consumer spending is distributed among stock indexes.",
            "explanation": "Pie charts effectively represent percentage contributions.",
        },
    },

    {
        "request": "Show the relationship between inflation rate and unemployment rate.",
        "response": {
            "type": "scatter",
            "data": {
                "x": "Inflation Rate (%)",
                "y": "Unemployment Rate (%)",
                "color": "Stock Index"
            },
            "title": "Inflation vs unemployment rate",
            "description": "Explores the relationship between inflation and unemployment rates.",
            "explanation": "Scatter plots are ideal for analyzing relationships between numeric variables.",
        },
    },
    {
        "request": "Compare crude oil price and gold price.",
        "response": {
            "type": "scatter",
            "data": {
                "x": "Crude Oil Price (USD per Barrel)",
                "y": "Gold Price (USD per Ounce)",
                "color": "Stock Index"
            },
            "title": "Crude oil price vs gold price",
            "description": "Shows the relationship between oil and gold market prices.",
            "explanation": "Scatter plots help identify correlations between commodities.",
        },
    },
    {
        "request": "Analyze the relationship between GDP growth and consumer confidence.",
        "response": {
            "type": "scatter",
            "data": {
                "x": "GDP Growth (%)",
                "y": "Consumer Confidence Index",
                "color": "Stock Index"
            },
            "title": "GDP growth vs consumer confidence",
            "description": "Explores how GDP growth relates to consumer confidence levels.",
            "explanation": "Scatter plots reveal patterns and trends between economic indicators.",
        },
    },

    {
        "request": "Show the distribution of daily closing prices.",
        "response": {
            "type": "histogram",
            "data": {
                "metric": "Close Price"
            },
            "title": "Distribution of closing prices",
            "description": "Displays how closing prices are distributed across observations.",
            "explanation": "Histograms are suitable for understanding numeric distributions.",
        },
    },
    {
        "request": "Show the distribution of interest rates.",
        "response": {
            "type": "histogram",
            "data": {
                "metric": "Interest Rate (%)"
            },
            "title": "Distribution of interest rates",
            "description": "Displays the frequency distribution of interest rate values.",
            "explanation": "Histograms reveal concentration and spread of values.",
        },
    },
    {
        "request": "Compare closing price distributions by stock index.",
        "response": {
            "type": "box",
            "data": {
                "dimension": "Stock Index",
                "metric": "Close Price"
            },
            "title": "Closing price distribution by stock index",
            "description": "Compares the spread and outliers of closing prices across indexes.",
            "explanation": "Box plots are ideal for comparing distributions between groups.",
        },
    },
    {
        "request": "Show the evolution of gold prices over time.",
        "response": {
            "type": "line",
            "data": {"dimension": "Date", "metric": "Gold Price (USD per Ounce)", "aggregation": "mean"},
            "title": "Gold prices over time",
            "description": "Displays how gold prices changed throughout the timeline.",
            "explanation": "Line charts are appropriate for tracking commodity price trends over time.",
        },
    },
    {
        "request": "How did crude oil prices change over time?",
        "response": {
            "type": "line",
            "data": {"dimension": "Date", "metric": "Crude Oil Price (USD per Barrel)", "aggregation": "mean"},
            "title": "Crude oil prices over time",
            "description": "Shows the evolution of oil prices across the dataset timeline.",
            "explanation": "Temporal data is best visualized using line charts.",
        },
    },
    {
        "request": "Compare unemployment rates over time by stock index.",
        "response": {
            "type": "line",
            "data": {
                "dimension": "Date",
                "metric": "Unemployment Rate (%)",
                "aggregation": "mean",
                "color": "Stock Index"
            },
            "title": "Unemployment rate by stock index",
            "description": "Displays unemployment rate trends separated by stock index.",
            "explanation": "Multiple lines allow comparison between stock index categories over time.",
        },
    },
    {
        "request": "Show the trend of consumer confidence over time.",
        "response": {
            "type": "line",
            "data": {
                "dimension": "Date",
                "metric": "Consumer Confidence Index",
                "aggregation": "mean"
            },
            "title": "Consumer confidence over time",
            "description": "Tracks changes in consumer confidence levels throughout the timeline.",
            "explanation": "Line charts clearly show fluctuations in economic indicators over time.",
        },
    },
    {
        "request": "Compare venture capital funding over time by stock index.",
        "response": {
            "type": "line",
            "data": {
                "dimension": "Date",
                "metric": "Venture Capital Funding (Billion USD)",
                "aggregation": "mean",
                "color": "Stock Index"
            },
            "title": "Venture capital funding by stock index",
            "description": "Compares venture capital investment trends across stock indexes.",
            "explanation": "Color grouping separates funding patterns between indexes.",
        },
    },

    {
        "request": "Which stock index has the highest average GDP growth?",
        "response": {
            "type": "bar",
            "data": {
                "dimension": "Stock Index",
                "metric": "GDP Growth (%)",
                "aggregation": "mean"
            },
            "title": "Average GDP growth by stock index",
            "description": "Compares average GDP growth rates across stock indexes.",
            "explanation": "Bar charts make it easy to compare average macroeconomic performance.",
        },
    },
    {
        "request": "Compare inflation rates by stock index.",
        "response": {
            "type": "bar",
            "data": {
                "dimension": "Stock Index",
                "metric": "Inflation Rate (%)",
                "aggregation": "mean"
            },
            "title": "Average inflation rate by stock index",
            "description": "Displays average inflation levels grouped by stock index.",
            "explanation": "Bars effectively compare economic indicators between categories.",
        },
    },
    {
        "request": "Compare average forex USD/EUR values by stock index.",
        "response": {
            "type": "bar",
            "data": {
                "dimension": "Stock Index",
                "metric": "Forex USD/EUR",
                "aggregation": "mean"
            },
            "title": "Average USD/EUR exchange rate by stock index",
            "description": "Shows average USD/EUR exchange rate values across indexes.",
            "explanation": "Bar charts are suitable for comparing average exchange rates.",
        },
    },
    {
        "request": "Show average real estate index values by stock index.",
        "response": {
            "type": "bar",
            "data": {
                "dimension": "Stock Index",
                "metric": "Real Estate Index",
                "aggregation": "mean"
            },
            "title": "Real estate index by stock index",
            "description": "Compares real estate index averages across stock indexes.",
            "explanation": "Categorical comparisons are clearly represented with bars.",
        },
    },
    {
        "request": "Compare bankruptcy rates by stock index.",
        "response": {
            "type": "bar",
            "data": {
                "dimension": "Stock Index",
                "metric": "Bankruptcy Rate (%)",
                "aggregation": "mean"
            },
            "title": "Bankruptcy rate by stock index",
            "description": "Shows average bankruptcy rates for each stock index.",
            "explanation": "Bar charts highlight differences in bankruptcy levels across categories.",
        },
    },

    {
        "request": "Show the share of total corporate profits by stock index.",
        "response": {
            "type": "pie",
            "data": {
                "dimension": "Stock Index",
                "metric": "Corporate Profits (Billion USD)",
                "aggregation": "sum"
            },
            "title": "Corporate profits share by stock index",
            "description": "Displays the contribution of each stock index to total corporate profits.",
            "explanation": "Pie charts effectively show proportional distributions.",
        },
    },
    {
        "request": "What proportion of total retail sales belongs to each stock index?",
        "response": {
            "type": "pie",
            "data": {
                "dimension": "Stock Index",
                "metric": "Retail Sales (Billion USD)",
                "aggregation": "sum"
            },
            "title": "Retail sales distribution by stock index",
            "description": "Shows how retail sales are distributed among stock indexes.",
            "explanation": "Pie charts reveal category contributions to the total.",
        },
    },
    {
        "request": "Show the distribution of government debt across stock indexes.",
        "response": {
            "type": "pie",
            "data": {
                "dimension": "Stock Index",
                "metric": "Government Debt (Billion USD)",
                "aggregation": "sum"
            },
            "title": "Government debt distribution by stock index",
            "description": "Displays the share of government debt associated with each stock index.",
            "explanation": "Pie charts are useful for understanding proportional composition.",
        },
    },

    {
        "request": "Analyze the relationship between interest rates and inflation rates.",
        "response": {
            "type": "scatter",
            "data": {
                "x": "Interest Rate (%)",
                "y": "Inflation Rate (%)",
                "color": "Stock Index"
            },
            "title": "Interest rate vs inflation rate",
            "description": "Explores the relationship between interest and inflation rates.",
            "explanation": "Scatter plots help identify economic correlations between numeric variables.",
        },
    },
    {
        "request": "Show the relationship between trading volume and closing price.",
        "response": {
            "type": "scatter",
            "data": {
                "x": "Trading Volume",
                "y": "Close Price",
                "color": "Stock Index"
            },
            "title": "Trading volume vs closing price",
            "description": "Explores whether trading activity is associated with stock closing prices.",
            "explanation": "Scatter plots are useful for detecting relationships and clusters.",
        },
    },
    {
        "request": "Analyze consumer spending versus retail sales.",
        "response": {
            "type": "scatter",
            "data": {
                "x": "Consumer Spending (Billion USD)",
                "y": "Retail Sales (Billion USD)",
                "color": "Stock Index"
            },
            "title": "Consumer spending vs retail sales",
            "description": "Examines the relationship between spending and retail activity.",
            "explanation": "Scatter plots reveal patterns between economic indicators.",
        },
    },
    {
        "request": "Compare government debt and GDP growth.",
        "response": {
            "type": "scatter",
            "data": {
                "x": "Government Debt (Billion USD)",
                "y": "GDP Growth (%)",
                "color": "Stock Index"
            },
            "title": "Government debt vs GDP growth",
            "description": "Explores how government debt levels relate to GDP growth.",
            "explanation": "Scatter plots help identify possible economic relationships.",
        },
    },

    {
        "request": "Show the distribution of trading volumes.",
        "response": {
            "type": "histogram",
            "data": {
                "metric": "Trading Volume"
            },
            "title": "Distribution of trading volumes",
            "description": "Displays the frequency distribution of trading volume values.",
            "explanation": "Histograms are effective for understanding data spread and concentration.",
        },
    },
    {
        "request": "Show the distribution of GDP growth rates.",
        "response": {
            "type": "histogram",
            "data": {
                "metric": "GDP Growth (%)"
            },
            "title": "Distribution of GDP growth rates",
            "description": "Displays how GDP growth values are distributed in the dataset.",
            "explanation": "Histograms help visualize variability and skewness in numeric data.",
        },
    },

    {
        "request": "Compare gold price distributions by stock index.",
        "response": {
            "type": "box",
            "data": {
                "dimension": "Stock Index",
                "metric": "Gold Price (USD per Ounce)"
            },
            "title": "Gold price distribution by stock index",
            "description": "Compares gold price spread and outliers across stock indexes.",
            "explanation": "Box plots summarize distribution, median, and variability between groups.",
        },
    }
]