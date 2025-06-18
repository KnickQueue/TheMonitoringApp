import os
import random
import threading
import time
from datetime import datetime

from flask import Flask, jsonify, render_template
import subprocess
from urllib.parse import urlparse

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

status_cache = {name: None for name in SERVICES}  # last latency ms
status_history = {name: [] for name in SERVICES}  # keep last 60 latency samples

# If TEST_MODE is set, we will not run real ping commands
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
            "ping",
            "-c",
            "1",
            "-W",
            "2",
            host,
        ], capture_output=True, text=True)
        if result.returncode == 0:
            for line in result.stdout.splitlines():
                if "time=" in line:
                    ms = line.split("time=")[-1].split()[0]
                    return float(ms)
        return None
    except Exception:
        return None


def update_statuses():
    while True:
        timestamp = datetime.utcnow().isoformat() + "Z"
        for name, url in SERVICES.items():
            latency = measure_latency(url)
            status_cache[name] = latency
            value = latency
            history = status_history[name]
            history.append({"timestamp": timestamp, "value": value})
            if len(history) > 60:
                history.pop(0)
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


@app.route("/api/history")
def api_history():
    return jsonify(status_history)


if __name__ == "__main__":
    start_background_thread()
    app.run(host="0.0.0.0", port=8000)
