from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class LLMConfig:
    model_name: str
    base_url: str
    temperature: float
    max_tokens: int