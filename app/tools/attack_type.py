from langchain.tools import Tool
from models.multiclass_model import load_multiclass_model
from agents.attack_type import classify_attack

model, tokenizer = load_multiclass_model()

def classify_attack_tool(log_entry: str) -> str:
    return classify_attack(log_entry, model, tokenizer, device="cuda")

attack_type_tool = Tool(
    name="Classify Attack Type",
    func=classify_attack_tool,
    description=(
        "Classifies the specific type of cyberattack in a network log. "
        "DO NOT use this tool unless the user has explicitly requested attack type classification. "
        "This tool assumes the log has already been confirmed as an attack. "    )
)
