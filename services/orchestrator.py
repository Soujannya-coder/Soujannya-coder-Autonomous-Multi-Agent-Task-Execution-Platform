class Orchestrator:
    def __init__(self, config, planner, executor, validator, memory):
        self.config = config
        self.planner = planner
        self.executor = executor
        self.validator = validator
        self.memory = memory
        self.max_cycles = config.get("workflow", "max_cycles", default=5)

    def run(self, session_id: str, task: str):

        print("\n🚀 ORCHESTRATOR STARTED")
        print("Session:", session_id)
        print("Task:", task)

        for cycle in range(self.max_cycles):
            print(f"\n--- Cycle {cycle+1} ---")

            # 1. Plan
            plan = self.planner.plan(task)
            print("📌 PLAN:", plan)

            # 2. Execute
            result = self.executor.execute(plan)
            print("⚙️ RESULT:", result)

            # 3. Validate
            validation = self.validator.validate(task, result)
            print("✅ VALIDATION:", validation)

            # 4. Save to memory
            self.memory.save(session_id, {
                "cycle": cycle,
                "plan": plan,
                "result": result,
                "validation": validation
            })

            # 5. Stop condition
            if isinstance(validation, dict) and validation.get("status") == "PASS":
                return {
                    "status": "SUCCESS",
                    "result": result
                }

        return {
            "status": "FAILED",
            "message": "Max cycles reached"
        }