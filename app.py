import streamlit as st
from model.LLM_groq import GroqModel

# --- UI CONFIGURATION ---
st.set_page_config(page_title="Uni-Assistant", page_icon="🎓")
st.title("🎓 University Student Assistant")
st.caption("I answer questions based on official university rules.")

# --- CLASS INITIALIZATION (The "Magic" Part) ---
# We use 'session_state' so Streamlit doesn't restart the bot every time you click a button.
if "bot" not in st.session_state:
    st.session_state.bot = GroqModel(rules_file="rules.txt")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Settings")
    if st.button("Clear Chat History"):
        st.session_state.bot.clear_history()
        st.rerun()

# --- DISPLAY CHAT HISTORY ---
# We skip the first message (index 0) because that is your hidden System Prompt/Rules.
for message in st.session_state.bot.conversation_history[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- USER INPUT ---
if prompt := st.chat_input("How can I help you today?"):
    # 1. Display user message immediately
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Generate and display bot response using our Class
    with st.chat_message("assistant"):
        with st.spinner("Checking university rules..."):
            response = st.session_state.bot.chat(prompt)
            st.markdown(response)