import os
import shutil
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

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
    
    loader = PyPDFDirectoryLoader(DATA_PATH)
    print(f"Loading PDFs from {DATA_PATH}...")
    documents = loader.load()
    if not documents:
        print("No files found. Please add PDFs to data/books/")
        return []
        
    print(f"Loaded {len(documents)} pages.")
    return documents

def split_text(documents):
    """Splits documents into chunks for the vector database."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,       
        chunk_overlap=80,     
        length_function=len,
        is_separator_regex=False,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split into {len(chunks)} knowledge chunks.")
    return chunks

def save_to_chroma(chunks):
    """Saves the chunks to Delphi's offline database."""
    # Clear out old database to ensure a fresh index
    if os.path.exists(DB_PATH):
        shutil.rmtree(DB_PATH)

    # Initialize the embedding function
    embedding_function = OllamaEmbeddings(model=EMBEDDING_MODEL)

    # Create and persist the database
    db = Chroma.from_documents(
        documents=chunks, 
        embedding=embedding_function, 
        persist_directory=DB_PATH
    )
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