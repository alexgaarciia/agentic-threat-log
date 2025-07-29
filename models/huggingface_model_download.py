from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="unsloth/DeepSeek-R1-Distill-Llama-8B",
    repo_type="model",
    local_dir="C:/Users/algar/Documents/Travail/agentic-threat-log/models/DeepSeek-R1-Distill-Llama-8B"
)
