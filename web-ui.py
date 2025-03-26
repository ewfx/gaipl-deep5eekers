import streamlit as st


def get_response(query) -> str:
    return "hello!"


def set_chat_title():
    st.title("TARS")


def get_chat_ui():
    set_chat_title()

    # Initialize chat history in session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Get user input
    prompt = st.chat_input("Type your query here...")

    if prompt:
        # Append user message to session state
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.write(prompt)

        # Generate bot response (simple echo for now)
        response = get_response(prompt)

        # Append bot response to session state
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Display bot response
        with st.chat_message("assistant"):
            st.write(response)


if __name__ == "__main__":
    get_chat_ui()