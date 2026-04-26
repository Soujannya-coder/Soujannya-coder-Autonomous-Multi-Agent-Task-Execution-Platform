class BaseAgent:
    def __init__(self, name, config, llm):
        self.name = name
        self.llm = llm
        self.role = config.get("agents", name, "role")
        self.prompt = config.get("agents", name, "system_prompt")

    def run(self, input_text: str):
        full_prompt = f"""
Role: {self.role}

Instructions:
{self.prompt}

Input:
{input_text}
"""
        return self.llm.generate(full_prompt)