# Delphi 🏛️
**An offline AI Study Companion with Streamlit UI.**

Delphi is a lightweight study assistant that helps you learn from course materials. Upload your PDF textbooks, and use the chat interface to ask questions or generate practice quizzes.

**Current Status:** ✅ Functional Streamlit UI with placeholder responses. Ready for LLM integration.

## 🚀 Features
- **📚 Upload PDFs:** Store course materials in your local knowledge base.
- **💬 Chat Interface:** Ask questions about your course materials.
- **📝 Quiz Mode:** Generate practice multiple-choice questions.
- **🔒 Local First:** All data stored locally in JSON format.
- **⚡ Lightweight:** No heavy dependencies—runs on any system.

## 🛠️ Tech Stack
- **Frontend:** Streamlit 1.53.1
- **Backend:** Python 3.10
- **Data Storage:** JSON (future: ChromaDB for vector embeddings)
- **Optional:** Ollama + Phi-3.5 for AI responses (not required for UI)

## ⚡ Quick Start

### 1. Prerequisites
- Python 3.10+
- Virtual environment (recommended)

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/crimznexus/delphi.git
cd delphi

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Run the Application
```bash
streamlit run src/app.py
```
The app will open at `http://localhost:8501` (or another available port).

## 📖 Usage

### Upload Books
1. Go to the sidebar
2. Click **"Upload PDF"** and select your course PDFs
3. Click **"Update Brain 🧠"** to ingest them

### Chat with Delphi
1. Navigate to the **"💬 Chat Tutor"** tab
2. Ask any question about your course materials
3. Delphi will search and provide relevant context

### Generate Quizzes
1. Go to the **"📝 Quiz Mode"** tab
2. Click **"Generate New Question 🎲"**
3. Answer the multiple-choice question
4. Click **"Show Answer 👁️"** to reveal the correct answer

## 🔌 Optional: Enable AI Responses with Ollama

To enable full AI tutor capabilities:

1. **Install [Ollama](https://ollama.com)**
2. **Pull models:**
   ```bash
   ollama pull phi3.5
   ollama pull nomic-embed-text
   ```
3. **Enable Ollama in app.py:** Uncomment the `ChatOllama` and `OllamaEmbeddings` imports (future update).

## 📁 Project Structure

```
delphi/
├── README.md              # This file
├── requirements.txt       # Python dependencies
├── LICENSE                # MIT License
├── src/
│   ├── __init__.py
│   ├── app.py            # Main Streamlit application
│   ├── ingest.py         # PDF ingestion and document storage
│   └── query_data.py     # CLI query interface
├── data/
│   ├── books/            # Store uploaded PDFs here
│   └── documents.json    # Indexed documents (auto-generated)
└── db/
    └── chroma_db/        # Vector database (future)
```

## 📋 File Descriptions

| File | Purpose |
|------|---------|
| `src/app.py` | Streamlit web UI with chat and quiz tabs |
| `src/ingest.py` | Loads PDFs and stores them as JSON documents |
| `src/query_data.py` | CLI tool for querying documents (placeholder) |
| `data/documents.json` | Auto-generated index of all uploaded materials |

## 🐛 Troubleshooting

### Issue: "Port already in use"
**Solution:** Streamlit will automatically use the next available port (8502, 8503, etc.)

### Issue: No documents found after upload
**Solution:** Ensure PDFs are in the `data/books/` folder and click "Update Brain 🧠"

### Issue: Chat responses are placeholders
**Solution:** Install Ollama and configure it in `src/app.py` for full AI responses

## 🚀 Roadmap

- [ ] Full LangChain integration with ChromaDB
- [ ] Ollama API integration for streaming responses
- [ ] PDF parsing with better text extraction (PyPDF)
- [ ] Quiz performance tracking and analytics
- [ ] Dark mode support
- [ ] Export study notes and session history

## 📝 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Create a feature branch from `dev`
2. Make your changes
3. Commit with clear messages
4. Push to your branch
5. Open a pull request

## 📧 Contact

For questions or feedback, reach out to the project maintainer or open an issue on GitHub.

---

**Happy studying with Delphi!** 🎓
