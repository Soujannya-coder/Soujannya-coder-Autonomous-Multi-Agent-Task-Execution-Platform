# Autonomous Multi-Agent Task Execution Platform

An intelligent task orchestration system that breaks down complex tasks into executable steps and autonomously processes them through a cycle of planning, execution, and validation using multi-agent collaboration.

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Core Services](#core-services)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This platform provides an autonomous task execution framework that:

- **Breaks Down Complex Tasks**: Uses AI planning to decompose tasks into actionable steps
- **Executes Autonomously**: Processes tasks through specialized executor agents
- **Validates Results**: Ensures task completion meets requirements
- **Remembers Context**: Maintains execution history and session memory in MongoDB
- **Iterates Intelligently**: Cycles through plan-execute-validate until success
- **RESTful API**: Exposes clean HTTP endpoints for integration

### Key Features

✨ **Multi-Agent Orchestration** - Planner, Executor, and Validator agents work together  
✨ **LLM-Powered** - Uses Ollama/Llama3 for intelligent task decomposition  
✨ **Persistent Memory** - MongoDB integration for tracking execution history  
✨ **Configurable Workflow** - YAML-based configuration for easy customization  
✨ **Session Management** - Track multiple concurrent task executions  
✨ **Automatic Retry Logic** - Self-corrects through validation feedback loops  

## 🏗️ Architecture

The platform follows an orchestrator pattern with a cyclic workflow:

```
┌─────────────────────────────────────────────────────────────┐
│                     Orchestrator                             │
│  (Manages workflow cycles until task validation passes)      │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
   ┌─────────┐      ┌──────────┐    ┌──────────────┐
   │ Planner │◄─────┤ Executor │◄───┤ Validator    │
   │ (Plan)  │      │ (Execute)│    │ (Validate)   │
   └────┬────┘      └──────────┘    └──────────────┘
        │                │                  │
        └────────────────┼──────────────────┘
                         │
                    ┌────▼─────┐
                    │  Memory   │
                    │ (MongoDB) │
                    └───────────┘
```

### Workflow Cycle

1. **Plan Phase**: Planner breaks task into structured steps (JSON)
2. **Execute Phase**: Executor runs the planned steps
3. **Validate Phase**: Validator checks if task is complete
4. **Memory Phase**: Results saved to MongoDB for session tracking
5. **Loop**: Repeats until validation passes or max cycles reached

## 📦 Prerequisites

- **Python 3.8+**
- **MongoDB 4.0+** (running on localhost:27017)
- **Ollama** (running on localhost:11434 with llama3 model)

### Quick Prerequisites Check

```bash
# Check Python version
python --version

# Check MongoDB connection
# Should be running on localhost:27017

# Check Ollama
# Should be running on localhost:11434
curl http://localhost:11434/api/tags
```

## 🚀 Installation

### 1. Clone the Repository

```bash
cd Autonomous-Multi-Agent-Task-Execution-Platform
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Verify Installation

```bash
pip list
```

Expected packages:
- fastapi
- uvicorn
- pydantic
- pyyaml
- requests
- pymongo

## ⚙️ Configuration

### Configuration File: `config/config.yaml`

The platform uses YAML for configuration. Key sections:

#### Server Configuration
```yaml
server:
  host: 0.0.0.0      # Listen on all interfaces
  port: 8000         # API port
```

#### LLM Configuration
```yaml
llm_backend:
  type: ollama
  endpoint: http://localhost:11434
  model_name: llama3
```

#### Memory Configuration
```yaml
memory:
  type: mongodb
  uri: mongodb://localhost:27017
  db_name: multi_agent_db
  collection: agent_memory
  persist: true
```

#### Model Parameters
```yaml
model:
  temperature: 0.3      # Lower = more deterministic
  max_tokens: 2048      # Maximum response length
  top_p: 0.9           # Nucleus sampling
```

#### Workflow Settings
```yaml
workflow:
  max_cycles: 5         # Maximum plan-execute-validate cycles
```

### Environment Variables (Optional)

Override config values with environment variables:

```bash
# Set model temperature
export OLLAMA_TEMP=0.5

# Set MongoDB URI
export MONGODB_URI=mongodb://user:pass@host:27017
```

## 🎮 Usage

### Starting the Server

```bash
# Run directly
python main.py

# Run with uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Run in background (PowerShell)
Start-Process -NoNewWindow python main.py
```

### API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Example: Run a Task

```bash
curl -X POST "http://localhost:8000/run" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "session-001",
    "task": "Calculate the sum of 2 + 2 and verify the result"
  }'
```

Response:
```json
{
  "status": "SUCCESS",
  "result": "The sum of 2 + 2 is 4"
}
```

## 📡 API Endpoints

### 1. **POST /run** - Execute a Task

Execute a task through the multi-agent orchestration pipeline.

**Request:**
```json
{
  "session_id": "string",    // Unique session identifier
  "task": "string"           // Task description
}
```

**Response:**
```json
{
  "status": "SUCCESS|FAILED",
  "result": "string",        // Task result or error message
  "message": "string"        // Additional status message
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{"session_id": "user-123", "task": "What is 10 * 5?"}'
```

### 2. **GET /history/{session_id}** - Retrieve Session History

Get all execution cycles for a specific session.

**Response:**
```json
[
  {
    "cycle": 0,
    "plan": {...},
    "result": "...",
    "validation": {...}
  }
]
```

**Example:**
```bash
curl http://localhost:8000/history/user-123
```

### 3. **GET /health** - Health Check

Basic health status endpoint.

**Response:**
```json
{
  "status": "ok"
}
```

**Example:**
```bash
curl http://localhost:8000/health
```

### 4. **GET /** - Root Endpoint

Welcome message and documentation links.

**Response:**
```json
{
  "message": "API is running",
  "docs": "/docs"
}
```

## 📂 Project Structure

```
.
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── schemas.py             # Pydantic models for request/response
├── openapi.yaml           # OpenAPI specification
├── README.md              # This file
│
├── config/
│   ├── config.yaml        # Application configuration
│   └── config_loader.py   # Config loading utility
│
├── api/
│   └── routes.py          # FastAPI route definitions
│
└── services/
    ├── base_agent.py      # Base agent class
    ├── orchestrator.py    # Main orchestration logic
    ├── planner_service.py # Task planning agent
    ├── executor_service.py # Task execution agent
    ├── validator_service.py # Result validation agent
    ├── llm_service.py     # LLM integration (Ollama)
    └── memory_service.py  # MongoDB memory storage
```

## 🤖 Core Services

### 1. **Orchestrator** (`services/orchestrator.py`)

Main coordination engine that:
- Manages the plan-execute-validate cycle
- Handles session state
- Persists results to memory
- Implements exit conditions

**Key Method:** `run(session_id, task)`

### 2. **PlannerService** (`services/planner_service.py`)

AI-powered planning agent that:
- Decomposes tasks into steps
- Returns structured JSON format
- Uses LLM for intelligent planning

**Key Method:** `plan(task)`

### 3. **ExecutorService** (`services/executor_service.py`)

Execution engine that:
- Processes planned steps
- Handles task execution logic
- Manages dependencies between steps

**Key Method:** `execute(plan)`

### 4. **ValidatorService** (`services/validator_service.py`)

Validation agent that:
- Checks task completion
- Verifies result quality
- Provides feedback for replanning

**Key Method:** `validate(task, result)`

### 5. **LLMService** (`services/llm_service.py`)

LLM integration layer for:
- Ollama/Llama3 connectivity
- Prompt engineering
- Response parsing

**Key Method:** `generate(prompt)`

### 6. **MemoryService** (`services/memory_service.py`)

Persistent storage for:
- Session execution history
- Plan-execute-validate cycles
- MongoDB integration

**Key Methods:** `save(session_id, data)`, `fetch(session_id)`

## 🔧 Development

### Adding a New Service

1. Create file in `services/` directory
2. Inherit from `BaseAgent` if applicable
3. Implement required methods
4. Inject into Orchestrator in `main.py`
5. Add configuration to `config/config.yaml`

### Testing Locally

```bash
# Test API health
curl http://localhost:8000/health

# Test with simple task
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{"session_id": "test-1", "task": "Say hello"}'

# Check history
curl http://localhost:8000/history/test-1
```

### Debugging

Enable verbose output by modifying log levels in services:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 🆘 Troubleshooting

### MongoDB Connection Error
```
Error: Failed to connect to MongoDB
```
**Solution:** Ensure MongoDB is running on localhost:27017
```bash
# Check MongoDB
mongosh
```

### Ollama Model Not Found
```
Error: Model 'llama3' not found
```
**Solution:** Pull the model
```bash
ollama pull llama3
```

### Port Already in Use
```
Error: Address already in use
```
**Solution:** Change port in config.yaml or kill existing process
```bash
# PowerShell
Get-Process -Name python | Stop-Process
```

### FastAPI Not Responding
```
Error: Connection refused
```
**Solution:** Check if server is running
```bash
curl http://localhost:8000/health
```

---

**Built with ❤️ using FastAPI, Ollama, and MongoDB**
