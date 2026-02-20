
import sys, os

# PATH FIX
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.append(PROJECT_ROOT)

import streamlit as st
import threading

from backend.tts import TextToSpeech
from service import upload_document, ask_question
from voice import listen_once, speak_async, voice_chat_loop

tts_engine = TextToSpeech()

# ---------------- PAGE ----------------
st.set_page_config(page_title="AI Document Intelligence")
st.title("🧠 AI Document Intelligence Sys (LLM + RAG)")

# ---------------- SESSION ----------------
ss = st.session_state
ss.setdefault("chat_history", [])
ss.setdefault("chat_running", False)
ss.setdefault("document_ready", False)

# ==========================================================
# 📄 Upload
# ==========================================================

col1, col2 = st.columns([4, 1])

with col1:
    uploaded = st.file_uploader(
        "📄 Upload your document",
        type=["pdf", "docx", "txt"]
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🧹 Clear Chat"):
        ss.chat_history = []
        ss.document_ready = False
        ss.chat_running = False
        st.success("Session reset successfully!")

if uploaded and not ss.document_ready:
    with st.spinner("📚 Uploading & indexing document..."):
        success, response = upload_document(uploaded)

        if success:
            ss.document_ready = True
            st.success("✅ Document indexed!")
        else:
            st.error(response)

# ==========================================================
# 💬 Typed Question
# ==========================================================

st.markdown("### 💬 Ask a Question")
typed_q = st.text_input("Type your question here...")

if st.button("Ask (Typed)"):
    if not ss.document_ready:
        st.warning("Upload document first.")
    elif not typed_q.strip():
        st.warning("Enter question.")
    else:
        with st.spinner("Thinking..."):
            success, answer = ask_question(typed_q.strip())

        if success:
            st.markdown(f"**🤖 AI:** {answer}")
            ss.chat_history.append(
                {"question": typed_q, "answer": answer}
            )
            speak_async(tts_engine, answer)
        else:
            st.error(answer)

# ==========================================================
# 🎤 Voice Controls
# ==========================================================

col1, col2 = st.columns(2)

with col1:

  if st.button("🎤 Speak Once"):

    if not ss.document_ready:
        st.warning("⚠ Please upload a document first.")

    else:
        try:
            status_box = st.empty()  # dynamic placeholder

            # Show listening message
            status_box.info("🎧 Listening...")

            # Capture voice
            query = listen_once()

            # Update UI after listening
            status_box.success(f"🧍 You said: {query}")

            # Ask backend
            with st.spinner("🧠 Thinking..."):
                success, answer = ask_question(query)

            if success:
                st.markdown(f"**🤖 AI:** {answer}")
                ss.chat_history.append(
                    {"question": query, "answer": answer}
                )
                speak_async(tts_engine, answer)

            else:
                st.error(answer)

        except Exception as e:
            st.error(f"Voice Error: {e}")

with col2:
    if st.button("🎧 Start Voice Chat"):
        if not ss.document_ready:
            st.warning("Upload document first.")
        elif not ss.chat_running:
            ss.chat_running = True
            threading.Thread(
                target=voice_chat_loop,
                args=(ss, ask_question, tts_engine),
                daemon=True
            ).start()
            st.success("Voice Chat Started")

if st.button("🛑 Stop Voice Chat"):
    ss.chat_running = False
    st.warning("Stopping Voice Chat...")

# ==========================================================
# 💬 Chat History
# ==========================================================

if ss.chat_history:
    st.markdown("---")
    st.subheader("Conversation History")

    for chat in reversed(ss.chat_history[-6:]):
        st.markdown(f"**🧍 You:** {chat['question']}")
        st.markdown(f"**🤖 AI:** {chat['answer']}")
