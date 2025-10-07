import json
from pathlib import Path
from utils.logging_utils import log

class InputAgent:
    def load_case(self, path: str) -> dict:
        file_path = Path(path)
        log(f"InputAgent: Loading case from {file_path}")

        if not file_path.exists():
            raise FileNotFoundError(f"Input file not found: {file_path}")

        try:
            with file_path.open("r", encoding="utf-8") as f:
                case = json.load(f)
            log(f"InputAgent: Successfully loaded case with keys: {list(case.keys())}")
            return case
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON from {file_path}: {e}")
