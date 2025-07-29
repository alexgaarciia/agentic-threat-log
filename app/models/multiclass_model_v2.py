from unsloth import FastLanguageModel

def load_multiclass_model(
    model_path: str = "./models/DeepSeek-R1-Distill-Llama-8B-fine-tuned",
    max_seq_length: int = 2048,
    dtype = None,
    load_in_4bit: bool = True,
):
    """
    Loads a locally fine-tuned language model using the Unsloth library,
    optimized for multiclass classification tasks.

    Parameters
    ----------
    model_path : str
        Local path to the fine-tuned model (default: './models/DeepSeek-R1-Distill-Llama-8B-fine-tuned').

    max_seq_length : int
        Maximum input sequence length in tokens (default: 2048).

    dtype : torch.dtype or None
        Precision type for loading the model (e.g., torch.float16). If None, default is used.

    load_in_4bit : bool
        Whether to load the model in 4-bit quantized mode for efficient GPU memory usage (default: True).

    Returns
    -------
    model : transformers.PreTrainedModel
        The loaded LLM ready for inference.

    tokenizer : transformers.PreTrainedTokenizer
        The tokenizer associated with the model.
    """
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=model_path,
        max_seq_length=max_seq_length,
        dtype=dtype,
        load_in_4bit=load_in_4bit,
    )
    FastLanguageModel.for_inference(model)
    return model, tokenizer
