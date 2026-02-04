import requests

OLLAMA_API_URL = "http://127.0.0.1:11434/api/generate"


class LLMError(Exception):
    pass


def ask_llm(
    prompt: str,
    model: str = "llama3.1",
    timeout: int = 60
) -> str:
    """
    Send a prompt to local Ollama via HTTP API.
    Returns the raw text response from the model.

    Expected usage:
    - Model returns Python code inside ```python ... ``` blocks
    """

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }

    try:
        response = requests.post(
            OLLAMA_API_URL,
            json=payload,
            timeout=timeout,
        )
        response.raise_for_status()

        data = response.json()

        if "response" not in data:
            raise LLMError("Malformed Ollama response")

        return data["response"]

    except requests.exceptions.ConnectionError:
        raise LLMError(
            "Ollama is not running. Start it with: ollama serve"
        )

    except requests.exceptions.Timeout:
        raise LLMError("LLM request timed out")

    except requests.exceptions.HTTPError as e:
        raise LLMError(f"Ollama HTTP error: {e}")

    except Exception as e:
        raise LLMError(f"Unexpected LLM failure: {e}")
