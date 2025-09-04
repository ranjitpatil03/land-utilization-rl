from utils.logging_utils import log

class FetchAgent:
    def fetch_docs(self, urls):
        # Placeholder: In real run, download PDFs with requests
        for u in urls:
            log(f"Would download: {u}")
        return ["rules_kb/sample_rules.json"]
