# src/llm_providers.py
import os
from typing import Dict, Any

class ProviderUnavailableError(Exception):
    pass


# ---------------- Base Provider ----------------
class BaseProvider:
    def __init__(self, temperature=0.7, max_tokens=512):
        self.temperature = temperature
        self.max_tokens = max_tokens

    def generate(self, payload: Dict[str, Any]):
        raise NotImplementedError


# ---------------- OpenAI Provider ----------------
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except:
    OPENAI_AVAILABLE = False


class OpenAIProvider(BaseProvider):
    def __init__(self, temperature=0.7, max_tokens=512):
        if not OPENAI_AVAILABLE:
            raise ProviderUnavailableError("OpenAI Python package not installed.")

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ProviderUnavailableError("OPENAI_API_KEY missing in .env")

        self.client = OpenAI(api_key=api_key)
        super().__init__(temperature, max_tokens)

    def generate(self, payload):
        system = payload.get("system", "")
        user = payload.get("prompt")

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ]
        )
        return response.choices[0].message.content.strip()


# ---------------- Groq Provider ----------------
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except:
    GROQ_AVAILABLE = False


class GroqProvider(BaseProvider):
    def __init__(self, temperature=0.7, max_tokens=512):
        if not GROQ_AVAILABLE:
            raise ProviderUnavailableError("groq Python package not installed.")

        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ProviderUnavailableError("GROQ_API_KEY missing in .env")

        self.client = Groq(api_key=api_key)
        super().__init__(temperature, max_tokens)

    def generate(self, payload):
        model = payload.get("model", "llama3-8b")
        prompt = payload.get("prompt")
        system = payload.get("system", "")

        response = self.client.chat.completions.create(
            model=model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()


# ---------------- Ollama Provider ----------------
try:
    import ollama
    OLLAMA_AVAILABLE = True
except:
    OLLAMA_AVAILABLE = False


class OllamaProvider(BaseProvider):
    def __init__(self, temperature=0.7, max_tokens=512):
        if not OLLAMA_AVAILABLE:
            raise ProviderUnavailableError("Ollama Python client not installed.")
        super().__init__(temperature, max_tokens)

    def generate(self, payload):
        model = payload.get("model", "mistral")
        prompt = payload.get("prompt")

        response = ollama.generate(
            model=model,
            prompt=prompt,
            options={"temperature": self.temperature}
        )
        return response["response"].strip()


# ---------------- Local Fallback ----------------
class LocalFallbackProvider(BaseProvider):
    def generate(self, payload):
        prompt = payload.get("prompt", "")
        return f"[local-fallback]\nEcho:\n{prompt}"


# ---------------- Provider Factory ----------------
class ProviderFactory:
    @staticmethod
    def create_provider(name: str, temperature=0.7, max_tokens=512):
        name = name.lower()

        if name == "openai":
            return OpenAIProvider(temperature, max_tokens)

        if name == "groq":
            return GroqProvider(temperature, max_tokens)

        if name == "ollama":
            return OllamaProvider(temperature, max_tokens)

        if name in ("local", "local-fallback"):
            return LocalFallbackProvider(temperature, max_tokens)

        raise ProviderUnavailableError(f"Unknown provider '{name}'")
