from utils.logging_utils import log

class ParseAgent:
    def parse_pdfs(self, files):
        # Placeholder for PyMuPDF parsing that would extract clauses.
        # We just return a stub telling that JSON rules exist.
        parsed = []
        for f in files:
            log(f"Parsing (stub): {f}")
            parsed.append({"source": f, "chunks": [{"id": "KB-1", "text": "See sample_rules.json"}]})
        return parsed
