# Tools Documentation

This document details the integrated tools used by the orchestrator agent for threat detection and classification within the system. Each tool acts as a callable, modular component that encapsulates a specific model and logic for analyzing IoT network logs.

## Tools Overview

The system uses LangChain’s Tool abstraction to provide reliable, modular access to each classifier. Tools wrap custom inference logic over local, fine-tuned LLMs. Two main tools are registered:

1. Detect Attack (`is_attack_tool`)
  - **What it does:** Says if a log entry is an Attack or Normal.
  - **How it works:** Uses a local LLM (fine-tuned) as a binary classifier.
  - **How it's built:**  
    - Entry point: `tools/is_attack.py`
    - Calls: `agents/is_attack.py` (`classify_log_entry()`)
  - **When it runs:** Automatically, on every user log submitted.
2. Classify Attack Type (`attack_type_tool`)
  - **What it does:** For logs already classified as Attack, tells you what *type* of attack it is (e.g., ddos_tcp, sql_injection, etc.).
  - **How it works:** Uses a separate LLM (fine-tuned) as a multiclass classifier.
  - **How it's built:**  
    - Entry point: `tools/attack_type.py`
    - Calls: `agents/attack_type.py` (`classify_attack()`)
  - **When it runs:** Only after the user agrees to analyze an attack in more detail.

## How Do Tools Work Internally?
### The "Agent Functions"

Despite the name, the code in `app/agents/` **does not implement full agents**, it provides the **core Python functions** that:
- Build a prompt.
- Tokenize the prompt.
- Run inference using the loaded model (on GPU or CPU).
- Decode and return the model response.

These functions are *wrapped* by the corresponding tool in `tools/` so they can be used in the agent orchestration logic.

## File Reference
```
app/
├── tools/
│ ├── is_attack.py # Tool wrapper: exposes binary classifier as a LangChain tool
│ └── attack_type.py # Tool wrapper: exposes multiclass classifier as a LangChain tool
├── models/
│ ├── binary_model.py # Loads the binary LLM model
│ └── multiclass_model.py # Loads the multiclass LLM model
├── agents/
│ ├── is_attack.py # Function: builds prompt & runs model for binary classification
│ └── attack_type.py # Function: builds prompt & runs model for multiclass classification
```
