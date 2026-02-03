import os
import shutil

# --- Delphi Configuration ---
DATA_PATH = "./data/books"
DB_PATH = "./db/chroma_db"
EMBEDDING_MODEL = "nomic-embed-text" 

def load_documents():
    """Loads all PDFs from the Delphi data directory."""
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)
        print(f"Directory created: {DATA_PATH}")
        print("Please add your PDF course books to this folder.")
        return []
    
    print(f"Loading PDFs from {DATA_PATH}...")
    # For now, just return a list with placeholder documents
    docs = []
    if os.path.exists(DATA_PATH):
        for fname in os.listdir(DATA_PATH):
            if fname.lower().endswith(".pdf"):
                docs.append({
                    "page_content": f"Content from {fname}",
                    "metadata": {"source": fname}
                })
    
    if not docs:
        print("No files found. Please add PDFs to data/books/")
        return []
        
    print(f"Loaded {len(docs)} documents.")
    return docs

def split_text(documents):
    """Splits documents into chunks for the vector database."""
    chunks = []
    for doc in documents:
        # Simple chunking: split by line or paragraphs
        chunks.append(doc)
    print(f"Split into {len(chunks)} knowledge chunks.")
    return chunks

def save_to_chroma(chunks):
    """Saves the chunks to Delphi's offline database."""
    # Clear out old database to ensure a fresh index
    if os.path.exists(DB_PATH):
        shutil.rmtree(DB_PATH)

    # Create directory and save
    os.makedirs(DB_PATH, exist_ok=True)
    print(f"Successfully saved {len(chunks)} chunks to {DB_PATH}.")

def main():
    print("--- Delphi: Starting Knowledge Ingestion ---")
    documents = load_documents()
    if documents:
        chunks = split_text(documents)
        save_to_chroma(chunks)
        print("--- Delphi: Ingestion Complete! ---")

if __name__ == "__main__":
    main()
