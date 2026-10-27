import streamlit as st
import math

# --- Page Configuration ---
st.set_page_config(
    page_title="Accessible Voice Calculator",
    page_icon="🎙️",
    layout="centered"
)

# --- Custom Styling for Accessibility & High Contrast ---
st.markdown("""
    <style>
    .main {
        background-color: #1E1E2E;
        color: #CDD6F4;
    }
    .stButton>button {
        width: 100%;
        font-size: 20px;
        font-weight: bold;
        padding: 15px;
        border-radius: 10px;
        background-color: #313244;
        color: #CDD6F4;
        border: 1px solid #45475A;
    }
    .stButton>button:hover {
        background-color: #89B4FA;
        color: #11111B;
    }
    .display-box {
        background-color: #181825;
        padding: 20px;
        border-radius: 12px;
        text-align: right;
        font-family: 'Consolas', monospace;
        font-size: 36px;
        font-weight: bold;
        color: #89B4FA;
        border: 2px solid #45475A;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Initialize Session State ---
if "expression" not in st.session_state:
    st.session_state.expression = ""
if "result" not in st.session_state:
    st.session_state.result = "0"

# --- Title & Accessibility Header ---
st.title("🎙️ Accessible Voice Calculator")
st.markdown("### *Designed as an assistive technology tool for visually impaired users.*")
st.info("💡 **Accessibility Note:** Type or click buttons. Every action is designed with high-contrast UI and auditory feedback readiness.")

# --- Display Panel ---
display_text = st.session_state.expression if st.session_state.expression else st.session_state.result
st.markdown(f'<div class="display-box">{display_text}</div>', unsafe_allow_html=True)

# --- Evaluation Logic ---
def calculate():
    try:
        clean_expr = st.session_state.expression.replace('×', '*').replace('÷', '/')
        res = eval(clean_expr, {"__builtins__": None}, {"math": math})
        formatted = f"{res:.6g}" if isinstance(res, float) else str(res)
        st.session_state.result = formatted
        st.session_state.expression = formatted
    except ZeroDivisionError:
        st.session_state.result = "Error: Division by zero"
        st.session_state.expression = ""
    except Exception:
        st.session_state.result = "Syntax Error"
        st.session_state.expression = ""

# --- Keypad Grid Layout with Unique Keys ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("C", key="clear"):
        st.session_state.expression = ""
        st.session_state.result = "0"
    if st.button("7", key="num_7"):
        st.session_state.expression += "7"
    if st.button("4", key="num_4"):
        st.session_state.expression += "4"
    if st.button("1", key="num_1"):
        st.session_state.expression += "1"
    if st.button("±", key="neg"):
        if st.session_state.expression.startswith("-"):
            st.session_state.expression = st.session_state.expression[1:]
        else:
            st.session_state.expression = "-" + st.session_state.expression

with col2:
    if st.button("(", key="open_paren"):
        st.session_state.expression += "("
    if st.button("8", key="num_8"):
        st.session_state.expression += "8"
    if st.button("5", key="num_5"):
        st.session_state.expression += "5"
    if st.button("2", key="num_2"):
        st.session_state.expression += "2"
    if st.button("0", key="num_0"):
        st.session_state.expression += "0"

with col3:
    if st.button(")", key="close_paren"):
        st.session_state.expression += ")"
    if st.button("9", key="num_9"):
        st.session_state.expression += "9"
    if st.button("6", key="num_6"):
        st.session_state.expression += "6"
    if st.button("3", key="num_3"):
        st.session_state.expression += "3"
    if st.button(".", key="dot"):
        st.session_state.expression += "."

with col4:
    if st.button("÷", key="div"):
        st.session_state.expression += "÷"
    if st.button("×", key="mul"):
        st.session_state.expression += "×"
    if st.button("-", key="sub"):
        st.session_state.expression += "-"
    if st.button("+", key="add"):
        st.session_state.expression += "+"
    if st.button("=", key="equals"):
        calculate()

# --- Voice Command Simulation ---
st.markdown("---")
st.subheader("🔊 Voice & Speech Integration")

voice_input = st.text_input("Simulate Spoken Expression (e.g., 25 * 4):", placeholder="Type what a blind user would speak...", key="voice_input_box")
if st.button("Process Spoken Input", key="process_voice_btn"):
    if voice_input:
        parsed = voice_input.lower().replace("times", "×").replace("multiplied by", "×")\
                                    .replace("divided by", "÷").replace("plus", "+")\
                                    .replace("minus", "-").replace(" ", "")
        st.session_state.expression = parsed
        calculate()
        st.success(f"Successfully processed voice command: '{voice_input}'")
        st.rerun()

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #A6ADC8;'>Built with Streamlit • Open Source Accessibility Project</p>", unsafe_allow_html=True)