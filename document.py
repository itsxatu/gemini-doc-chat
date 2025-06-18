import streamlit as st
import google.generativeai as genai
import fitz

st.set_page_config(page_title=" PDF QA Agent", layout="centered")
API_KEY = "AIzaSyCiH8mcfqsE3ARn2Eif-Pgv3gyY3Pcf_8o"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

if "chat" not in st.session_state:
    st.session_state.chat = None
if "document_text" not in st.session_state:
    st.session_state.document_text = ""
if "messages" not in st.session_state:
    st.session_state.messages = []

st.sidebar.title("Upload PDF")
uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type=["pdf"])
if uploaded_file is not None:
    st.session_state.document_text = extract_text_from_pdf(uploaded_file)
    st.session_state.chat = model.start_chat(history=[])
    st.session_state.messages = []
    st.success("PDF successfully loaded!")

if st.sidebar.button("Clear Chat"):
    st.session_state.chat = None
    st.session_state.messages = []
    st.session_state.document_text = ""
    st.rerun()

st.title("📄PDF QA Agent")

if st.session_state.document_text:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input("Ask a question based on the document")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        prompt = f"""Based on the following document, answer the question:
        \n=== DOCUMENT START ===\n{st.session_state.document_text}\n=== DOCUMENT END ===\n\nQuestion: {user_input}"""

        response = st.session_state.chat.send_message(prompt)
        answer = response.text
        st.session_state.messages.append({"role": "assistant", "content": answer})

        with st.chat_message("assistant"):
            st.markdown(answer)

else:
    st.info("Please upload a PDF file from the sidebar to begin.")