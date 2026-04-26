from services.base_agent import BaseAgent

class ExecutorService(BaseAgent):
    def __init__(self, config, llm):
        super().__init__("executor", config, llm)
        self.tools = config.get("agents", "executor", "tools", default=[])

    def execute(self, plan: str):
        return self.run(f"{plan}\nAvailable tools: {self.tools}")