from transformers import AutoTokenizer, AutoModelForCausalLM

def load_multiclass_model(
    model_path: str = "./models/DeepSeek-R1-Distill-Llama-8B",
    device: str = "cuda",
    torch_dtype = "auto",
):
    """
    Loads a language model and tokenizer from a local directory using Hugging Face Transformers.

    Args:
        model_path (str): Path to the local fine-tuned model directory.
        device (str): Device to load the model onto ("cuda" or "cpu").
        torch_dtype: Data type for model weights (e.g., torch.float16, "auto").

    Returns:
        model (PreTrainedModel): The loaded causal language model.
        tokenizer (PreTrainedTokenizer): The associated tokenizer.
    """
    tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)

    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        device_map="auto" if device == "cuda" else None,
        torch_dtype=torch_dtype,
        local_files_only=True
    )

    return model, tokenizer
