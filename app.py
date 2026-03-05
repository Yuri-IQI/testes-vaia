import streamlit as st
from code_assistant import CodeAssistant
import pandas as pd
import numpy as np
import plotly as plt

assistant = CodeAssistant()

safe_globals = {
    "st": st,
    "pd": pd,
    "np": np,
    "plt": plt
}

st.title("Streamlit App")

prompt = st.text_input("Prompt")

if len(prompt) > 0:
    context = """
        You generate only valid Python code.
        Use streamlit to display charts.
        Do not explain anything.
        Use st.line_chart, st.bar_chart or matplotlib with st.pyplot.
        Return only python code.
    """
    
    code = assistant.generate_code(context, prompt)
    parsed_code = assistant.parse_code("python", code)
    
    st.subheader("Generated Chart")
    st.code(parsed_code, language="python")
    
    st.subheader("Output")
    
    try:
        exec(parsed_code, safe_globals)
    except Exception as e:
        st.error(e)