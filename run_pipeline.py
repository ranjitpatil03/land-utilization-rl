from agents.orchestrator import Orchestrator
from utils.logging_utils import log
from pathlib import Path
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Service is running")

if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent

    cases = [
        BASE_DIR / "io" / "cases" / "mumbai_case.json",
        BASE_DIR / "io" / "cases" / "pune_case.json",
    ]

    orch = Orchestrator()
    for case in cases:
        log("=" * 60)
        orch.run_case(str(case))

    print("Pipeline done. Starting dummy HTTP server for Render free tier.")

    PORT = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", PORT), HealthHandler)
    server.serve_forever()
