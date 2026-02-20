
import requests

API_URL = "http://127.0.0.1:8000"


def upload_document(uploaded_file):
    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            uploaded_file.type
        )
    }

    try:
        response = requests.post(
            f"{API_URL}/upload",
            files=files,
            timeout=30
        )

        if response.status_code != 200:
            return False, response.text

        return True, response.json()

    except requests.exceptions.RequestException as e:
        return False, f"Connection error: {e}"


def ask_question(question):
    try:
        response = requests.post(
            f"{API_URL}/ask",
            data={"question": question},
            timeout=30
        )

        if response.status_code != 200:
            return False, response.text

        return True, response.json().get("answer", "No answer returned")

    except requests.exceptions.RequestException as e:
        return False, f"Connection error: {e}"
