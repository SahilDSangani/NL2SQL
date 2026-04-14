# =============================================================================
# app.py — StatGenie Streamlit web interface
# =============================================================================
# HOW TO RUN:
#   Prerequisites:
#     1. Install dependencies:
#          pip install -r requirements.txt
#     2. Start the local LLM server (llama.cpp) on port 8080:
#          llama-server --model <path-to-model> --port 8080
#     3. Make sure mlb_batting_stats.db exists (run ingest_data.py if not)
#
#   Launch the app:
#     streamlit run app.py
#
#   Opens at http://localhost:8501 in your browser.
#   Type any question in the chat box — try "Hi" or "Who led the MLB in HR in 2023?"
# =============================================================================

import streamlit as st
from agent import get_response

st.set_page_config(page_title="StatGenie", page_icon="⚾")

st.title("⚾ StatGenie — MLB Stats Assistant")
st.markdown("Ask questions about MLB batting stats in plain English.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("sql"):
            with st.expander("View SQL Query"):
                st.code(message["sql"], language="sql")

# Handle new user input
if prompt := st.chat_input("Ask about stats, or just say hi..."):
    # Show and store user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Build chat history in OpenAI format for the agent (text only, no sql keys)
    history = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages[:-1]  # exclude the message we just added
    ]

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = get_response(prompt, chat_history=history)

        st.markdown(result["answer"])

        if result["sql"]:
            with st.expander("View SQL Query"):
                st.code(result["sql"], language="sql")

    # Store assistant message (include sql so it re-renders on rerun)
    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"],
        "sql": result["sql"],
    })
