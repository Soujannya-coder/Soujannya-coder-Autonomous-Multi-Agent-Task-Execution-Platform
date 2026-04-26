from services.base_agent import BaseAgent

class PlannerService(BaseAgent):
    def __init__(self, config, llm):
        super().__init__("planner", config, llm)

    def plan(self, task: str):
        return self.run(task)