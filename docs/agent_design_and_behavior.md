# Agent Design & Behavior

This document describes the architecture, behavior, and logic of the main orchestrator agent. The agent acts as a cybersecurity assistant that interacts with users through natural language, classifies network logs, and delegates tasks to specialized tools.

## Role and Responsibilities

The agent operates as a **conversational orchestrator**, implemented using LangChain's `Conversational ReAct` paradigm. Its main responsibilities are:

- Determining if the input is a valid network log.
- Deciding whether to invoke tools for threat detection and classification.
- Managing dialogue flow through memory and system-level instructions.

## Tools Integrated

The agent has access to two key tools:
- **Detect Attack** (`is_attack`): Classifies a log as Attack or Normal using a binary classifier (LLM with few-shot prompting).
- **Classify Attack Type** (`attack_type`): Invoked only after an attack is confirmed. Identifies the specific type of threat (e.g., ddos_tcp, sql_injection, xss, etc.) via a multiclass classifier.

## System Prompt

The behavior of the agent is controlled through a structured `system_message`. It enforces rules such as:

1. **Initial Processing**  
   Always attempt to detect whether the log is an attack or not.
2. **Friendly Non-Attack Handling**  
   If the log is safe, respond and ask if the user wants to analyze another.
3. **Attack Detected**  
   Offer to classify the specific attack type, only proceeding if the user agrees.
4. **Invalid Input**  
   Inform the user if the input is not recognized as a valid log.
5. **User-Centric Style**  
   Maintain a professional, clear, and multilingual tone (Spanish or English).

## Memory and Dialogue Management

The agent uses `ConversationBufferMemory` to keep track of the full interaction history. This ensures:

- Contextual continuity in longer conversations.
- Reuse of previous user input and clarifications.
- Human-like interaction over multiple log reviews.

## Agent Configuration Summary

| Component             | Value / Description                                 |
|----------------------|------------------------------------------------------|
| LLM                  | `ChatMistralAI` via LangChain                        |
| Agent Type           | `ConversationalReActDescription`                    |
| Temperature          | 0.7                                                  |
| Max Tokens           | 512                                                  |
| Tools                | `is_attack_tool`, `attack_type_tool`                |
| Memory               | `ConversationBufferMemory`                          |
| Prompt Language      | Multilingual (based on user input)                  |
| Orchestration Script | `app/orchestrator.py`                               |

## File Reference

The agent logic is implemented in:
```
app/
├── orchestrator.py # Agent setup logic
├── tools/
│ ├── is_attack.py # Binary classification tool
│ └── attack_type.py # Multiclass classification tool
├── agents/
│ ├── is_attack.py # Prompt + logic (binary)
│ └── attack_type.py # Prompt + logic (multiclass)
```
