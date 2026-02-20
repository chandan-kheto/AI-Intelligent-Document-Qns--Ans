
import os
from . import config
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

from .llm_loader import load_llm
from .embedding_loader import load_embeddings


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VECTOR_PATH = os.path.join(BASE_DIR, "vector_store")


class RAGEngine:
    def __init__(self):
        self.embeddings = None
        self.llm = None
        self.vector_store = None
        self.qa_chain = None

    # ---------------- LOAD MODELS ----------------
    def load_models(self):
        if self.embeddings is None:
            print("🔎 Loading Embeddings...")
            self.embeddings = load_embeddings()

        if self.llm is None:
            print("🤖 Loading LLM...")
            self.llm = load_llm()

    # ---------------- CUSTOM PROMPT ----------------
    def get_prompt(self):
        prompt_template = """
        You are an expert AI assistant.

        Use ONLY the information from the provided context to answer the question.

        Guidelines:
        - Be clear and concise.
        - If the answer is not found in the context, say:
          "The document does not contain this information."
        - Do NOT hallucinate.
        - Do NOT use external knowledge.

        Context: {context}

        Question: {question}

        Detailed Answer:
        ."""
        return PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )

    # ---------------- BUILD INDEX ----------------
    def build_index(self, document_text: str):
        self.load_models()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP
        )

        documents = splitter.create_documents([document_text])

        self.vector_store = FAISS.from_documents(
            documents,
            self.embeddings
        )

        # Save index
        os.makedirs(VECTOR_PATH, exist_ok=True)
        self.vector_store.save_local(VECTOR_PATH)

        prompt = self.get_prompt()

        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.vector_store.as_retriever(
                search_kwargs={"k": config.TOP_K}
            ),
            chain_type_kwargs={"prompt": prompt},
            return_source_documents=False
        )

        print("✅ Index built successfully.")

    # ---------------- LOAD INDEX ----------------
    def load_index(self):
        self.load_models()

        index_file = os.path.join(VECTOR_PATH, "index.faiss")
        store_file = os.path.join(VECTOR_PATH, "index.pkl")

        if os.path.exists(index_file) and os.path.exists(store_file):

            self.vector_store = FAISS.load_local(
                VECTOR_PATH,
                self.embeddings,
                allow_dangerous_deserialization=True
            )

            prompt = self.get_prompt()

            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                retriever=self.vector_store.as_retriever(
                    search_kwargs={"k": config.TOP_K}
                ),
                chain_type_kwargs={"prompt": prompt},
                return_source_documents=False
            )

            print("✅ Vector index loaded from disk.")
            return True

        print("⚠ No saved index found.")
        return False

    # ---------------- QUERY ----------------
    def query(self, question: str) -> str:
        if self.qa_chain is None:
            raise ValueError("No document indexed yet. Please upload a document first.")

        response = self.qa_chain.invoke({"query": question})
        return response.get("result", "No answer generated.")
