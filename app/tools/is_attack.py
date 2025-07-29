from langchain.tools import Tool
from models.binary_model import load_binary_model
from agents.is_attack import classify_log_entry

model, tokenizer = load_binary_model()

def classify_log_entry_tool(log_entry: str) -> str:
    return classify_log_entry(log_entry, model, tokenizer, device="cuda")

is_attack_tool = Tool(
    name="Detect Attack",
    func=classify_log_entry_tool,
    description="Detects if a log entry indicates an Attack or is Normal. Input: a log string."
)
