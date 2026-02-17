
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil, os

from rag_engine import RAGEngine
from document_loader import extract_text  # 🔥 import generic loader

app = FastAPI(title="AI Document Intelligence API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.engine = RAGEngine()

# 🔥 Load existing index at startup
if app.state.engine.load_index():
    print("✅ Existing vector index loaded.")
else:
    print("⚠ No existing index found. Upload document first.")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        filename = os.path.basename(file.filename)
        temp_path = os.path.join(BASE_DIR, f"temp_{filename}")

        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        text = extract_text(temp_path)
        print("Text length:", len(text))

        if not text.strip():
            raise ValueError("Extracted text is empty.")

        app.state.engine.build_index(text)
        print("Index built successfully")

        os.remove(temp_path)

        return {"message": "Document indexed and saved successfully"}

    except Exception as e:
        print("UPLOAD ERROR:", e)
        raise e

@app.post("/ask")
async def ask_question(question: str = Form(...)):
    try:
        answer = app.state.engine.query(question)
        return {"answer": answer}
    except Exception as e:
        print("ASK ERROR:", e)
        return {"error": str(e)}
