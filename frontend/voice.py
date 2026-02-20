
import speech_recognition as sr
import threading

def listen_once():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)

    return recognizer.recognize_google(audio)


def speak_async(tts_engine, text):
    threading.Thread(
        target=tts_engine.speak,
        args=(text,),
        daemon=True
    ).start()


def voice_chat_loop(session_state, ask_question, tts_engine):
    recognizer = sr.Recognizer()

    while session_state.get("chat_running", False):
        try:
            with sr.Microphone() as source:
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)

            query = recognizer.recognize_google(audio)
            success, answer = ask_question(query)

            if success:
                session_state.chat_history.append(
                    {"question": query, "answer": answer}
                )
                tts_engine.speak(answer)

        except Exception:
            pass
