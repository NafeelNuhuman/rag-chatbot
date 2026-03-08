import streamlit as st
import config
import rag

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("RAG Chatbot",text_alignment="left")

uploaded_file = st.file_uploader(label="Choose a file",
                 max_upload_size=10, 
                 accept_multiple_files="true",
                 type="pdf")

if uploaded_file is not None:
    if uploaded_file is isinstance(uploaded_file, list):
        for file in uploaded_file:
            # save the file to data directory
            with open(f"{config.DATA_PATH}/{file.name}", "wb") as f:
                f.write(file.getbuffer())
            # index the document by passing the file path to the index_document function
            with st.spinner(f"Indexing {file.name}..."):
                rag.index_document(f"data/{file.name}")
            print(f"Indexed file: {file.name}")
    else:
        with open(f"{config.DATA_PATH}/{uploaded_file.name}", "wb") as f:
            f.write(uploaded_file.getbuffer())
        with st.spinner(f"Indexing {uploaded_file.name}..."):
            rag.index_document(f"data/{uploaded_file.name}")
        print(f"Indexed file: {uploaded_file.name}")


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if question := st.chat_input("Ask a question about your documents"):
    # 1. Add user message to history
    st.session_state.messages.append({"role":"user", "content":question})
    # 2. Display user message
    with st.chat_message("user"):
        st.markdown(question)
    # 3. Call rag.query()
    with st.spinner("Generating response..."):
        response = rag.query(question)
    # 4. Add assistant response to history
    st.session_state.messages.append({"role":"assistant", "content":response})
    # 5. Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response)