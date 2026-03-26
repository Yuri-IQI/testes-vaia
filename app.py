import streamlit as st
from code_assistant import CodeAssistant
from plotly import express as px
from examples import bar_chart_exp, line_chart_exp
from json_parser import extract_json, parse_json

@st.cache_resource
def load_assistant():
    return CodeAssistant()

assistant = load_assistant()

st.title("Streamlit App")

context = """
    You are a JSON generator.

    Return ONLY valid JSON.

    STRICT RULES:
    - No markdown
    - No ``` blocks
    - No explanations
    - No text before or after JSON
    - Output must start with { and end with }

    JSON must contain ONLY:
    - numbers
    - strings
    - arrays

    DO NOT generate code like Math.pow or loops.
"""

user_input = st.text_input("Prompt")

def build_prompt(user_input):
    return f"""
        You are a system that generates chart JSON.

        Return ONLY valid JSON.

        Rules:
        - No markdown
        - No explanations
        - Output must start with {{ and end with }}
        - Values must be explicit numbers

        Format:
        {{
        "type": "bar" | "line" | "pie",
        "labels": string[],
        "values": number[],
        "title": string
        }}

        Examples:

        Input: bar chart with values 10, 20, 30
        Output:
        {{"type":"bar","labels":["A","B","C"],"values":[10,20,30],"title":"Bar chart"}}

        Input: line chart with values jan, feb: 5, 8
        Output:
        {{"type":"line","labels":["jan","feb"],"values":[5,8],"title":"Sales"}}

        Now generate the JSON for:

        {user_input}
    """
    
def validate(data):
    required = ["type", "labels", "values", "title"]

    if data["type"] not in ["bar", "line", "pie"]:
        return False, "Invalid type"

    if not all(isinstance(v, (int, float)) for v in data["values"]):
        return False, "Values should be numbers"

    for key in required:
        if key not in data:
            return False, f"Missing {key}"

    if data["type"] not in ["bar", "line", "pie"]:
        return False, "Invalid type"

    if len(data["labels"]) != len(data["values"]):
        return False, "Labels and values mismatch"

    return True, None

def render_chart(data):
    if data["type"] == "bar":
        fig = px.bar(x=data["labels"], y=data["values"], title=data.get("title"))

    elif data["type"] == "line":
        fig = px.line(x=data["labels"], y=data["values"], title=data.get("title"))

    elif data["type"] == "pie":
        fig = px.pie(names=data["labels"], values=data["values"], title=data.get("title"))

    else:
        return None

    return fig

if user_input:
    response = assistant.generate_code(context, build_prompt(user_input))
    print("Raw response:", response)
    
    json_str = extract_json(response)
    print("Extracted JSON string:", json_str)
    
    data = None
    if not json_str:
        st.error("Não foi possível extrair JSON")
    else:
        data = parse_json(json_str)

    if not data:
        st.error("Erro ao interpretar JSON")
    else:
        st.json(data)
        valid, error = validate(data)

        if not valid:
            st.error(error)
        else:
            fig = render_chart(data)
            st.plotly_chart(fig)