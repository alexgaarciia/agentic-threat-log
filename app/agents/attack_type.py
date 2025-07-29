def classify_attack(log_entry: str, model, tokenizer, device: str = "cuda") -> str:
    """
    Classifies a network log entry into one of several specific cybersecurity attack categories
    using few-shot prompting with a causal language model.

    This function constructs a detailed prompt containing labeled examples of various attack types 
    (e.g., 'ddos_tcp', 'sql_injection', 'xss', etc.) and normal traffic. It appends the new log entry 
    and asks the model to think step by step before generating the predicted category.

    Args:
        log_entry (str): The raw log entry to classify, typically a sequence of protocol and TCP feature values.
        model: The language model (e.g., DeepSeek, LLaMA) used for inference, already loaded and ready.
        tokenizer: The tokenizer corresponding to the model.
        device (str): Device to perform inference on. Defaults to "cuda".

    Returns:
        str: The full string response from the model, including the reasoning and the predicted category.
    """
    question = f"""
    Below is an instruction that describes a task, paired with input that provides context. Write a response that completes the request. Think step by step before answering and end with the final category.

    ### Instruction:
    You are a cybersecurity LLM trained to analyze raw IoT network logs and classify them into one of the following categories:
    - SQL_Injection
    - Fingerprinting
    - Vulnerability_Scanner
    - Normal
    - DDoS_UDP
    - DDoS_ICMP
    - DDoS_HTTP
    - DDoS_TCP
    - Uploading
    - MITM
    - Backdoor
    - Password
    - Ransomware
    - XSS
    - Port_Scanning

    Only respond with the category name at the end. Think step by step before answering.

    ### Example 1:
    - The length of the DNS query is: 0.0
    - The MQTT protocol name used is: 0.0
    - The MQTT message type is: 0.0
    - The MQTT topic is: 0.0
    - The MQTT connection acknowledgment flags are: 0.0
    - TCP options set in the packet are: 0.0
    - TCP destination port is: 0.0
    <think>
    This log data is an attack!! The type of attack detected is Fingerprinting.
    </think>

    ### Example 2:
    - The length of the DNS query is: 0.0
    - The MQTT protocol name used is: 0.0
    - The MQTT message type is: 0.0
    - The MQTT topic is: 0.0
    - The MQTT connection acknowledgment flags are: 0.0
    - TCP options set in the packet are: 0.0
    - TCP destination port is: 0.0
    <think>
    This log data is an attack!! The type of attack detected is MITM.
    </think>

    ### Example 3:
    - The length of the DNS query is: 0.0
    - The MQTT protocol name used is: 0.0
    - The MQTT message type is: 0.0
    - The MQTT topic is: 0.0
    - The MQTT connection acknowledgment flags are: 0.0
    - TCP options set in the packet are: 0101080a9eade1d99b204ef3
    - TCP destination port is: 39536.0
    <think>
    This log data is an attack!! The type of attack detected is SQL_injection.
    </think>

    ### Example 4:
    - The length of the DNS query is: 0.0
    - The MQTT protocol name used is: 0.0
    - The MQTT message type is: 0.0
    - The MQTT topic is: 0.0
    - The MQTT connection acknowledgment flags are: 0.0
    - TCP options set in the packet are: 0.0
    - TCP destination port is: 0.0
    <think>
    This log data is an attack!! The type of attack detected is DDoS_ICMP.
    </think>

    ### Example 5:
    - The length of the DNS query is: 0.0
    - The MQTT protocol name used is: 0.0
    - The MQTT message type is: 0.0
    - The MQTT topic is: 0.0
    - The MQTT connection acknowledgment flags are: 0.0
    - TCP options set in the packet are: 0101080a0aa7faea1dd8584c
    - TCP destination port is: 80.0
    <think>
    This log data is an attack!! The type of attack detected is DDoS_HTTP.
    </think>

    ### Example 6:
    - The length of the DNS query is: 0
    - The MQTT protocol name used is: 0
    - The MQTT message type is: 0
    - The MQTT topic is: 0
    - The MQTT connection acknowledgment flags are: 0x00000000
    - TCP options set in the packet are: 0
    - TCP destination port is: 61189.0
    <think>
    This log data is normal traffic.
    </think>

    ### Example 7:
    - The length of the DNS query is: 0.0
    - The MQTT protocol name used is: 0.0
    - The MQTT message type is: 0.0
    - The MQTT topic is: 0.0
    - The MQTT connection acknowledgment flags are: 0.0
    - TCP options set in the packet are: 0.0
    - TCP destination port is: 20041.0
    <think>
    This log data is an attack!! The type of attack detected is DDoS_TCP.
    </think>

    ### Example 8:
    - The length of the DNS query is: 0.0
    - The MQTT protocol name used is: 0.0
    - The MQTT message type is: 0.0
    - The MQTT topic is: 0.0
    - The MQTT connection acknowledgment flags are: 0.0
    - TCP options set in the packet are: 0101080a4a07695740863e92
    - TCP destination port is: 60656.0
    <think>
    This log data is an attack!! The type of attack detected is Uploading.
    </think>

    ### Example 9:
    - The length of the DNS query is: 0.0
    - The MQTT protocol name used is: 0.0
    - The MQTT message type is: 0.0
    - The MQTT topic is: 0.0
    - The MQTT connection acknowledgment flags are: 0.0
    - TCP options set in the packet are: 0101080a3fc429fe49455658
    - TCP destination port is: 80.0
    <think>
    This log data is an attack!! The type of attack detected is Vulnerability_scanner.
    </think>

    ### Example 10:
    - The length of the DNS query is: 0.0
    - The MQTT protocol name used is: 0.0
    - The MQTT message type is: 0.0
    - The MQTT topic is: 0.0
    - The MQTT connection acknowledgment flags are: 0.0
    - TCP options set in the packet are: 0.0
    - TCP destination port is: 0.0
    <think>
    This log data is an attack!! The type of attack detected is DDoS_UDP.
    </think>

    ### Example 11:
    - The length of the DNS query is: 0.0
    - The MQTT protocol name used is: 0.0
    - The MQTT message type is: 0.0
    - The MQTT topic is: 0.0
    - The MQTT connection acknowledgment flags are: 0.0
    - TCP options set in the packet are: 0101080a3de26c442b785b80
    - TCP destination port is: 60210.0
    <think>
    This log data is an attack!! The type of attack detected is Backdoor.
    </think>

    ### Example 12:
    - The length of the DNS query is: 0.0
    - The MQTT protocol name used is: 0.0
    - The MQTT message type is: 0.0
    - The MQTT topic is: 0.0
    - The MQTT connection acknowledgment flags are: 0.0
    - TCP options set in the packet are: 0101080a7b0104a7e78c1342
    - TCP destination port is: 54832.0
    <think>
    This log data is an attack!! The type of attack detected is Password.
    </think>

    ### Example 13:
    - The length of the DNS query is: 0.0
    - The MQTT protocol name used is: 0.0
    - The MQTT message type is: 0.0
    - The MQTT topic is: 0.0
    - The MQTT connection acknowledgment flags are: 0.0
    - TCP options set in the packet are: 0101080a8e93b45ac5b69a25
    - TCP destination port is: 47924.0
    <think>
    This log data is an attack!! The type of attack detected is Ransomware.
    </think>

    ### Example 14:
    - The length of the DNS query is: 0.0
    - The MQTT protocol name used is: 0.0
    - The MQTT message type is: 0.0
    - The MQTT topic is: 0.0
    - The MQTT connection acknowledgment flags are: 0.0
    - TCP options set in the packet are: 0
    - TCP destination port is: 0.0
    <think>
    This log data is an attack!! The type of attack detected is XSS.
    </think>

    ### Example 15:
    - The length of the DNS query is: 0.0
    - The MQTT protocol name used is: 0.0
    - The MQTT message type is: 0.0
    - The MQTT topic is: 0.0
    - The MQTT connection acknowledgment flags are: 0.0
    - TCP options set in the packet are: 0.0
    - TCP destination port is: 80.0
    <think>
    This log data is an attack!! The type of attack detected is Port_Scanning.
    </think>

    ### New Input:
    {log_entry.strip()}

    <think>
    """ 

    # Tokenize and send to model
    inputs = tokenizer([question], return_tensors="pt")
    input_ids = inputs["input_ids"].to(model.device)
    attention_mask = inputs["attention_mask"].to(model.device)

    outputs = model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,
        max_new_tokens=100,
        use_cache=True,
    )
    response = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]

    return response
