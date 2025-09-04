import json
from utils.logging_utils import log

class InputAgent:
    def load_case(self, path: str) -> dict:
        log(f"Loading case: {path}")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
