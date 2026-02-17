# 🚀 AI Document Intelligence System (LLM + RAG)

> Voice-enabled AI system that lets you chat with your documents using Local LLM + Retrieval-Augmented Generation (RAG).

---

## 🧠 Overview

AI Document Intelligence System is a full-stack AI application that allows users to:

- 📄 Upload PDF / DOCX / TXT documents  
- 💬 Ask questions about the document  
- 🎤 Use voice input  
- 🔊 Receive voice responses  
- ⚡ Get answers powered by Retrieval-Augmented Generation (RAG)  
- 💾 Persist vector database locally  

Built using **FastAPI + Streamlit + LangChain + FAISS + HuggingFace Models**

---

## 🏗 Architecture

```
User (Voice/Text)
        ↓
Streamlit Frontend
        ↓
FastAPI Backend
        ↓
RAG Engine
        ↓
FAISS Vector Store
        ↓
HuggingFace LLM + Embeddings
```

---

## ⚙️ Tech Stack

### 🖥 Backend
- FastAPI
- LangChain
- FAISS (Vector Database)
- HuggingFace Transformers
- Sentence Transformers
- PyPDF2
- python-docx

### 🎨 Frontend
- Streamlit
- SpeechRecognition
- pyttsx3 (Text-to-Speech)

### 🧠 Models
- **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2`
- **LLM:** `google/flan-t5-small`

---

## 📦 Features

- ✅ Multi-format Document Upload (PDF, DOCX, TXT)
- ✅ RAG-based Question Answering
- ✅ Local LLM (No OpenAI API Required)
- ✅ Persistent FAISS Vector Store
- ✅ Voice Input
- ✅ Voice Output
- ✅ Clear / Reset Session
- ✅ REST API with FastAPI
- ✅ Modular Backend Architecture

---

## 📂 Project Structure

```
AI-Document-Intelligence/
│
├── backend/
│   ├── api.py
│   ├── rag_engine.py
│   ├── document_loader.py
│   ├── embedding_loader.py
│   ├── llm_loader.py
│   ├── config.py
│   ├── tts.py
│   └── vector_store/
│
├── frontend/
│   └── app.py
│
├── data/
│   └── sample.pdf
│
└── requirements.txt
```

---

## 🚀 Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/ai-document-intelligence.git
cd ai-document-intelligence
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate:

**Windows**
```bash
venv\Scripts\activate
```

**Mac/Linux**
```bash
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

### 🔹 Start Backend (FastAPI)

```bash
cd backend
uvicorn api:app --reload
```

Backend runs at:

```
http://127.0.0.1:8000
```

Swagger API Docs:

```
http://127.0.0.1:8000/docs
```

---

### 🔹 Start Frontend (Streamlit)

```bash
cd frontend
streamlit run app.py
```

Frontend runs at:

```
http://localhost:8501
```

---

## 🧪 How It Works

1. User uploads document  
2. Text is extracted  
3. Text is chunked  
4. Embeddings are generated  
5. FAISS builds vector index  
6. On question:
   - Relevant chunks retrieved  
   - Context + question sent to LLM  
   - Answer generated  
   - Voice output returned  

---

## 🧩 RAG Configuration

Located in `backend/config.py`:

```python
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
TOP_K = 4
MAX_NEW_TOKENS = 150
```

---

## 📈 Performance

- Fully local inference
- No paid APIs
- Fast response time on CPU
- Persistent vector database
- Lightweight models optimized for performance

---

## 🔮 Future Improvements

- Chat memory with contextual awareness
- Streaming responses
- Better LLM (Mistral / Phi-2)
- Docker deployment
- Cloud deployment (AWS / GCP)
- Authentication system

---

## 👨‍💻 Author

**Chandan Kheto**  
AI/ML & Generative AI Engineer  

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!

---

