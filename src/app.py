import os
import json
import streamlit as st
from pathlib import Path

# --- Configuration ---
CHROMA_PATH = "./db/chroma_db"
BOOKS_PATH = "./data/books"
DOCS_FILE = "./data/documents.json"

# --- PROMPTS ---
CHAT_PROMPT = """
You are Delphi, an expert AI tutor. 
Use the following context from the course text to answer the question strictly.
If the answer is not in the context, say "I cannot find that info in your course materials."

Context:
{context}

---

Question: {question}
Answer:
"""

QUIZ_PROMPT = """
You are a professor creating an exam. 
Based on the following context, create ONE multiple-choice question.
Format the output exactly like this:
Question: [The question text]
A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]
Correct: [The letter of the correct answer, e.g. A]
Explanation: [Brief explanation why]

Context:
{context}
"""

st.set_page_config(page_title="Delphi Study Buddy", page_icon="🏛️", layout="wide")

# --- Helpers ---
def save_uploaded_file(uploaded_file):
    if not os.path.exists(BOOKS_PATH):
        os.makedirs(BOOKS_PATH)
    file_path = os.path.join(BOOKS_PATH, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def load_documents_simple():
    """Load documents from JSON file."""
    if os.path.exists(DOCS_FILE):
        try:
            with open(DOCS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_documents_simple(docs):
    """Save documents to JSON file."""
    os.makedirs(os.path.dirname(DOCS_FILE), exist_ok=True)
    with open(DOCS_FILE, "w", encoding="utf-8") as f:
        json.dump(docs, f, indent=2)

def get_vector_db():
    """Simulate a simple vector database from saved documents."""
    docs = load_documents_simple()
    return docs if docs else None

def similarity_search(query: str, docs, k: int = 5):
    """Simple keyword-based similarity search."""
    if not docs:
        return []
    q_words = [w.lower() for w in query.split() if w.strip()]
    scored = []
    for doc in docs:
        text = doc.get("page_content", "") or ""
        text_low = text.lower()
        score = sum(text_low.count(w) for w in q_words)
        scored.append((doc, float(score)))
    scored.sort(key=lambda x: x[1], reverse=True)
    return [doc for doc, _ in scored[:k]]

def generate_quiz(docs):
    """Generate a placeholder quiz from stored documents."""
    if not docs:
        return "No documents available to generate a quiz."
    # Return a simple placeholder since we don't have Ollama/phi3.5
    return """Question: What is the main concept discussed in the course materials?
A) Fundamental understanding of the subject
B) Advanced techniques
C) Historical context
D) Practical applications
Correct: A
Explanation: The course materials focus on building a strong foundation."""

# --- SIDEBAR ---
with st.sidebar:
    st.header("📚 Knowledge Base")
    uploaded_files = st.file_uploader("Upload PDF", type=["pdf"], accept_multiple_files=True)
    if st.button("Update Brain 🧠"):
        if uploaded_files:
            with st.spinner("Digesting..."):
                for file in uploaded_files:
                    save_uploaded_file(file)
                # For now, store a simple representation
                docs = []
                for fname in os.listdir(BOOKS_PATH) if os.path.exists(BOOKS_PATH) else []:
                    fpath = os.path.join(BOOKS_PATH, fname)
                    if fname.lower().endswith(".pdf"):
                        docs.append({
                            "page_content": f"Content from {fname}",
                            "metadata": {"source": fname}
                        })
                if docs:
                    save_documents_simple(docs)
                    st.success("Updated!")
                    st.rerun()
                else:
                    st.info("No PDFs found to process.")

# --- MAIN UI ---
st.title("🏛️ Delphi: Your Offline AI Tutor")

# Create Tabs
tab1, tab2 = st.tabs(["💬 Chat Tutor", "📝 Quiz Mode"])

# --- TAB 1: CHAT ---
with tab1:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            db = get_vector_db()
            if db:
                results = similarity_search(prompt, db, k=5)
                context_text = "\n\n---\n\n".join([doc.get("page_content", "") for doc in results])
                
                # Simple placeholder response
                full_response = f"Based on the course materials: {context_text[:200]}... (Ollama not configured)"
                
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                st.error("Please upload a book first.")

# --- TAB 2: QUIZ ---
with tab2:
    st.header("Test Your Knowledge")
    
    # Initialize Quiz State
    if "quiz_data" not in st.session_state:
        st.session_state.quiz_data = None
        st.session_state.quiz_revealed = False

    if st.button("Generate New Question 🎲"):
        db = get_vector_db()
        if db:
            with st.spinner("Generating question from your books..."):
                st.session_state.quiz_data = generate_quiz(db)
                st.session_state.quiz_revealed = False
        else:
            st.error("Database not found. Please upload documents first.")

    # Display Quiz
    if st.session_state.quiz_data:
        st.markdown("---")
        st.markdown(st.session_state.quiz_data)
        
        if st.button("Show Answer 👁️"):
            st.session_state.quiz_revealed = True
            
        if st.session_state.quiz_revealed:
            st.info("Review the 'Correct' and 'Explanation' sections above.")
