def classify_log_entry(log_entry: str, model, tokenizer, device: str = "cuda") -> str:
    """
    Classifies a single network log entry as either 'Attack' or 'Normal' using few-shot prompting
    with a large language model.

    This function builds a prompt with embedded examples, sends it to the model, and extracts
    the predicted label from the generated output.

    Args:
        log_entry (str): A structured log entry to be classified.
        model: A preloaded causal language model (e.g., LLaMA, DeepSeek).
        tokenizer: The tokenizer associated with the given model.
        device (str): The device to run inference on ('cuda' or 'cpu').

    Returns:
        str: The full string response from the model
    """
    few_shot_examples = """
    ### Examples:
    Log Entry:
    - The length of the DNS query is: 0
    - The MQTT protocol name used is: 0
    - The MQTT message type is: 0
    - The MQTT topic is: 0
    - The MQTT connection acknowledgment flags are: 0
    - TCP options set in the packet are: 0
    - TCP destination port is: 1883.0
    Response: Normal

    Log Entry:
    - The length of the DNS query is: 0
    - The MQTT protocol name used is: 0
    - The MQTT message type is: 0
    - The MQTT topic is: 0
    - The MQTT connection acknowledgment flags are: 0
    - TCP options set in the packet are: 020405b40402080ae78762e20000000001030307
    - TCP destination port is: 80.0
    Response: Attack

    Log Entry:
    - The length of the DNS query is: 0
    - The MQTT protocol name used is: MQTT
    - The MQTT message type is: 0
    - The MQTT topic is: 0
    - The MQTT connection acknowledgment flags are: 0
    - TCP options set in the packet are: 0
    - TCP destination port is: 61388.0
    Response: Normal

    Log Entry:
    - The length of the DNS query is: 0.0
    - The MQTT protocol name used is: 0.0
    - The MQTT message type is: 0.0
    - The MQTT topic is: 0.0
    - The MQTT connection acknowledgment flags are: 0.0
    - TCP options set in the packet are: 0.0
    - TCP destination port is: 5972.0
    Response: Attack
    """

    # Final prompt with few-shot and the new log
    prompt = f"""You are an AI security classifier.

    Your task is to classify whether the following log indicates an **Attack** or is **Normal**.

    Only respond with one word: Attack or Normal. No explanation.

    {few_shot_examples}

    ### Log Entry:
    {log_entry}
    Response:"""    

    inputs = tokenizer([prompt], return_tensors="pt").to(device)
    outputs = model.generate(
        input_ids=inputs.input_ids,
        attention_mask=inputs.attention_mask,
        max_new_tokens=3, 
        use_cache=True,
    )
    response = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
   
    return response
