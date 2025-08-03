# Agentic Threat Log Detection
## Overview
This project implements an AI-powered assistant to analyze IoT network logs and detect cybersecurity threats. It uses a conversational agent that orchestrates two specialized language model tools:
- A binary classifier that detects whether a log indicates an attack or normal behavior.
- A multiclass classifier that identifies the specific type of attack, once confirmed.

## Project structure
```
agentic-threat-log/
│
├── app/
│   ├── main.py                               # Entry point (Streamlit interface)
│   ├── orchestrator.py                       # Builds the agent with tools and prompts
│   ├── tools/
│   │   ├── is_attack.py                      # Tool: Attack vs. Normal classification
│   │   ├── attack_type.py                    # Tool: Multiclass attack type classification
│   ├── agents/
│   │   ├── is_attack.py                      # Prompt + inference logic (binary)
│   │   ├── attack_type.py                    # Prompt + inference logic (multiclass)
│   ├── models/
│   │   ├── binary_model.py                   # Loader for binary LLM
│   │   ├── multiclass_model.py               # Loader for multiclass LLM
|   |   ├── multiclass_model_v2.py            # Loader for fine-tuned multiclass LLM
│
├── models/
│   ├── huggingface_model_download.py         # Downloads a specified Hugging Face momdel
│   └── [Model folders]                       # Locally stored models
│
├── images/
│   └── architecture.png                      # Architecture diagram
│
└── README.md
```

## System Architecture
The system architecture consists of:
- A LangChain Conversational Agent.
- Two custom LangChain tools:
  - Detect Attack → binary classifier.
  - Classify Attack Type → multiclass classifier.
- Fine-tuned models loaded using Hugging Face or Unsloth.
- A Streamlit-based UI for interactive local usage.

Tool invocation is conditional and conversational:
1. First, the assistant uses the binary tool to detect whether the log is an attack.
2. If so, it asks the user whether to classify the attack.
3. Only upon confirmation, it uses the multiclass classifier.

<p align="center">
  <img src="https://github.com/alexgaarciia/agentic-threat-log/blob/main/images/architecture.png" alt="Architecture Diagram" width="750">
</p>

## Documentation Index
These pages provide technical deep-dives into each component of the system:
- [Agent Design & Behavior](docs/agent_design_and_behavior.md)  
- [Tools Documentation](docs/tools_overview.md)  
- [Models & Inference](docs/models_and_inference.md)  
- [Deployment Guide](docs/deployment_guide.md)  
