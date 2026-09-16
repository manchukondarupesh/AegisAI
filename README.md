# AegisAI

## Multi-Agent Drone Intelligence & Autonomous Operations Platform

AegisAI is an AI-powered multi-agent system designed to demonstrate intelligent drone monitoring, operational risk prediction, document-based reasoning, and autonomous decision support.

## Key Features

- Multi-agent architecture
- Supervisor-based agent routing
- Drone database management using SQLite
- RAG-based safety document retrieval
- Local LLM using Ollama and Llama 3.2
- PyTorch-based drone risk prediction
- FastAPI backend
- Interactive web dashboard
- Drone telemetry monitoring
- Mission monitoring
- Safety alert monitoring

## System Architecture

User
↓
AegisAI Dashboard
↓
FastAPI Backend
↓
Supervisor Agent
↓
├── Drone Database Agent
├── RAG Agent
└── ML Agent

## Technologies Used

- Python
- PyTorch
- LangChain
- LangGraph
- Ollama
- Llama 3.2
- ChromaDB
- HuggingFace Embeddings
- SQLite
- FastAPI
- HTML
- CSS
- JavaScript

## Agents

### 1. Drone Database Agent

Retrieves:

- Drone status
- Battery levels
- Temperature
- Telemetry
- Missions
- Safety alerts

### 2. RAG Agent

Retrieves information from the AegisAI Drone Safety and Operations Manual and provides answers using the retrieved documents.

### 3. ML Agent

Uses drone telemetry including:

- Battery
- Temperature
- Signal strength

to predict operational risk as LOW or HIGH.

### 4. Supervisor Agent

Analyzes the user's question and routes it to the appropriate specialist agent.

## Example Queries

```text
Which drone has low battery?
## ML Model Setup

The drone risk prediction model is generated locally and is not stored in the GitHub repository.

To train and generate the model files, run:

```bash
python ml/drone_risk_train.py