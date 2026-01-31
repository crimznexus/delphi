import streamlit as st
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate

# --- Configuration ---
CHROMA_PATH = "./db/chroma_db"
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

# --- Page Setup ---
st.set_page_config(page_title="Delphi Study Buddy", page_icon="🏛️")
st.title("🏛️ Delphi: Your Offline AI Tutor")

# --- Load Database (Cached) ---
@st.cache_resource
def get_vector_db():
    embedding_function = OllamaEmbeddings(model="nomic-embed-text")
    return Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

db = get_vector_db()

# --- Initialize Session State (Chat History) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display Chat History ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Handle User Input ---
if prompt := st.chat_input("Ask a question about your books..."):
    # 1. Display User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Generate Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")

        # Search DB
        results = db.similarity_search_with_score(prompt, k=5)
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        
        # Prepare Prompt
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        final_prompt = prompt_template.format(context=context_text, question=prompt)

        # Run Model (Streamed)
        model = ChatOllama(model="phi3.5", temperature=0.3)
        response_text = model.invoke(final_prompt).content
        
        # Display Final Answer
        message_placeholder.markdown(response_text)

    # 3. Save History
    st.session_state.messages.append({"role": "assistant", "content": response_text})