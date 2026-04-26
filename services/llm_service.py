import requests

class LLMService:
    def __init__(self, config):
        self.base_url = config.get("llm_backend", "endpoint")
        self.model = config.get("llm_backend", "model_name")
        self.temperature = config.get("model", "temperature")

    def generate(self, prompt: str) -> str:
        res = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "temperature": self.temperature,
                "stream": False
            }
        )

        if res.status_code != 200:
            raise Exception(res.text)

        return res.json().get("response", "")