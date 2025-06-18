import os
import random
import threading
import time
from datetime import datetime

from flask import Flask, jsonify, render_template
import requests

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

status_cache = {name: "Unknown" for name in SERVICES}

# If TEST_MODE is set, we will not make real HTTP requests
TEST_MODE = os.getenv("TEST_MODE", "0") == "1"


def check_service(name, url):
    """Check the given service URL."""
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
        for name, url in SERVICES.items():
            status_cache[name] = check_service(name, url)
        time.sleep(60)  # update every minute


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


if __name__ == "__main__":
    start_background_thread()
    app.run(host="0.0.0.0", port=8000)
