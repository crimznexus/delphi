# Delphi 🏛️
**An offline, CPU-optimized AI Study Companion.**

Delphi uses the **Phi-3.5** Small Language Model to act as a local tutor. It ingests your course books (PDFs), creates a local knowledge base, and answers questions using RAG (Retrieval-Augmented Generation).

## 🚀 Features
- **100% Offline:** Runs locally on your CPU using Ollama.
- **Private:** Your data never leaves your device.
- **Textbook Aware:** Answers are grounded in the specific PDFs you provide.

## 🛠️ Tech Stack
- **Model:** Phi-3.5-mini (via Ollama)
- **Embeddings:** Nomic-Embed-Text
- **Database:** ChromaDB (Local vector store)
- **Orchestrator:** LangChain

## ⚡ Quick Start

### 1. Prerequisites
- Install [Ollama](https://ollama.com)
- Pull the models:
  ```bash
  ollama pull phi3.5
  ollama pull nomic-embed-text
