import argparse
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

# --- Configuration ---
CHROMA_PATH = "./db/chroma_db"
PROMPT_TEMPLATE = """
You are an expert tutor for a student. Use the following context from the course text to answer the question.
If the answer is not in the context, say "I don't find that information in your course books" and do not try to make it up.

Context:
{context}

---

Question: {question}
Answer:
"""

def main():
    # 1. Initialize the Database (The Library)
    embedding_function = OllamaEmbeddings(model="nomic-embed-text")
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # 2. Welcome Message
    print("----------------------------------------------------------------")
    print("Welcome to Delphi! 🏛️")
    print("I am ready to help you study. Type 'exit' or 'quit' to stop.")
    print("----------------------------------------------------------------")

    # 3. Chat Loop
    while True:
        query_text = input("\nStudent: ")
        
        # Check for exit commands
        if query_text.lower() in ['exit', 'quit']:
            print("Goodbye! Happy studying.")
            break
        
        # 4. Search the DB (Retrieval)
        # k=5 means "get the 5 most relevant chunks from the book"
        results = db.similarity_search_with_score(query_text, k=5)

        if not results:
            print("\nDelphi: I couldn't find any relevant context in the database.")
            continue

        # 5. Combine Context (RAG)
        # We join the text of the found pages together
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        
        # 6. Setup the Prompt
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context_text, question=query_text)

        # 7. Ask Phi-3.5 (Generation)
        # Temperature=0.3 makes it creative enough to be fluent, but strict on facts
        model = ChatOllama(model="phi3.5", temperature=0.3) 
        
        print("\nDelphi is thinking...\n")
        response_text = model.invoke(prompt)

        # 8. Output Answer
        print(f"Delphi: {response_text.content}")
        
        # Optional: Show sources (Debugging/Verification)
        # print(f"\n[Sources: {results[0][0].metadata.get('source', 'Unknown')}]")

if __name__ == "__main__":
    main()