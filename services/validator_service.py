import json
import re
from services.base_agent import BaseAgent

class ValidatorService(BaseAgent):
    def __init__(self, config, llm):
        super().__init__("validator", config, llm)

    def extract_json(self, text: str):
        # Try to extract JSON block from text
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return match.group(0)
        return None

    def validate(self, task: str, result: str):
        response = self.run(f"Task: {task}\nResult: {result}")

        json_str = self.extract_json(response)

        if not json_str:
            return {"status": "FAIL", "reason": "No JSON found"}

        try:
            return json.loads(json_str)
        except Exception as e:
            return {"status": "FAIL", "reason": f"Bad JSON: {json_str}"}