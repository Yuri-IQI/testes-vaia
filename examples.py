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

def build_few_shots_block() -> str:
    lines = []
    for i in range(70, 80):
        lines.append(f"User request: {EXAMPLES[i]['request']}")
        lines.append("JSON response:")
        lines.append(json.dumps(EXAMPLES[i]["response"], indent=2, ensure_ascii=False))
        lines.append("")
    return "\n".join(lines).strip()

EXAMPLES = [
    {
        "request": "Show the distribution of crude oil prices.",
        "response": json.dumps({
            "type": "histogram",
            "data": {
                "dimension": None,
                "metric": "Crude Oil Price (USD per Barrel)",
                "metric_secondary": None,
                "aggregation": None,
                "color": None,
                "filters": {},
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": 40,
                "top_n": None,
            },
            "title": "Distribution of crude oil prices",
            "description": "Shows how crude oil prices are spread across the dataset.",
            "explanation": (
                "A histogram reveals the frequency distribution "
                "of a single numeric column."
            ),
        })
    },
    {
        "request": "Show the spread of close prices by stock index.",
        "response": {
            "type": "box",
            "data": {
                "dimension": "Stock Index",
                "metric": "Close Price",
                "metric_secondary": None,
                "aggregation": None,
                "color": None,
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Close price spread by stock index",
            "description": "Displays the distribution and outliers of closing prices for each stock index.",
            "explanation": "Box plots show variance and outliers across categorical groups.",
        },
    },
    {
        "request": "Is there a correlation between crude oil price and close price?",
        "response": {
            "type": "scatter",
            "data": {
                "dimension": "Crude Oil Price (USD per Barrel)",
                "metric": "Close Price",
                "metric_secondary": None,
                "aggregation": None,
                "color": None,
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": True,
                "nbins": None,
                "top_n": None,
            },
            "title": "Crude oil price vs close price",
            "description": "Plots each observation as a point to reveal any linear relationship between oil and stock prices.",
            "explanation": "Scatter with a trend line is the standard tool for visualizing correlation between two numeric columns.",
        },
    },
    {
        "request": "Show trading volume over time by stock index.",
        "response": {
            "type": "line",
            "data": {
                "dimension": "Date",
                "metric": "Trading Volume",
                "metric_secondary": None,
                "aggregation": "sum",
                "color": "Stock Index",
            },
            "render_options": {
                "log_scale_y": True,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Trading volume over time by stock index",
            "description": "Compares total trading volume trends across stock indexes on a log scale.",
            "explanation": "Trading Volume spans several orders of magnitude, so a log scale prevents large spikes from compressing the rest of the chart.",
        },
    },
    {
        "request": "Which are the top 3 stock indexes by average corporate profits?",
        "response": {
            "type": "bar",
            "data": {
                "dimension": "Stock Index",
                "metric": "Corporate Profits (Billion USD)",
                "metric_secondary": None,
                "aggregation": "mean",
                "color": None,
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": 3,
            },
            "title": "Top 3 stock indexes by average corporate profits",
            "description": "Ranks the three stock indexes with the highest average corporate profits.",
            "explanation": "top_n limits the bar chart to the requested number of leading categories.",
        },
    },
    {
        "request": "Show the variance of unemployment rate across stock indexes.",
        "response": {
            "type": "box",
            "data": {
                "dimension": "Stock Index",
                "metric": "Unemployment Rate (%)",
                "metric_secondary": None,
                "aggregation": None,
                "color": None,
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Unemployment rate variance by stock index",
            "description": "Shows the spread and outliers of unemployment rates grouped by stock index.",
            "explanation": "Box plots expose variance and extremes that a mean-based bar chart would hide.",
        },
    },
    {
        "request": "Is there a relationship between gold price and real estate index, colored by stock index?",
        "response": {
            "type": "scatter",
            "data": {
                "dimension": "Gold Price (USD per Ounce)",
                "metric": "Real Estate Index",
                "metric_secondary": None,
                "aggregation": None,
                "color": "Stock Index",
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": True,
                "nbins": None,
                "top_n": None,
            },
            "title": "Gold price vs real estate index by stock index",
            "description": "Plots gold price against real estate index with each stock index in a distinct color.",
            "explanation": "Color separates the groups while the trend line surfaces the overall relationship direction.",
        },
    },
    {
        "request": "Show the distribution of interest rates with high granularity.",
        "response": {
            "type": "histogram",
            "data": {
                "dimension": None,
                "metric": "Interest Rate (%)",
                "metric_secondary": None,
                "aggregation": None,
                "color": None,
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": 60,
                "top_n": None,
            },
            "title": "Distribution of interest rates",
            "description": "Shows the frequency of interest rate values across the full dataset at fine resolution.",
            "explanation": "A higher bin count reveals subtle clustering in the distribution when the dataset is large.",
        },
    },
    {
        "request": "Compare average inflation rate by stock index and show outliers.",
        "response": {
            "type": "box",
            "data": {
                "dimension": "Stock Index",
                "metric": "Inflation Rate (%)",
                "metric_secondary": None,
                "aggregation": None,
                "color": "Stock Index",
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Inflation rate distribution by stock index",
            "description": "Displays median, spread, and outliers of inflation rates for each stock index.",
            "explanation": "Box plots are preferred over bar when the user explicitly asks about outliers or variance.",
        },
    },
    {
        "request": "Show the relationship between GDP growth and consumer spending.",
        "response": {
            "type": "scatter",
            "data": {
                "dimension": "GDP Growth (%)",
                "metric": "Consumer Spending (Billion USD)",
                "metric_secondary": None,
                "aggregation": None,
                "color": None,
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": True,
                "nbins": None,
                "top_n": None,
            },
            "title": "GDP growth vs consumer spending",
            "description": "Plots GDP growth against consumer spending to surface any macroeconomic relationship.",
            "explanation": "Scatter with trend line is appropriate when the user asks about the relationship between two numeric indicators.",
        },
    },
    {
        "request": "Show how the interest rate evolved over time for each stock index.",
        "response": {
            "type": "line",
            "data": {
                "dimension": "Date",
                "metric": "Interest Rate (%)",
                "metric_secondary": None,
                "aggregation": "mean",
                "color": "Stock Index",
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Interest rate evolution by stock index",
            "description": "Tracks mean interest rate over time separated by stock index.",
            "explanation": "A colored line chart separates each index's monetary policy trajectory across the timeline.",
        },
    },
    {
        "request": "What is the distribution of bankruptcy rates?",
        "response": {
            "type": "histogram",
            "data": {
                "dimension": None,
                "metric": "Bankruptcy Rate (%)",
                "metric_secondary": None,
                "aggregation": None,
                "color": None,
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": 40,
                "top_n": None,
            },
            "title": "Distribution of bankruptcy rates",
            "description": "Shows how bankruptcy rate values are distributed across all observations.",
            "explanation": "A histogram is the correct choice for understanding the shape of a single numeric column's distribution.",
        },
    },
    {
        "request": "Is there a correlation between inflation rate and unemployment rate by stock index?",
        "response": {
            "type": "scatter",
            "data": {
                "dimension": "Inflation Rate (%)",
                "metric": "Unemployment Rate (%)",
                "metric_secondary": None,
                "aggregation": None,
                "color": "Stock Index",
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": True,
                "nbins": None,
                "top_n": None,
            },
            "title": "Inflation rate vs unemployment rate by stock index",
            "description": "Plots inflation against unemployment for each observation, colored by stock index.",
            "explanation": "Scatter with trend line surfaces the Phillips curve relationship; color separates market groups.",
        },
    },
    {
        "request": "Show the top 5 dates by highest total trading volume.",
        "response": {
            "type": "bar",
            "data": {
                "dimension": "Date",
                "metric": "Trading Volume",
                "metric_secondary": None,
                "aggregation": "sum",
                "color": None,
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": 5,
            },
            "title": "Top 5 dates by total trading volume",
            "description": "Ranks the five dates with the highest combined trading activity.",
            "explanation": "top_n limits the bar chart to the explicitly requested number of leading entries.",
        },
    },
    {
        "request": "How spread out are venture capital funding values across stock indexes?",
        "response": {
            "type": "box",
            "data": {
                "dimension": "Stock Index",
                "metric": "Venture Capital Funding (Billion USD)",
                "metric_secondary": None,
                "aggregation": None,
                "color": None,
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Venture capital funding spread by stock index",
            "description": "Displays the distribution and outliers of venture capital funding grouped by stock index.",
            "explanation": "Box plots reveal spread and extreme values that aggregated bar charts would obscure.",
        },
    },
    {
        "request": "Show the share of total retail sales by stock index.",
        "response": {
            "type": "pie",
            "data": {
                "dimension": "Stock Index",
                "metric": "Retail Sales (Billion USD)",
                "metric_secondary": None,
                "aggregation": "sum",
                "color": None,
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Share of total retail sales by stock index",
            "description": "Shows each stock index's proportional contribution to total retail sales.",
            "explanation": "Pie charts communicate part-of-whole relationships for low-cardinality categorical dimensions.",
        },
    },
    {
        "request": "Is there a relationship between consumer confidence and consumer spending?",
        "response": {
            "type": "scatter",
            "data": {
                "dimension": "Consumer Confidence Index",
                "metric": "Consumer Spending (Billion USD)",
                "metric_secondary": None,
                "aggregation": None,
                "color": None,
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": True,
                "nbins": None,
                "top_n": None,
            },
            "title": "Consumer confidence vs consumer spending",
            "description": "Plots consumer confidence against spending levels across all observations.",
            "explanation": "Scatter with trend line is appropriate when the request asks about the relationship between two numeric indicators.",
        },
    },
    {
        "request": "Show the distribution of daily high prices with fine granularity.",
        "response": {
            "type": "histogram",
            "data": {
                "dimension": None,
                "metric": "Daily High",
                "metric_secondary": None,
                "aggregation": None,
                "color": None,
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": 60,
                "top_n": None,
            },
            "title": "Distribution of daily high prices",
            "description": "Shows the frequency of daily high price values at fine resolution.",
            "explanation": "A higher bin count is appropriate when the user explicitly requests granularity on a large dataset.",
        },
    },
    {
        "request": "Compare average consumer spending by stock index.",
        "response": {
            "type": "bar",
            "data": {
                "dimension": "Stock Index",
                "metric": "Consumer Spending (Billion USD)",
                "metric_secondary": None,
                "aggregation": "mean",
                "color": None,
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Average consumer spending by stock index",
            "description": "Compares mean consumer spending levels across stock indexes.",
            "explanation": "A bar chart with mean aggregation is the standard choice for comparing a numeric metric across a categorical dimension.",
        },
    },
    {
        "request": "Show the volatility of gold prices across stock indexes.",
        "response": {
            "type": "box",
            "data": {
                "dimension": "Stock Index",
                "metric": "Gold Price (USD per Ounce)",
                "metric_secondary": None,
                "aggregation": None,
                "color": "Stock Index",
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Gold price volatility by stock index",
            "description": "Displays the spread, median, and outliers of gold prices for each stock index.",
            "explanation": "Volatility implies variance and outliers, which box plots convey directly; color reinforces the categorical grouping.",
        },
    },
    {
        "request": "Show how crude oil prices evolved over time.",
        "response": {
            "type": "line",
            "data": {
                "dimension": "Date",
                "metric": "Crude Oil Price (USD per Barrel)",
                "metric_secondary": None,
                "aggregation": "mean",
                "color": None,
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Crude oil price evolution over time",
            "description": "Tracks the mean crude oil price across the full dataset timeline.",
            "explanation": "A line chart is the natural choice for a single numeric indicator evolving over a datetime dimension.",
        },
    },
    {
        "request": "Show the distribution of GDP growth rates.",
        "response": {
            "type": "histogram",
            "data": {
                "dimension": None,
                "metric": "GDP Growth (%)",
                "metric_secondary": None,
                "aggregation": None,
                "color": None,
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": 40,
                "top_n": None,
            },
            "title": "Distribution of GDP growth rates",
            "description": "Shows how GDP growth rate values are spread across all observations.",
            "explanation": "A histogram is appropriate for understanding the shape and spread of a single numeric column.",
        },
    },
    {
        "request": "Is there a relationship between interest rate and inflation rate?",
        "response": {
            "type": "scatter",
            "data": {
                "dimension": "Interest Rate (%)",
                "metric": "Inflation Rate (%)",
                "metric_secondary": None,
                "aggregation": None,
                "color": None,
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": True,
                "nbins": None,
                "top_n": None,
            },
            "title": "Interest rate vs inflation rate",
            "description": "Plots interest rate against inflation rate across all observations.",
            "explanation": "Scatter with trend line is the correct choice when the user asks about the relationship between two numeric columns.",
        },
    },
    {
        "request": "Show the spread of GDP growth by stock index.",
        "response": {
            "type": "box",
            "data": {
                "dimension": "Stock Index",
                "metric": "GDP Growth (%)",
                "metric_secondary": None,
                "aggregation": None,
                "color": None,
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "GDP growth spread by stock index",
            "description": "Displays the distribution and outliers of GDP growth rates for each stock index.",
            "explanation": "Box plots expose variance and extremes that a mean bar chart would hide.",
        },
    },
    {
        "request": "Compare total venture capital funding by stock index.",
        "response": {
            "type": "bar",
            "data": {
                "dimension": "Stock Index",
                "metric": "Venture Capital Funding (Billion USD)",
                "metric_secondary": None,
                "aggregation": "sum",
                "color": None,
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Total venture capital funding by stock index",
            "description": "Shows the total venture capital funding associated with each stock index.",
            "explanation": "A bar chart with sum aggregation compares total accumulated values across a low-cardinality categorical dimension.",
        },
    },
    {
        "request": "Show the share of average government debt by stock index.",
        "response": {
            "type": "pie",
            "data": {
                "dimension": "Stock Index",
                "metric": "Government Debt (Billion USD)",
                "metric_secondary": None,
                "aggregation": "mean",
                "color": None,
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Share of average government debt by stock index",
            "description": "Shows each stock index's proportional share of average government debt.",
            "explanation": "Pie charts are appropriate for part-of-whole comparisons across a low-cardinality categorical dimension.",
        },
    },
    {
        "request": "Show trading volume over time on a log scale.",
        "response": {
            "type": "line",
            "data": {
                "dimension": "Date",
                "metric": "Trading Volume",
                "metric_secondary": None,
                "aggregation": "sum",
                "color": None,
            },
            "render_options": {
                "log_scale_y": True,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Trading volume over time (log scale)",
            "description": "Tracks total trading volume across the timeline with a logarithmic y-axis.",
            "explanation": "Trading Volume spans several orders of magnitude; log scale prevents extreme spikes from compressing lower values.",
        },
    },
    {
        "request": "Is there a correlation between real estate index and corporate profits, grouped by stock index?",
        "response": {
            "type": "scatter",
            "data": {
                "dimension": "Real Estate Index",
                "metric": "Corporate Profits (Billion USD)",
                "metric_secondary": None,
                "aggregation": None,
                "color": "Stock Index",
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": True,
                "nbins": None,
                "top_n": None,
            },
            "title": "Real estate index vs corporate profits by stock index",
            "description": "Plots real estate index against corporate profits, colored by stock index.",
            "explanation": "Scatter with trend line and color reveals whether the correlation differs across market groups.",
        },
    },
    {
        "request": "Show the distribution of forex USD/JPY values.",
        "response": {
            "type": "histogram",
            "data": {
                "dimension": None,
                "metric": "Forex USD/JPY",
                "metric_secondary": None,
                "aggregation": None,
                "color": None,
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": 40,
                "top_n": None,
            },
            "title": "Distribution of Forex USD/JPY",
            "description": "Shows the frequency distribution of USD/JPY exchange rate values.",
            "explanation": "A histogram is the right tool for revealing clustering and spread in a single continuous variable.",
        },
    },
    {
        "request": "Show how gold prices evolved over time by stock index.",
        "response": {
            "type": "line",
            "data": {
                "dimension": "Date",
                "metric": "Gold Price (USD per Ounce)",
                "metric_secondary": None,
                "aggregation": "mean",
                "color": "Stock Index",
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Gold price evolution by stock index",
            "description": "Tracks mean gold price over time for each stock index.",
            "explanation": "Colored lines separate each index's gold price trajectory across the timeline.",
        },
    },
    {
        "request": "Which stock index has the highest average unemployment rate?",
        "response": {
            "type": "bar",
            "data": {
                "dimension": "Stock Index",
                "metric": "Unemployment Rate (%)",
                "metric_secondary": None,
                "aggregation": "mean",
                "color": None,
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Average unemployment rate by stock index",
            "description": "Compares mean unemployment rates across stock indexes.",
            "explanation": "A bar chart with mean aggregation is the standard approach for comparing a rate metric across categories.",
        },
    },
    {
        "request": "Show the volatility of inflation rates across stock indexes.",
        "response": {
            "type": "box",
            "data": {
                "dimension": "Stock Index",
                "metric": "Inflation Rate (%)",
                "metric_secondary": None,
                "aggregation": None,
                "color": "Stock Index",
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Inflation rate volatility by stock index",
            "description": "Displays median, spread, and outliers of inflation rates for each stock index.",
            "explanation": "Volatility implies variance and extremes; box plots communicate both directly.",
        },
    },
    {
        "request": "Show the top 10 dates by highest average close price.",
        "response": {
            "type": "bar",
            "data": {
                "dimension": "Date",
                "metric": "Close Price",
                "metric_secondary": None,
                "aggregation": "mean",
                "color": None,
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": 10,
            },
            "title": "Top 10 dates by average close price",
            "description": "Ranks the ten dates with the highest mean closing price.",
            "explanation": "top_n limits the bar chart to the explicitly requested number of leading entries.",
        },
    },
    {
        "request": "Is there a relationship between forex USD/EUR and gold price?",
        "response": {
            "type": "scatter",
            "data": {
                "dimension": "Forex USD/EUR",
                "metric": "Gold Price (USD per Ounce)",
                "metric_secondary": None,
                "aggregation": None,
                "color": None,
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": True,
                "nbins": None,
                "top_n": None,
            },
            "title": "Forex USD/EUR vs gold price",
            "description": "Plots the USD/EUR exchange rate against gold price across all observations.",
            "explanation": "Scatter with trend line reveals whether currency strength correlates with gold valuation.",
        },
    },
    {
        "request": "Show the distribution of consumer confidence index values.",
        "response": {
            "type": "histogram",
            "data": {
                "dimension": None,
                "metric": "Consumer Confidence Index",
                "metric_secondary": None,
                "aggregation": None,
                "color": None,
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": 20,
                "top_n": None,
            },
            "title": "Distribution of consumer confidence index",
            "description": "Shows how consumer confidence values are distributed across the dataset.",
            "explanation": "Consumer Confidence Index has only 70 unique values, so a lower bin count avoids over-fragmenting the distribution.",
        },
    },
    {
        "request": "Compare average retail sales by stock index.",
        "response": {
            "type": "bar",
            "data": {
                "dimension": "Stock Index",
                "metric": "Retail Sales (Billion USD)",
                "metric_secondary": None,
                "aggregation": "mean",
                "color": None,
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Average retail sales by stock index",
            "description": "Compares mean retail sales levels across stock indexes.",
            "explanation": "Bar charts with mean aggregation clearly compare average economic output across categorical groups.",
        },
    },
    {
        "request": "Show how the real estate index changed over time.",
        "response": {
            "type": "line",
            "data": {
                "dimension": "Date",
                "metric": "Real Estate Index",
                "metric_secondary": None,
                "aggregation": "mean",
                "color": None,
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Real estate index over time",
            "description": "Tracks the mean real estate index value across the full dataset timeline.",
            "explanation": "A line chart is appropriate for a single indicator's temporal evolution.",
        },
    },
    {
        "request": "Show the spread of corporate profits by stock index with outliers.",
        "response": {
            "type": "box",
            "data": {
                "dimension": "Stock Index",
                "metric": "Corporate Profits (Billion USD)",
                "metric_secondary": None,
                "aggregation": None,
                "color": "Stock Index",
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Corporate profits spread by stock index",
            "description": "Displays the distribution, median, and outliers of corporate profits for each stock index.",
            "explanation": "When the user explicitly asks for outliers, box plots are preferred over any aggregated chart type.",
        },
    },
    {
        "request": "Is there a correlation between government debt and corporate profits by stock index?",
        "response": {
            "type": "scatter",
            "data": {
                "dimension": "Government Debt (Billion USD)",
                "metric": "Corporate Profits (Billion USD)",
                "metric_secondary": None,
                "aggregation": None,
                "color": "Stock Index",
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": True,
                "nbins": None,
                "top_n": None,
            },
            "title": "Government debt vs corporate profits by stock index",
            "description": "Plots government debt against corporate profits across all observations, colored by stock index.",
            "explanation": "Scatter with trend line and color reveals whether the debt-profit relationship differs across market groups.",
        },
    },
    {
        "request": "Show the distribution of mergers and acquisitions deals.",
        "response": {
            "type": "histogram",
            "data": {
                "dimension": None,
                "metric": "Mergers & Acquisitions Deals",
                "metric_secondary": None,
                "aggregation": None,
                "color": None,
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": 20,
                "top_n": None,
            },
            "title": "Distribution of mergers and acquisitions deals",
            "description": "Shows the frequency of M&A deal counts across all observations.",
            "explanation": "Mergers & Acquisitions Deals has only 50 unique values, so a lower bin count produces clean, readable buckets without over-fragmenting.",
        },
    },
    {
        "request": "How many records exist per stock index?",
        "response": {
            "type": "bar",
            "data": {
                "dimension": "Stock Index",
                "metric": "Close Price",
                "metric_secondary": None,
                "aggregation": "count",
                "color": None,
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Record count by stock index",
            "description": "Shows the number of observations available for each stock index.",
            "explanation": "Count aggregation on a bar chart is the correct choice when the user asks how many records exist per category.",
        },
    },
    {
        "request": "Show the relationship between crude oil price and gold price on a log scale.",
        "response": {
            "type": "scatter",
            "data": {
                "dimension": "Crude Oil Price (USD per Barrel)",
                "metric": "Gold Price (USD per Ounce)",
                "metric_secondary": None,
                "aggregation": None,
                "color": None,
            },
            "render_options": {
                "log_scale_y": True,
                "show_trend_line": True,
                "nbins": None,
                "top_n": None,
            },
            "title": "Crude oil price vs gold price (log scale)",
            "description": "Plots crude oil price against gold price with a logarithmic y-axis to handle value range differences.",
            "explanation": "Log scale is appropriate when the metric spans a wide numeric range; trend line surfaces the directional relationship.",
        },
    },
    {
        "request": "Show the distribution of retail sales with high granularity.",
        "response": {
            "type": "histogram",
            "data": {
                "dimension": None,
                "metric": "Retail Sales (Billion USD)",
                "metric_secondary": None,
                "aggregation": None,
                "color": None,
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": 60,
                "top_n": None,
            },
            "title": "Distribution of retail sales",
            "description": "Shows the frequency distribution of retail sales values at fine resolution.",
            "explanation": "Retail Sales has nearly 2600 unique values across 3000 rows; a higher bin count reveals subtle clustering in the distribution.",
        },
    },
    {
        "request": "Compare the average interest rate over time by stock index.",
        "response": {
            "type": "line",
            "data": {
                "dimension": "Date",
                "metric": "Interest Rate (%)",
                "metric_secondary": None,
                "aggregation": "mean",
                "color": "Stock Index",
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Average interest rate over time by stock index",
            "description": "Tracks mean interest rate across the timeline separated by stock index.",
            "explanation": "Color by Stock Index separates each group's monetary environment trajectory on the same time axis.",
        },
    },
    {
        "request": "Show the top 5 stock indexes by total mergers and acquisitions deals.",
        "response": {
            "type": "bar",
            "data": {
                "dimension": "Stock Index",
                "metric": "Mergers & Acquisitions Deals",
                "metric_secondary": None,
                "aggregation": "sum",
                "color": None,
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": 5,
            },
            "title": "Top 5 stock indexes by total M&A deals",
            "description": "Ranks the five stock indexes with the highest total number of mergers and acquisitions deals.",
            "explanation": "top_n is set because the user explicitly requested a ranking of the top 5 entries.",
        },
    },
    {
        "request": "Show the variance of daily low prices across stock indexes.",
        "response": {
            "type": "box",
            "data": {
                "dimension": "Stock Index",
                "metric": "Daily Low",
                "metric_secondary": None,
                "aggregation": None,
                "color": "Stock Index",
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Daily low price variance by stock index",
            "description": "Displays the spread and outliers of daily low prices for each stock index.",
            "explanation": "Variance implies distribution shape and extremes; box plots communicate both without collapsing the data into a single aggregate.",
        },
    },
    {
        "request": "Show the share of total consumer spending by stock index.",
        "response": {
            "type": "pie",
            "data": {
                "dimension": "Stock Index",
                "metric": "Consumer Spending (Billion USD)",
                "metric_secondary": None,
                "aggregation": "sum",
                "color": None,
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Share of total consumer spending by stock index",
            "description": "Shows each stock index's proportional contribution to total consumer spending.",
            "explanation": "Pie charts are the correct choice for part-of-whole questions on a low-cardinality categorical dimension.",
        },
    },
    {
        "request": "Is there a relationship between unemployment rate and bankruptcy rate by stock index?",
        "response": {
            "type": "scatter",
            "data": {
                "dimension": "Unemployment Rate (%)",
                "metric": "Bankruptcy Rate (%)",
                "metric_secondary": None,
                "aggregation": None,
                "color": "Stock Index",
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": True,
                "nbins": None,
                "top_n": None,
            },
            "title": "Unemployment rate vs bankruptcy rate by stock index",
            "description": "Plots unemployment rate against bankruptcy rate across all observations, colored by stock index.",
            "explanation": "Scatter with trend line reveals whether higher unemployment predicts higher bankruptcy rates; color separates market groups.",
        },
    },
    {
        "request": "Show how consumer spending evolved over time.",
        "response": {
            "type": "line",
            "data": {
                "dimension": "Date",
                "metric": "Consumer Spending (Billion USD)",
                "metric_secondary": None,
                "aggregation": "mean",
                "color": None,
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Consumer spending over time",
            "description": "Tracks mean consumer spending across the full dataset timeline.",
            "explanation": "A single-line chart without color is appropriate when the user asks about one metric's temporal evolution with no grouping requested.",
        },
    },
    {
        "request": "Show the distribution of government debt values.",
        "response": {
            "type": "histogram",
            "data": {
                "dimension": None,
                "metric": "Government Debt (Billion USD)",
                "metric_secondary": None,
                "aggregation": None,
                "color": None,
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": 40,
                "top_n": None,
            },
            "title": "Distribution of government debt",
            "description": "Shows how government debt values are distributed across all observations.",
            "explanation": "Government Debt has nearly 2850 unique values; 40 bins balances resolution against readability for a broadly distributed numeric column.",
        },
    },
    {
        "request": "Show trading volume over time for Dow Jones.",
        "response": {
            "type": "line",
            "data": {
                "dimension": "Date",
                "metric": "Trading Volume",
                "metric_secondary": None,
                "aggregation": "sum",
                "color": None,
            },
            "render_options": {
                "log_scale_y": True,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Trading volume over time",
            "description": "Tracks total trading volume across the timeline.",
            "explanation": "Date is a datetime column so a line chart is correct; scatter requires two numeric columns.",
        },
    },
    {
        "request": "Show the relationship between trading volume and corporate profits by stock index.",
        "response": {
            "type": "scatter",
            "data": {
                "dimension": "Trading Volume",
                "metric": "Corporate Profits (Billion USD)",
                "metric_secondary": None,
                "aggregation": None,
                "color": "Stock Index",
            },
            "render_options": {
                "log_scale_y": True,
                "show_trend_line": True,
                "nbins": None,
                "top_n": None,
            },
            "title": "Trading volume vs corporate profits by stock index",
            "description": "Plots trading volume against corporate profits colored by stock index.",
            "explanation": "Scatter requires two numeric columns; color must be a column name, not a column value.",
        },
    },
    {
        "request": "Show trading volume over time for Dow Jones.",
        "response": {
            "type": "line",
            "data": {
                "dimension": "Date",
                "metric": "Trading Volume",
                "metric_secondary": None,
                "aggregation": "sum",
                "color": None,
                "filters": {"Stock Index": ["Dow Jones"]},
            },
            "render_options": {
                "log_scale_y": True,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Trading volume over time — Dow Jones",
            "description": "Tracks total trading volume for the Dow Jones index across the timeline.",
            "explanation": "Filter restricts rows to Dow Jones only; log scale handles the wide volume range.",
        },
    },
    {
        "request": "Compare crude oil price over time for Dow Jones and S&P 500.",
        "response": {
            "type": "line",
            "data": {
                "dimension": "Date",
                "metric": "Crude Oil Price (USD per Barrel)",
                "metric_secondary": None,
                "aggregation": "mean",
                "color": "Stock Index",
                "filters": {"Stock Index": ["Dow Jones", "S&P 500"]},
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Crude oil price over time — Dow Jones vs S&P 500",
            "description": "Compares mean crude oil price trends between Dow Jones and S&P 500.",
            "explanation": "Filter restricts to two named indexes; color separates their trajectories on the same axis.",
        },
    },
    {
        "request": "Show the distribution of gold prices for S&P 500 only.",
        "response": {
            "type": "histogram",
            "data": {
                "dimension": None,
                "metric": "Gold Price (USD per Ounce)",
                "metric_secondary": None,
                "aggregation": None,
                "color": None,
                "filters": {"Stock Index": ["S&P 500"]},
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": 40,
                "top_n": None,
            },
            "title": "Gold price distribution — S&P 500",
            "description": "Shows the frequency distribution of gold prices for S&P 500 observations only.",
            "explanation": "Filter restricts rows to S&P 500; histogram is correct for single-column distribution.",
        },
    },
    {
        "request": "Show the spread of close prices for Dow Jones.",
        "response": {
            "type": "box",
            "data": {
                "dimension": "Stock Index",
                "metric": "Close Price",
                "metric_secondary": None,
                "aggregation": None,
                "color": None,
                "filters": {"Stock Index": ["Dow Jones"]},
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Close price spread — Dow Jones",
            "description": "Displays the distribution and outliers of closing prices for Dow Jones only.",
            "explanation": "Filter restricts to Dow Jones; box plot shows variance and extremes within that group.",
        },
    },
    {
        "request": "Is there a correlation between GDP growth and corporate profits for S&P 500?",
        "response": {
            "type": "scatter",
            "data": {
                "dimension": "GDP Growth (%)",
                "metric": "Corporate Profits (Billion USD)",
                "metric_secondary": None,
                "aggregation": None,
                "color": None,
                "filters": {"Stock Index": ["S&P 500"]},
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": True,
                "nbins": None,
                "top_n": None,
            },
            "title": "GDP growth vs corporate profits — S&P 500",
            "description": "Plots GDP growth against corporate profits for S&P 500 observations.",
            "explanation": "Filter restricts to S&P 500; scatter with trend line surfaces the correlation.",
        },
    },
    {
        "request": "Compare average inflation rate over time for Dow Jones and Nasdaq.",
        "response": {
            "type": "line",
            "data": {
                "dimension": "Date",
                "metric": "Inflation Rate (%)",
                "metric_secondary": None,
                "aggregation": "mean",
                "color": "Stock Index",
                "filters": {"Stock Index": ["Dow Jones", "Nasdaq"]},
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Inflation rate over time — Dow Jones vs Nasdaq",
            "description": "Tracks mean inflation rate for Dow Jones and Nasdaq across the timeline.",
            "explanation": "Filter restricts to two named indexes; color separates each group's trend line.",
        },
    },
    {
        "request": "Show average corporate profits by stock index, excluding Nasdaq.",
        "response": {
            "type": "bar",
            "data": {
                "dimension": "Stock Index",
                "metric": "Corporate Profits (Billion USD)",
                "metric_secondary": None,
                "aggregation": "mean",
                "color": None,
                "filters": {"Stock Index": ["Dow Jones", "S&P 500"]},
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Average corporate profits — Dow Jones and S&P 500",
            "description": "Compares mean corporate profits between Dow Jones and S&P 500.",
            "explanation": "Filter includes only the two requested indexes, effectively excluding Nasdaq.",
        },
    },
    {
        "request": "Show the distribution of interest rates for Dow Jones.",
        "response": {
            "type": "histogram",
            "data": {
                "dimension": None,
                "metric": "Interest Rate (%)",
                "metric_secondary": None,
                "aggregation": None,
                "color": None,
                "filters": {"Stock Index": ["Dow Jones"]},
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": 40,
                "top_n": None,
            },
            "title": "Interest rate distribution — Dow Jones",
            "description": "Shows how interest rate values are distributed for Dow Jones observations.",
            "explanation": "Filter restricts to Dow Jones rows; histogram reveals the distribution shape of the metric.",
        },
    },
    {
        "request": "Show the variance of unemployment rates for S&P 500 and Nasdaq.",
        "response": {
            "type": "box",
            "data": {
                "dimension": "Stock Index",
                "metric": "Unemployment Rate (%)",
                "metric_secondary": None,
                "aggregation": None,
                "color": "Stock Index",
                "filters": {"Stock Index": ["S&P 500", "Nasdaq"]},
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Unemployment rate variance — S&P 500 and Nasdaq",
            "description": "Displays the spread and outliers of unemployment rates for S&P 500 and Nasdaq.",
            "explanation": "Filter restricts to two indexes; box plot with color shows variance side by side.",
        },
    },
    {
        "request": "Is there a relationship between crude oil price and gold price for Dow Jones?",
        "response": {
            "type": "scatter",
            "data": {
                "dimension": "Crude Oil Price (USD per Barrel)",
                "metric": "Gold Price (USD per Ounce)",
                "metric_secondary": None,
                "aggregation": None,
                "color": None,
                "filters": {"Stock Index": ["Dow Jones"]},
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": True,
                "nbins": None,
                "top_n": None,
            },
            "title": "Crude oil price vs gold price — Dow Jones",
            "description": "Plots crude oil price against gold price for Dow Jones observations only.",
            "explanation": "Filter restricts to Dow Jones; scatter with trend line reveals the directional relationship.",
        },
    },
    {
        "request": "Show total retail sales over time for S&P 500.",
        "response": {
            "type": "line",
            "data": {
                "dimension": "Date",
                "metric": "Retail Sales (Billion USD)",
                "metric_secondary": None,
                "aggregation": "sum",
                "color": None,
                "filters": {"Stock Index": ["S&P 500"]},
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Retail sales over time — S&P 500",
            "description": "Tracks total retail sales across the timeline for S&P 500 observations.",
            "explanation": "Filter restricts to S&P 500; line chart is appropriate for temporal evolution of a single metric.",
        },
    },
    {
        "request": "Compare the spread of gold prices for all three stock indexes.",
        "response": {
            "type": "box",
            "data": {
                "dimension": "Stock Index",
                "metric": "Gold Price (USD per Ounce)",
                "metric_secondary": None,
                "aggregation": None,
                "color": "Stock Index",
                "filters": {},
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Gold price spread by stock index",
            "description": "Displays the distribution and outliers of gold prices for each stock index.",
            "explanation": "No filter needed when the user asks about all indexes; empty filters passes the full dataset.",
        },
    },
    {
        "request": "Show the distribution of bankruptcy rates for Dow Jones and S&P 500.",
        "response": {
            "type": "histogram",
            "data": {
                "dimension": None,
                "metric": "Bankruptcy Rate (%)",
                "metric_secondary": None,
                "aggregation": None,
                "color": None,
                "filters": {"Stock Index": ["Dow Jones", "S&P 500"]},
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": 40,
                "top_n": None,
            },
            "title": "Bankruptcy rate distribution — Dow Jones and S&P 500",
            "description": "Shows the frequency distribution of bankruptcy rates for two indexes.",
            "explanation": "Filter restricts to the two named indexes before computing the distribution.",
        },
    },
    {
        "request": "Show average consumer spending over time for Nasdaq only.",
        "response": {
            "type": "line",
            "data": {
                "dimension": "Date",
                "metric": "Consumer Spending (Billion USD)",
                "metric_secondary": None,
                "aggregation": "mean",
                "color": None,
                "filters": {"Stock Index": ["Nasdaq"]},
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Consumer spending over time — Nasdaq",
            "description": "Tracks mean consumer spending across the timeline for Nasdaq observations only.",
            "explanation": "Filter restricts rows to Nasdaq; line chart shows the temporal trend for that group alone.",
        },
    },
    {
        "request": "Is there a correlation between real estate index and consumer confidence for Dow Jones and Nasdaq?",
        "response": {
            "type": "scatter",
            "data": {
                "dimension": "Real Estate Index",
                "metric": "Consumer Confidence Index",
                "metric_secondary": None,
                "aggregation": None,
                "color": "Stock Index",
                "filters": {"Stock Index": ["Dow Jones", "Nasdaq"]},
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": True,
                "nbins": None,
                "top_n": None,
            },
            "title": "Real estate index vs consumer confidence — Dow Jones and Nasdaq",
            "description": "Plots real estate index against consumer confidence for two indexes, colored by group.",
            "explanation": "Filter restricts to named indexes; color separates the groups; trend line shows the overall relationship direction.",
        },
    },
    {
        "request": "Show me the data for Nasdaq.",
        "response": {
            "type": "bar",
            "data": {
                "dimension": "Stock Index",
                "metric": "Close Price",
                "metric_secondary": None,
                "aggregation": "mean",
                "color": None,
                "filters": {"Stock Index": ["Nasdaq"]},
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Average close price — Nasdaq",
            "description": "Shows average close price for Nasdaq observations.",
            "explanation": "Vague exploration requests default to a bar chart of the most representative numeric metric filtered to the named entity.",
        },
    },
    {
        "request": "Describe the dataset.",
        "response": {
            "type": "bar",
            "data": {
                "dimension": "Stock Index",
                "metric": "Close Price",
                "metric_secondary": None,
                "aggregation": "mean",
                "color": None,
                "filters": {},
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Average close price by stock index",
            "description": "Shows average close price across all stock indexes.",
            "explanation": "Dataset description requests default to a bar chart comparing the primary metric across the categorical dimension.",
        },
    },
    {
        "request": "Show the close price trend over time.",
        "response": {
            "type": "line",
            "data": {
                "dimension": "Date",
                "metric": "Close Price",
                "metric_secondary": None,
                "aggregation": "mean",
                "color": None,
                "filters": {},
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Close price trend over time",
            "description": "Average close price across all stock indexes over time.",
            "explanation": "Line chart is appropriate for time-series trends using the Date column.",
        },
    },
    {
        "request": "How did the S&P 500 close price evolve over time?",
        "response": {
            "type": "line",
            "data": {
                "dimension": "Date",
                "metric": "Close Price",
                "metric_secondary": None,
                "aggregation": "mean",
                "color": None,
                "filters": {"Stock Index": ["S&P 500"]},
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": True,
                "nbins": None,
                "top_n": None,
            },
            "title": "S&P 500 close price over time",
            "description": "Evolution of the S&P 500 average close price over time.",
            "explanation": "Filter restricts rows to S&P 500. Trend line helps identify the long-term direction.",
        },
    },
    {
        "request": "Compare the close price trend of all indexes over time.",
        "response": {
            "type": "line",
            "data": {
                "dimension": "Date",
                "metric": "Close Price",
                "metric_secondary": None,
                "aggregation": "mean",
                "color": "Stock Index",
                "filters": {},
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Close price trend by stock index",
            "description": "Compares close price evolution across all stock indexes over time.",
            "explanation": "Color encodes each index as a separate line, allowing direct comparison.",
        },
    },
    {
        "request": "Show me the volume traded over time for Dow Jones.",
        "response": {
            "type": "line",
            "data": {
                "dimension": "Date",
                "metric": "Volume",
                "metric_secondary": None,
                "aggregation": "sum",
                "color": None,
                "filters": {"Stock Index": ["Dow Jones"]},
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Dow Jones traded volume over time",
            "description": "Total volume traded by Dow Jones across time.",
            "explanation": "Filter restricts to Dow Jones. Sum aggregation is appropriate for volume.",
        },
    },
    {
        "request": "Plot open and close price over time for Nasdaq.",
        "response": {
            "type": "line",
            "data": {
                "dimension": "Date",
                "metric": "Close Price",
                "metric_secondary": "Open Price",
                "aggregation": "mean",
                "color": None,
                "filters": {"Stock Index": ["Nasdaq"]},
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Nasdaq open vs close price over time",
            "description": "Compares average open and close price for Nasdaq over time.",
            "explanation": "metric_secondary adds a second line for open price alongside close price.",
        },
    },

    # --- BAR: comparisons ---
    {
        "request": "Which stock index has the highest average close price?",
        "response": {
            "type": "bar",
            "data": {
                "dimension": "Stock Index",
                "metric": "Close Price",
                "metric_secondary": None,
                "aggregation": "mean",
                "color": None,
                "filters": {},
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Average close price by stock index",
            "description": "Compares average close price across all stock indexes.",
            "explanation": "Bar chart allows direct comparison of a numeric metric across categories.",
        },
    },
    {
        "request": "Compare total volume traded by stock index.",
        "response": {
            "type": "bar",
            "data": {
                "dimension": "Stock Index",
                "metric": "Volume",
                "metric_secondary": None,
                "aggregation": "sum",
                "color": None,
                "filters": {},
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Total volume traded by stock index",
            "description": "Total traded volume for each stock index.",
            "explanation": "Sum aggregation is appropriate for volume totals across categories.",
        },
    },
    {
        "request": "Show average high price by index on a log scale.",
        "response": {
            "type": "bar",
            "data": {
                "dimension": "Stock Index",
                "metric": "High Price",
                "metric_secondary": None,
                "aggregation": "mean",
                "color": None,
                "filters": {},
            },
            "render_options": {
                "log_scale_y": True,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Average high price by stock index (log scale)",
            "description": "Average daily high price per index with logarithmic Y axis.",
            "explanation": "Log scale reduces visual distortion when indexes differ greatly in magnitude.",
        },
    },
    {
        "request": "Show me the data for Dow Jones.",
        "response": {
            "type": "bar",
            "data": {
                "dimension": "Stock Index",
                "metric": "Close Price",
                "metric_secondary": None,
                "aggregation": "mean",
                "color": None,
                "filters": {"Stock Index": ["Dow Jones"]},
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Average close price — Dow Jones",
            "description": "Shows average close price for Dow Jones observations.",
            "explanation": "Vague exploration requests default to a bar chart of the most representative metric filtered to the named entity.",
        },
    },
    {
        "request": "Top 5 indexes by average close price.",
        "response": {
            "type": "bar",
            "data": {
                "dimension": "Stock Index",
                "metric": "Close Price",
                "metric_secondary": None,
                "aggregation": "mean",
                "color": None,
                "filters": {},
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": 5,
            },
            "title": "Top 5 indexes by average close price",
            "description": "The five stock indexes with the highest average close price.",
            "explanation": "top_n limits the bar chart to the five highest-valued categories.",
        },
    },

    # --- PIE: composition ---
    {
        "request": "What share of total volume does each index represent?",
        "response": {
            "type": "pie",
            "data": {
                "dimension": "Stock Index",
                "metric": "Volume",
                "metric_secondary": None,
                "aggregation": "sum",
                "color": None,
                "filters": {},
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Volume share by stock index",
            "description": "Proportion of total traded volume contributed by each index.",
            "explanation": "Pie chart emphasizes part-to-whole composition across categories.",
        },
    },
    {
        "request": "Show the proportion of trading days by stock index.",
        "response": {
            "type": "pie",
            "data": {
                "dimension": "Stock Index",
                "metric": "Close Price",
                "metric_secondary": None,
                "aggregation": "count",
                "color": None,
                "filters": {},
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Trading day count by stock index",
            "description": "Distribution of trading day records across stock indexes.",
            "explanation": "Count aggregation measures how many rows exist per category.",
        },
    },

    # --- SCATTER: correlation ---
    {
        "request": "Is there a correlation between open and close price?",
        "response": {
            "type": "scatter",
            "data": {
                "dimension": "Open Price",
                "metric": "Close Price",
                "metric_secondary": None,
                "aggregation": None,
                "color": None,
                "filters": {},
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": True,
                "nbins": None,
                "top_n": None,
            },
            "title": "Open price vs close price",
            "description": "Scatter plot showing the relationship between open and close price.",
            "explanation": "Scatter is appropriate for correlation analysis between two numeric columns.",
        },
    },
    {
        "request": "Plot volume against close price for S&P 500.",
        "response": {
            "type": "scatter",
            "data": {
                "dimension": "Volume",
                "metric": "Close Price",
                "metric_secondary": None,
                "aggregation": None,
                "color": None,
                "filters": {"Stock Index": ["S&P 500"]},
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Volume vs close price — S&P 500",
            "description": "Relationship between traded volume and close price for S&P 500.",
            "explanation": "Scatter with filter restricted to S&P 500 isolates the correlation for one index.",
        },
    },
    {
        "request": "Show the relationship between high and low price colored by index.",
        "response": {
            "type": "scatter",
            "data": {
                "dimension": "Low Price",
                "metric": "High Price",
                "metric_secondary": None,
                "aggregation": None,
                "color": "Stock Index",
                "filters": {},
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "High vs low price by stock index",
            "description": "Scatter showing daily price range, colored by index.",
            "explanation": "Color encodes the index to reveal whether the correlation differs across markets.",
        },
    },

    # --- HISTOGRAM: distribution ---
    {
        "request": "What is the distribution of close prices?",
        "response": {
            "type": "histogram",
            "data": {
                "dimension": None,
                "metric": "Close Price",
                "metric_secondary": None,
                "aggregation": None,
                "color": None,
                "filters": {},
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": 40,
                "top_n": None,
            },
            "title": "Distribution of close prices",
            "description": "Frequency distribution of all close price observations.",
            "explanation": "Histogram shows the shape, spread, and skewness of a numeric variable.",
        },
    },
    {
        "request": "Show the volume distribution for Nasdaq.",
        "response": {
            "type": "histogram",
            "data": {
                "dimension": None,
                "metric": "Volume",
                "metric_secondary": None,
                "aggregation": None,
                "color": None,
                "filters": {"Stock Index": ["Nasdaq"]},
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": 40,
                "top_n": None,
            },
            "title": "Volume distribution — Nasdaq",
            "description": "Frequency distribution of daily traded volume for Nasdaq.",
            "explanation": "Histogram with filter restricted to Nasdaq isolates the distribution for one index.",
        },
    },
    {
        "request": "Show the distribution of daily returns on a log scale.",
        "response": {
            "type": "histogram",
            "data": {
                "dimension": None,
                "metric": "Close Price",
                "metric_secondary": None,
                "aggregation": None,
                "color": None,
                "filters": {},
            },
            "render_options": {
                "log_scale_y": True,
                "show_trend_line": False,
                "nbins": 60,
                "top_n": None,
            },
            "title": "Close price distribution (log scale)",
            "description": "Frequency distribution of close prices with logarithmic Y axis.",
            "explanation": "Log scale is useful when the distribution is heavily skewed or spans several orders of magnitude.",
        },
    },

    # --- BOX: spread and outliers ---
    {
        "request": "Show the spread of close prices across indexes.",
        "response": {
            "type": "box",
            "data": {
                "dimension": "Stock Index",
                "metric": "Close Price",
                "metric_secondary": None,
                "aggregation": None,
                "color": None,
                "filters": {},
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Close price spread by stock index",
            "description": "Distribution and outliers of close price for each stock index.",
            "explanation": "Box plot reveals median, quartiles, and outliers for each category.",
        },
    },
    {
        "request": "Are there volume outliers in the dataset?",
        "response": {
            "type": "box",
            "data": {
                "dimension": "Stock Index",
                "metric": "Volume",
                "metric_secondary": None,
                "aggregation": None,
                "color": None,
                "filters": {},
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Volume distribution and outliers by index",
            "description": "Box plot showing volume spread and outliers per stock index.",
            "explanation": "Box chart is the most effective way to identify outliers in a numeric column.",
        },
    },
    {
        "request": "Compare price volatility between S&P 500 and Nasdaq.",
        "response": {
            "type": "box",
            "data": {
                "dimension": "Stock Index",
                "metric": "Close Price",
                "metric_secondary": None,
                "aggregation": None,
                "color": None,
                "filters": {"Stock Index": ["S&P 500", "Nasdaq"]},
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Close price volatility — S&P 500 vs Nasdaq",
            "description": "Compares the spread and outliers of close price between S&P 500 and Nasdaq.",
            "explanation": "Filter restricts to two indexes. Box plot reveals which has higher volatility.",
        },
    },

    # --- EDGE CASES ---
    {
        "request": "Describe the dataset.",
        "response": {
            "type": "bar",
            "data": {
                "dimension": "Stock Index",
                "metric": "Close Price",
                "metric_secondary": None,
                "aggregation": "mean",
                "color": None,
                "filters": {},
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Average close price by stock index",
            "description": "Overview of average close price across all stock indexes.",
            "explanation": "Ambiguous overview requests default to a bar chart of the primary metric across the main categorical dimension.",
        },
    },
    {
        "request": "Show me something interesting.",
        "response": {
            "type": "line",
            "data": {
                "dimension": "Date",
                "metric": "Close Price",
                "metric_secondary": None,
                "aggregation": "mean",
                "color": "Stock Index",
                "filters": {},
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Close price trend by stock index over time",
            "description": "Evolution of close price for all indexes, colored by index.",
            "explanation": "When the request is fully ambiguous, a time-series comparison across all indexes is the most informative default.",
        },
    },
    {
        "request": "How many records exist per index?",
        "response": {
            "type": "bar",
            "data": {
                "dimension": "Stock Index",
                "metric": "Close Price",
                "metric_secondary": None,
                "aggregation": "count",
                "color": None,
                "filters": {},
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Record count by stock index",
            "description": "Number of trading day records available for each stock index.",
            "explanation": "Count aggregation answers questions about data frequency rather than values.",
        },
    },
    {
        "request": "Show average close price only for indexes with more than 1000 records.",
        "response": {
            "type": "bar",
            "data": {
                "dimension": "Stock Index",
                "metric": "Close Price",
                "metric_secondary": None,
                "aggregation": "mean",
                "color": None,
                "filters": {},
            },
            "render_options": {
                "log_scale_y": False,
                "show_trend_line": False,
                "nbins": None,
                "top_n": None,
            },
            "title": "Average close price by stock index",
            "description": "Average close price per index — row-count filtering not supported, showing all indexes.",
            "explanation": "Filters only support column value matching. Numeric threshold filters are not supported; the chart falls back to showing all indexes.",
        },
    },
]