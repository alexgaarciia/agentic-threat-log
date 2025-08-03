# Deployment Guide

This guide describes the minimal steps required to deploy and run the agentic-threat-log system on a local machine or server.

## 1. Requirements
- Python 3.10+ (recommended)
- A CUDA-compatible GPU (recommended for inference performance)

## 2. Environment Setup
### 1. Clone the repository
```
git clone https://github.com/alexgaarciia/agentic-threat-log.git
cd agentic-threat-log
```

### 2. Environment variables
Create a `.env` file in the project root, based on the provided `.env.example`. At minimum, set the following variables:
```
MISTRAL_API_KEY=your-mistral-api-key
MISTRAL_MODEL_NAME=mistral-tiny  # or mistral-medium, mistral-large, etc.
```

### 3. Run the application
Start the Streamlit interface with:
```
streamlit run app/main.py
```
