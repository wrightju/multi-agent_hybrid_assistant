Here’s a **README.md** draft for your project. This document provides a comprehensive overview, including the project purpose, setup instructions, and directory structure.

---

# Multi-Agent Hybrid Assistant for Intel Teams

This project is a multi-agent, conversational assistant system designed to support Intel teams (e.g., vPro, WiFi, Graphics) by enabling efficient troubleshooting and document creation. The system features a main **Operator Agent** that routes requests to specialized agents, such as the **VPro Troubleshooting Agent** and **Document Processor Agent**. Built with OpenAI's API and vector-based knowledge retrieval, this assistant provides targeted, dynamic responses.

## Project Overview

- **Operator Agent**: Handles all user interactions and routes requests to specialized agents.
- **VPro Troubleshooting Agent**: Assists with Intel vPro troubleshooting using a vector store.
- **Document Processor Agent**: Generates documents based on templates and provides Intel-standard content.

### Features
- **Conversational Interface**: The Operator Agent manages user interactions and uses OpenAI's API for intent detection and natural language understanding.
- **Vector-Based Search**: The VPro Troubleshooting Agent leverages vectorized reference documents to offer relevant troubleshooting solutions.
- **Session Management**: Tracks multi-step interactions to support continuity in troubleshooting workflows.

## Getting Started

### Prerequisites
- **Python 3.10+**
- **OpenAI API Key**: Set as an environment variable (`OPENAI_API_KEY`).
- **Required Python Packages**:
  - `openai`
  - `PyYAML` (for configuration)
  - `httpx` (required by OpenAI's new API client)

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/multi-agent_hybrid_assistant.git
   cd multi-agent_hybrid_assistant
   ```

2. **Set Up Virtual Environment** (recommended):
   ```bash
   python -m venv vpse_venv
   source vpse_venv/bin/activate  # Use vpse_venv\Scripts\activate on Windows
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Environment Variables**:
   Add your OpenAI API key as an environment variable.
   ```bash
   export OPENAI_API_KEY="your_openai_api_key"  # Use set on Windows
   ```

### Running the Project

Start the interactive assistant by running:
```bash
python vpse_assistant.py
```

The Operator Agent will guide you through a conversation. Type `exit` to end the session.

## Directory Structure

```
multi-agent_hybrid_assistant/
├── agents/
│   ├── operator.py                   # Main Operator agent
│   ├── troubleshooting_agent.py       # Troubleshooting agent for vPro issues
│   └── document_processor_agent.py    # Document Processor agent for creating Intel-standard documents
├── config/
│   ├── team_config.yaml               # Global configuration file for team-specific settings
│   ├── constants.py                   # Constants and shared settings
├── core/
│   ├── core_tools.py                  # Shared utility functions
│   ├── session_manager.py             # Manages session persistence
│   └── config_manager.py              # Loads and manages configurations
├── prompts/
│   ├── operator_prompt.md             # System prompt for the Operator Agent
│   ├── router_prompt.md               # Reserved for future routing prompts
│   ├── initial_router_prompt.md       # Reserved for initial routing prompts
├── teams/
│   ├── intel_vpro/
│   │   ├── reference_materials/
│   │   │   ├── public/
│   │   │   └── confidential/
│   │   ├── vector_store/
│   │   │   ├── public/
│   │   │   └── confidential/
│   │   ├── prompts/
│   │   │   └── intel_vpro_prompt.md
│   │   └── config.yaml                # Team-specific configuration for Intel vPro
│   ├── intel_wifi/                    # Future WiFi team setup
│   │   ├── reference_materials/
│   │   ├── vector_store/
│   │   ├── prompts/
│   │   └── config.yaml
│   └── intel_graphics/                # Future Graphics team setup
│       ├── reference_materials/
│       ├── vector_store/
│       ├── prompts/
│       └── config.yaml
├── shared/
│   ├── reference_materials/           # Shared documents for all teams
│   └── vector_store/                  # Shared vector store for team-wide knowledge
├── vpse_assistant.py                  # Main entry point for running the Operator Agent
└── README.md                          # Project documentation (you are here)
```

## Key Files

- **`vpse_assistant.py`**: Entry script to start the Operator Agent and begin interactions.
- **`operator_prompt.md`**: Customizable system prompt for the Operator Agent.
- **`team_config.yaml`**: Configuration for team-specific settings, such as agent permissions and access levels.

## Future Enhancements

- **Additional Team Integrations**: Extend support to Intel WiFi and Graphics teams.
- **Enhanced Logging**: Implement logging for conversation tracking and error handling.
- **Session-Driven Interactions**: Expand session management for multi-turn troubleshooting.

---
