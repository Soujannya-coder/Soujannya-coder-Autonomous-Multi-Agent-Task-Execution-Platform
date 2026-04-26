from fastapi import FastAPI

from config.config_loader import Config
from api.routes import router, set_orchestrator

from services.llm_service import LLMService
from services.memory_service import MemoryService
from services.planner_service import PlannerService
from services.executor_service import ExecutorService
from services.validator_service import ValidatorService
from services.orchestrator import Orchestrator

import traceback
from fastapi.responses import JSONResponse

app = FastAPI(title="Autonomous Multi-Agent System")


@app.exception_handler(Exception)
def global_exception_handler(request, exc):
    print("❌ ERROR OCCURRED:")
    traceback.print_exc()

    return JSONResponse(
        status_code=500,
        content={"error": str(exc)}
    )

@app.get("/")
def root():
    return {
        "message": "API is running",
        "docs": "/docs"
    }
# Load config
config = Config()

# Init services
llm = LLMService(config)
memory = MemoryService(config)

planner = PlannerService(config, llm)
executor = ExecutorService(config, llm)
validator = ValidatorService(config, llm)

orchestrator = Orchestrator(config, planner, executor, validator, memory)

# Inject into routes
set_orchestrator(orchestrator)

app.include_router(router)