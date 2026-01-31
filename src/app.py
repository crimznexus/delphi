import os
import streamlit as st
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate

# Import ingestion logic from our existing script
# (Make sure src/ingest.py is in the same folder structure)
from src.ingest import load_documents, split_text, save_to_chroma

# --- Configuration ---
CHROMA_PATH = "./db/chroma_db"
BOOKS_PATH = "./data/books"

PROMPT_TEMPLATE = """
You are Delphi, an expert AI tutor. 
Use the following context from the course text to answer the question strictly.
If the answer is not in the context, say "I cannot find that info in your course materials."

Context:
{context}

---

Question: {question}
Answer:
"""

st.set_page_config(page_title="Delphi Study Buddy", page_icon="🏛️", layout="wide")

# --- Helper: Save Uploaded File ---
def save_uploaded_file(uploaded_file):
    if not os.path.exists(BOOKS_PATH):
        os.makedirs(BOOKS_PATH)
    file_path = os.path.join(BOOKS_PATH, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

# --- Helper: Load DB ---
@st.cache_resource
def get_vector_db():
    embedding_function = OllamaEmbeddings(model="nomic-embed-text")
    if os.path.exists(CHROMA_PATH):
        return Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    return None

# --- SIDEBAR: Manage Knowledge ---
with st.sidebar:
    st.header("📚 Knowledge Base")
    st.write("Upload new chapters or books here.")
    
    uploaded_files = st.file_uploader("Upload PDF", type=["pdf"], accept_multiple_files=True)
    
    if st.button("Update Brain 🧠"):
        if uploaded_files:
            with st.spinner("Digesting new books... this may take a moment."):
                # 1. Save files to disk
                for file in uploaded_files:
                    save_uploaded_file(file)
                
                # 2. Run Ingestion (Re-using logic from ingest.py)
                raw_docs = load_documents()
                chunks = split_text(raw_docs)
                save_to_chroma(chunks)
                
                # 3. Refresh the App
                st.cache_resource.clear()
                st.success("Delphi has learned the new material!")
                st.rerun()
        else:
            st.warning("Please upload a PDF first.")

    st.divider()
    st.caption(f"Model: Phi-3.5-mini")
    st.caption("Running Locally on CPU")

# --- MAIN PAGE: Chat Interface ---
st.title("🏛️ Delphi: Your Offline AI Tutor")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle Input
if prompt := st.chat_input("Ask a question about your books..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        db = get_vector_db()
        if db:
            # Search
            results = db.similarity_search_with_score(prompt, k=5)
            context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
            
            # Generate
            prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
            final_prompt = prompt_template.format(context=context_text, question=prompt)
            
            model = ChatOllama(model="phi3.5", temperature=0.3)
            
            # Stream response
            response_placeholder = st.empty()
            full_response = ""
            for chunk in model.stream(final_prompt):
                full_response += chunk.content
                response_placeholder.markdown(full_response + "▌")
            response_placeholder.markdown(full_response)
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        else:
            st.error("Knowledge base not found! Please upload a PDF in the sidebar.")