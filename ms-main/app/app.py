from flask import Flask, request, jsonify, g
from pathlib import Path
from typing import Optional
import os
import logging
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from uuid import uuid4

app = Flask(__name__)

DATA_DIR = Path(os.getenv("DATA_DIR", "/etc/data")).resolve()
LOOKUP_URL = os.getenv("LOOKUP_URL", "http://lookup:5002/")
REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", "10"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

@app.before_request
def add_request_id():
    g.rid = request.headers.get("X-Request-ID", str(uuid4()))

def error(msg: str, file: Optional[str], code: int):
    return jsonify({"file": file, "error": msg, "request_id": g.get("rid")}), code

session = requests.Session()
retry = Retry(
    total=5, connect=3, read=3, backoff_factor=0.5,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=frozenset(["POST"]),   # if your requests version is old, use method_whitelist
)
adapter = HTTPAdapter(max_retries=retry)
session.mount("http://", adapter)
session.mount("https://", adapter)

def safe_under_data_dir(filename: str) -> Path:
    candidate = (DATA_DIR / filename).resolve()
    candidate.relative_to(DATA_DIR)
    return candidate

@app.get("/")
def root():
    return "You are in the calculate endpoint now"

@app.route("/calculate", methods=["POST"])
def calculate():
    if request.method == "GET":
        return "You are in the calculate endpoint now"

    if not request.is_json:
        return error("Invalid JSON input.", None, 400)

    data = request.get_json(silent=True) or {}
    file = data.get("file")
    if not isinstance(file, str) or not file.strip():
        return error("Invalid JSON input.", None, 400)

    try:
        target = safe_under_data_dir(file)
    except Exception:
        return error("File not found.", file, 404)

    if not target.exists():
        return error("File not found.", file, 404)

    try:
        resp = session.post(LOOKUP_URL, json=data,
                            headers={"X-Request-ID": g.rid},
                            timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
    except requests.exceptions.Timeout:
        return error("Upstream timeout.", file, 504)
    except requests.exceptions.ConnectionError:
        logger.exception("Connection error to lookup service")
        return error("Upstream connection error.", file, 502)
    except requests.RequestException as e:
        logger.exception("HTTP error from lookup service")
        code = getattr(e.response, "status_code", 502)
        return error(f"Upstream HTTP error: {code}", file, 502)

    try:
        return jsonify(resp.json()), 200
    except ValueError:
        return error("Invalid response from lookup service.", file, 502)

@app.get("/health")
def health():
    return jsonify(status="ok"), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "6000")),
            debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")
