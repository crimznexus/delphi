import argparse
import json
import os

# --- Configuration ---
CHROMA_PATH = "./db/chroma_db"
DOCS_FILE = "./data/documents.json"
PROMPT_TEMPLATE = """
You are an expert tutor for a student. Use the following context from the course text to answer the question.
If the answer is not in the context, say "I don't find that information in your course books" and do not try to make it up.

Context:
{context}

---

Question: {question}
Answer:
"""

def load_documents():
    """Load documents from JSON file."""
    if os.path.exists(DOCS_FILE):
        try:
            with open(DOCS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

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

def main():
    # 1. Load Documents
    docs = load_documents()
    
    # 2. Welcome Message
    print("----------------------------------------------------------------")
    print("Welcome to Delphi! 🏛️")
    print("I am ready to help you study. Type 'exit' or 'quit' to stop.")
    print("(Note: This is a text-based demo with placeholder responses)")
    print("----------------------------------------------------------------")

    # 3. Chat Loop
    while True:
        query_text = input("\nStudent: ")
        
        # Check for exit commands
        if query_text.lower() in ['exit', 'quit']:
            print("Goodbye! Happy studying.")
            break
        
        # 4. Search the DB (Retrieval)
        results = similarity_search(query_text, docs, k=5)

        if not results:
            print("\nDelphi: I couldn't find any relevant context in the database.")
            continue

        # 5. Combine Context (RAG)
        context_text = "\n\n---\n\n".join([doc.get("page_content", "") for doc in results])
        
        # 6. Setup the Prompt
        prompt = PROMPT_TEMPLATE.format(context=context_text, question=query_text)

        # 7. Placeholder Response (Ollama not configured)
        print("\nDelphi: Based on your course materials:")
        print(f"Context: {context_text[:200]}...")
        print("(Full AI response would require Ollama configured)")

if __name__ == "__main__":
    main()
