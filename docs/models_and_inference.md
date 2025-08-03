# Models & Inference

This document summarizes the models used for cyberattack detection and classification, as well as the inference workflow in the system.

## Overview

The system uses two local language model, each providing a different classification purpose, and both are loaded from local directories.

## Models Used
1. Binary Classification Model
- **Purpose:** Detects if a log is an Attack or Normal.
- **Location:** `./models/<your-model-here>` (used by `app/models/binary_model.py`)

2. Multiclass Classification Model
- **Purpose:** For logs already detected as attacks, predicts the specific type (e.g., ddos_tcp, sql_injection, xss, etc.).
- **Location:** `./models/<your-model-here>` (used by `app/models/multiclass_model.py`)

## Model Loading

- Models are loaded at runtime using Hugging Face Transformers (`AutoModelForCausalLM` and `AutoTokenizer`).
- The functions `load_binary_model()` and `load_multiclass_model()` (in `models/binary_model.py` and `models/multiclass_model.py`) handle the loading and return both the model and the tokenizer.

## Inference Workflow

- When a log is to be analyzed, the corresponding Python function builds a prompt using the user log plus a set of few-shot examples.
- The prompt is tokenized and passed to the model for text generation.
- The generated output is decoded and parsed to extract the predicted class label.
- This process is the same for both binary and multiclass classification, only changing the examples and expected output.

## Model Replacement or Update

- To use a new or updated model, simply place it in the appropriate `models/` directory and update the path if needed.
- Both loaders are compatible with Hugging Face format (local directory with model weights and config).
