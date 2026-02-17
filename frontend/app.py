
import streamlit as st
import requests, threading, os, sys
import speech_recognition as sr

# ---------------- PATH SETUP ----------------

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.append(PROJECT_ROOT)

from backend.tts import TextToSpeech

tts_engine = TextToSpeech()

API_URL = "http://127.0.0.1:8000"

# ---------------- PAGE CONFIG ----------------

st.set_page_config(page_title="AI Document Intelligence", page_icon="🧠")

# ---------------- HEADER (Title + Reset Button) ----------------

st.title("🧠 AI Document Intelligence System (LLM + RAG)")

# ---------------- SESSION STATE ----------------

ss = st.session_state
ss.setdefault("chat_history", [])
ss.setdefault("chat_running", False)
ss.setdefault("document_ready", False)

# ==========================================================
# 📄 DOCUMENT UPLOAD
# ==========================================================

# ---------------- UPLOAD + RESET (Same Row) ----------------

col1, col2 = st.columns([4,1])

with col1:
    uploaded = st.file_uploader(
        "📄 Upload your document",
        type=["pdf", "docx", "txt"],
        label_visibility="visible"
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)  # align vertically
    if st.button("🧹 Clear Chat"):
        st.session_state.chat_history = []
        st.session_state.document_ready = False
        st.session_state.chat_running = False
        st.success("Session reset successfully!")


if uploaded and not ss.document_ready:
    with st.spinner("📚 Uploading & indexing document..."):

        files = {
            "file": (
                uploaded.name,
                uploaded.getvalue(),
                uploaded.type
            )
        }

        try:
            response = requests.post(f"{API_URL}/upload", files=files)

            if response.status_code == 200:
                ss.document_ready = True
                st.success("✅ Document indexed successfully!")
            else:
                st.error(f"❌ Upload failed: {response.text}")

        except Exception as e:
            st.error(f"❌ Connection error: {e}")

# ==========================================================
# 🤖 ASK FUNCTION
# ==========================================================

def ask_api(question):
    try:
        response = requests.post(
            f"{API_URL}/ask",
            data={"question": question}
        )

        if response.status_code != 200:
            return f"❌ Backend Error: {response.text}"

        data = response.json()

        return data.get("answer", "❌ No answer returned")

    except Exception as e:
        return f"❌ Connection error: {e}"

# ==========================================================
# 💬 TYPED QUESTION
# ==========================================================

st.markdown("### 💬 Ask a Question")
typed_q = st.text_input("Type your question here...")

if st.button("Ask (Typed)"):

    if not ss.document_ready:
        st.warning("⚠ Please upload a document first.")
    elif not typed_q.strip():
        st.warning("⚠ Please enter a question.")
    else:
        with st.spinner("🧠 Thinking..."):
            answer = ask_api(typed_q.strip())

        st.markdown(f"**🤖 AI:** {answer}")
        ss.chat_history.append({"question": typed_q, "answer": answer})

        # 🔊 Speak answer
        if not answer.startswith("❌"):
            threading.Thread(
                target=tts_engine.speak,
                args=(answer,),
                daemon=True
            ).start()

# ==========================================================
# 🎤 VOICE RECOGNITION
# ==========================================================

def listen_once():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎧 Listening...")
        audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
    return recognizer.recognize_google(audio)

# ---------------- Single Voice ----------------

if st.button("🎤 Speak Once"):

    if not ss.document_ready:
        st.warning("⚠ Please upload a document first.")
    else:
        try:
            query = listen_once()
            st.success(f"🧍 You said: {query}")

            with st.spinner("🧠 Thinking..."):
                answer = ask_api(query)

            st.markdown(f"**🤖 AI:** {answer}")
            ss.chat_history.append({"question": query, "answer": answer})

            if not answer.startswith("❌"):
                threading.Thread(
                    target=tts_engine.speak,
                    args=(answer,),
                    daemon=True
                ).start()

        except Exception as e:
            st.error(f"Voice Error: {e}")

# ==========================================================
# 🔄 CONTINUOUS VOICE CHAT
# ==========================================================

def voice_chat_loop():
    recognizer = sr.Recognizer()

    while True:
        if not ss.get("chat_running", False):
            break

        try:
            with sr.Microphone() as source:
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)

            query = recognizer.recognize_google(audio)

            answer = ask_api(query)

            # Save to session safely
            ss.chat_history.append({"question": query, "answer": answer})

            if not answer.startswith("❌"):
                tts_engine.speak(answer)

        except:
            pass

# ---------------- Buttons ----------------

col1, col2 = st.columns(2)

with col1:
    if st.button("🎧 Start Voice Chat"):
        if not ss.document_ready:
            st.warning("⚠ Please upload a document first.")
        elif not ss.chat_running:
            ss.chat_running = True
            threading.Thread(target=voice_chat_loop, daemon=True).start()
            st.success("Voice Chat Started")

with col2:
    if st.button("🛑 Stop Voice Chat"):
        ss.chat_running = False
        st.warning("Stopping Voice Chat...")

# ==========================================================
# 💬 CHAT HISTORY
# ==========================================================

if ss.chat_history:
    st.markdown("---")
    st.subheader("💬 Conversation History")

    for chat in reversed(ss.chat_history[-6:]):
        st.markdown(f"**🧍 You:** {chat['question']}")
        st.markdown(f"**🤖 AI:** {chat['answer']}")

