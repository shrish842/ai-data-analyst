import streamlit as st
from analyst.loader import load_data
from analyst.profiler import suggest_prompts
from analyst.translator import prompt_to_code
from analyst.executor import run_code
from analyst.llm import ask_llm
import os

ENABLE_LLM = os.getenv("ENABLE_LLM", "false").lower() == "true"

use_llm = False

if ENABLE_LLM:
    use_llm = st.sidebar.checkbox(
        "Use local LLM (Ollama)",
        value=False
    )
else:
    st.sidebar.info("LLM features are disabled in production.")



st.set_page_config(page_title="Personal AI Data Analyst", layout="wide")
st.title("🧠 Personal AI Data Analyst")

uploaded = st.file_uploader("Upload CSV / Excel / JSON")

if not uploaded:
    st.info("Upload a file to begin")
    st.stop()

df = load_data(uploaded)
if df is None or df.empty:
    st.error("failed to load data or file is empty")
    st.stop()
st.dataframe(df.head(100))

prompts = suggest_prompts(df)
selected = st.selectbox("Suggested prompts", prompts)
custom = st.text_area("Or write your own")

final_prompt = custom.strip() or selected

if st.button("Run"):
    code = prompt_to_code(final_prompt)

    if not code:
        system_prompt = (
    "Return ONLY Python code inside ```python```.\n"
    "Use pandas, numpy, and matplotlib ONLY.\n"
    "DO NOT use seaborn, plotly, or other libraries.\n"
    "The DataFrame is named df.\n"
)
        llm_out = ask_llm(system_prompt)
        code = llm_out.split("```python")[1].split("```")[0]

    result = run_code(df, code)

    if result["type"] == "image":
        st.image(result["path"])
    elif result["type"] == "dataframe":
        st.dataframe(result["df"])
    else:
        st.text(result["output"])
