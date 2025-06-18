import os
import random
import threading
import time
from datetime import datetime
from urllib.parse import urlparse
import subprocess
import requests
from flask import Flask, jsonify, render_template

app = Flask(__name__)

SERVICES = {
    "Microsoft 365": "https://status.office.com",
    "Microsoft Exchange": "https://status.office.com",
    "ProofPoint": "https://status.proofpoint.com",
    "SentinelOne": "https://status.sentinelone.com",
    "Duo Security": "https://status.duo.com",
    "Verizon Wireless (South Florida)": "https://www.verizon.com/support/status/",
    "AT&T Internet (South Florida)": "https://www.att.com/outages/",
    "Xfinity Internet (South Florida)": "https://www.xfinity.com/support/service-status",
    "ConnectWise Backup (Skykick)": "https://status.connectwise.com",
    "Ring Central": "https://status.ringcentral.com",
    "ConnectWise Control": "https://status.screenconnect.com",
    "Webroot": "https://status.webroot.com",
    "iDrive": "https://status.idrive.com",
}

# Choose monitoring mode: "latency" or "status"
MODE = os.getenv("MODE", "status").lower()

status_cache = {name: None for name in SERVICES}
status_history = {name: [] for name in SERVICES}  # keep last 60 samples

# Test mode disables real network calls
TEST_MODE = os.getenv("TEST_MODE", "0") == "1"

def measure_latency(url):
    """Ping the host for the given URL and return the latency in ms."""
    if TEST_MODE:
        return random.uniform(20, 100)
    host = urlparse(url).hostname
    if not host:
        return None
    try:
        result = subprocess.run([
            "ping", "-c", "1", "-W", "2", host
        ], capture_output=True, text=True)
        if result.returncode == 0:
            for line in result.stdout.splitlines():
                if "time=" in line:
                    ms = line.split("time=")[-1].split()[0]
                    return float(ms)
    except Exception:
        pass
    return None

def check_service(name, url):
    """Check the given service URL for availability."""
    if TEST_MODE:
        return random.choice(["Operational", "Issues Detected"])
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            return "Operational"
        return f"HTTP {resp.status_code}"
    except Exception as exc:
        return f"Error: {exc}"

def update_statuses():
    while True:
        timestamp = datetime.utcnow().isoformat() + "Z"
        for name, url in SERVICES.items():
            if MODE == "latency":
                value = measure_latency(url)
                status_cache[name] = value
            else:
                status = check_service(name, url)
                value = 1 if status == "Operational" else 0
                status_cache[name] = status
            history = status_history[name]
            history.append({"timestamp": timestamp, "value": value})
            if len(history) > 60:
                history.pop(0)
        time.sleep(60)

def start_background_thread():
    thread = threading.Thread(target=update_statuses, daemon=True)
    thread.start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/status")
def api_status():
    return jsonify({
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "services": status_cache,
    })

@app.route("/api/history")
def api_history():
    return jsonify(status_history)

if __name__ == "__main__":
    start_background_thread()
    app.run(host="0.0.0.0", port=8000)
