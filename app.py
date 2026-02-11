import streamlit as st
from agent import get_response

st.set_page_config(page_title="StatGenie", page_icon="⚾")

st.title("⚾ MLB Stats Assistant")
st.markdown("Ask natural language  questions about batting  stats (e.g., *'Who hit the most home runs in 2023?'*)")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask a question about stats..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role":"user", "content":prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                #Call the function from agent.py
                response = get_response(prompt)
                st.markdown(response)

                # Add assistant response to chat history 
                st.session_state.messages.append({"role":"assistant", "content":response})
            except Exception as e:
                st.error(f"An error occurred: {e}")