from typing import List, Dict
from utils.logging_utils import log

class ParseAgent:
    def parse_pdfs(self, files: List[str]) -> List[Dict]:
        parsed = []
        for f in files:
            log(f"Parsing (stub): {f}")
            parsed.append({
                "source": f,
                "chunks": [{"id": "KB-1", "text": "See sample_rules.json"}]
            })
        return parsed
