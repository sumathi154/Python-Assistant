import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv
import sys
import random
import traceback
import time
from io import StringIO
import matplotlib.pyplot as plt

# 1. Configuration
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("Missing GROQ_API_KEY in .env file!")
    st.stop()

client = Groq(api_key=api_key)

st.set_page_config(page_title="PyGuide Assistant", page_icon="🐍", layout="wide")

# --- 2. HELPERS & CALLBACKS ---
def get_random_placeholder():
    examples = [
        "How to plot a sine wave?", 
        "Explain List comprehension", 
        "What are Decorators?", 
        "How to use Pandas DataFrames?",
        "Explain __init__ in Classes"
    ]
    return f"Enter your query (e.g., {random.choice(examples)})"

def clean_code(code):
    if not code: return ""
    return code.replace('“', '"').replace('”', '"').replace("‘", "'").replace("’", "'").replace('\r\n', '\n')

def reset_all_content():
    st.session_state.editor_box = "# Welcome to the Lab!\nimport matplotlib.pyplot as plt\n\nplt.plot([1, 2, 3], [10, 25, 15])\nplt.title('Quick Start Plot')\nprint('Hello Python!')"
    st.session_state.ai_response = None
    st.session_state.ai_eval = None
    if "user_query_input" in st.session_state:
        st.session_state.user_query_input = ""

# --- ENHANCED: AI EVALUATION SYSTEM (LLM-AS-JUDGE) ---
def evaluate_response(query, response):
    """Method 4: LLM-as-Judge implementation"""
    # If the response is the "Off-topic" message, we don't need a formal audit
    if "only answer queries related to Python" in response:
        return "N/A: Query was identified as off-topic."
        
    try:
        eval_chat = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a critical AI evaluator. Rate the following Python tutorial response based on Accuracy and Clarity. Provide a score out of 10 and a 1-sentence critique."},
                {"role": "user", "content": f"User Query: {query}\n\nAI Response: {response}"}
            ],
            model="llama-3.3-70b-versatile",
        )
        return eval_chat.choices[0].message.content
    except:
        return "Evaluation service temporarily unavailable."

def process_explanation():
    query = st.session_state.user_query_input.strip()
    if query:
        with st.spinner("Analyzing with AI..."):
            try:
                # Primary AI Generation with Strict Guardrails
                chat = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system", 
                            "content": (
                                "You are an expert Python tutor. Your primary rule is to ONLY answer "
                                "queries related to Python programming, libraries (like Pandas, NumPy, etc.), "
                                "and software development concepts involving Python. "
                                "If a user asks about anything else (e.g., biology, general history, cooking, trees), "
                                "politely inform them that you can only assist with Python-related questions."
                            )
                        },
                        {"role": "user", "content": query}
                    ],
                    model="llama-3.3-70b-versatile",
                )
                res = chat.choices[0].message.content
                st.session_state.ai_response = res
                
                # Automatic LLM-as-Judge Evaluation
                st.session_state.ai_eval = evaluate_response(query, res)
                
            except Exception as e:
                st.error(f"AI service error: {e}")
    else:
        st.warning("Please enter a query first!")

# --- 3. SESSION STATE ---
if "editor_box" not in st.session_state:
    st.session_state.editor_box = "import matplotlib.pyplot as plt\n\nplt.plot([1, 2, 3], [10, 40, 20])\nplt.title('Line Plot Example')\nprint('Rendering graph...')"
if "exit_session" not in st.session_state:
    st.session_state.exit_session = False
if "ai_response" not in st.session_state:
    st.session_state.ai_response = None
if "ai_eval" not in st.session_state:
    st.session_state.ai_eval = None

# --- 4. EXIT LOGIC ---
if st.session_state.exit_session:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.columns([1, 2, 1])[1].info(
        "👋 **Session Ended Successfully.**\n\n"
        "Your interactive learning lab has been closed. "
        "**To completely exit, you may now close this browser tab.**\n\n"
        "Alternatively, refresh the page to start a new session."
    )
    st.stop()

# 5. Sidebar
with st.sidebar:
    st.title("🚀 PyGuide Navigator")
    
    with st.expander("🤖 AI & Machine Learning"):
        st.write("**Tech:** TensorFlow, PyTorch, Scikit-Learn")

    with st.expander("📊 Data Science & Analysis"):
        st.write("**Tech:** Pandas, NumPy, Seaborn, Matplotlib")

    with st.expander("🏗️ Data Engineering"):
        st.write("**Tech:** PySpark, Airflow, SQL, Kafka")

    with st.expander("🌐 Web Development"):
        st.write("**Tech:** Django, Flask, FastAPI, Jinja2")

    with st.expander("⚙️ Automation & DevOps"):
        st.write("**Tech:** Selenium, Docker, Ansible, PyTest")

    with st.expander("🛡️ Cybersecurity"):
        st.write("**Tech:** Scapy, Requests, Cryptography")

    st.markdown("---")
    st.header("📚 Python Essentials")
    with st.expander("🔹 Core Syntax"):
        st.write("- Variables & Casting\n- Arithmetic/Logic Operators\n- If-Else & Match-Case")

    with st.expander("🔁 Loops & Iterables"):
        st.write("- For/While Loops\n- Lists, Tuples, Sets, Dictionaries\n- Comprehensions (List/Dict)")

    with st.expander("🛠️ Functions & Modules"):
        st.write("- Defining Functions\n- *args & **kwargs\n- Importing & Pip Packages")

    with st.expander("🏗️ OOP (Object Oriented)"):
        st.write("- Classes & Objects\n- Inheritance & Mixins\n- Dunder Methods (`__str__`, etc.)")

    with st.expander("⚡ Advanced Logic"):
        st.write("- Lambda Expressions\n- Decorators & Generators\n- Context Managers (`with` statement)")

    with st.expander("📈 Data Science Basics"):
        st.write("- Array manipulation (NumPy)\n- Data Cleaning (Pandas)\n- Basic Plotting (Matplotlib)")

    with st.expander("🧪 Testing & Debugging"):
        st.write("- Try-Except-Finally\n- Unit Testing (PyTest)\n- Logging & Debugging tools")

    st.markdown("---")

    st.subheader("📁 Upload Script")
    uploaded_file = st.file_uploader("Upload a .py file", type=["py"])
    if uploaded_file:
        content = uploaded_file.getvalue().decode("utf-8")
        st.session_state.editor_box = clean_code(content)
        st.success(f"File '{uploaded_file.name}' loaded!")

    st.markdown("---")
    st.button("🧹 Clear All Session Data", on_click=reset_all_content)
    
    if st.button("❌ Exit Session"):
        st.session_state.exit_session = True
        st.rerun()

# 6. Main UI
st.title("🐍 PyGuide: Interactive Learning Lab")
st.caption("AI-Powered Python Tutor & Real-Time Evaluation Environment")
st.markdown("---")

# 7. Query Lab
st.subheader("🔍 Query Lab")

with st.form(key="query_form", clear_on_submit=False):
    st.text_input(
        "Enter your query:", 
        placeholder=get_random_placeholder(), 
        label_visibility="collapsed",
        key="user_query_input"
    )
    st.form_submit_button("✨ Show Explanation", on_click=process_explanation)

if st.session_state.ai_response:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("💡 AI Explanation")
        st.markdown(st.session_state.ai_response)
        
        st.write("---")
        st.write("**Rate this explanation:**")
        c1, c2, c3 = st.columns([1, 1, 8])
        if c1.button("👍"): st.toast("Thanks for the positive feedback!")
        if c2.button("👎"): st.toast("We'll work to improve the response.")

    with col2:
        st.subheader("⚖️ AI Quality Audit")
        st.info(st.session_state.ai_eval)

st.markdown("---")

# 8. Code Playground
st.subheader("🚀 Code Playground")

code_to_run = st.text_area("Python Editor:", value=st.session_state.editor_box, height=350)
st.session_state.editor_box = code_to_run

if st.button("▶️ Run Code"):
    buffer = StringIO()
    sys.stdout = buffer
    plt.close('all') 
    
    start_time = time.perf_counter()
    line_count = len([line for line in code_to_run.split('\n') if line.strip()])

    try:
        exec_scope = {
            "__name__": "__main__", 
            "plt": plt, 
            "st": st,
            "random": random
        }
        
        exec(clean_code(code_to_run), exec_scope)
        end_time = time.perf_counter()
        
        execution_time = end_time - start_time
        
        st.subheader("📊 Performance Analytics")
        m1, m2 = st.columns(2)
        m1.metric("Execution Time", f"{execution_time:.4f}s")
        m2.metric("Code Complexity", f"{line_count} Lines")

        terminal_output = buffer.getvalue()
        st.subheader("Terminal Output:")
        if terminal_output:
            st.code(terminal_output, language="text")
        else:
            st.info("Code executed successfully.")
            
        if plt.get_fignums():
            st.subheader("📊 Visualization Output:")
            st.pyplot(plt.gcf())
            plt.close('all')
            
    except Exception:
        st.subheader("⚠️ Execution Error")
        st.error(traceback.format_exc().split('File "<string>", line', 1)[-1])
    finally:
        sys.stdout = sys.__stdout__