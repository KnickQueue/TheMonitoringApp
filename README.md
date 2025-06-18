# Service Health Monitoring App

This Flask application monitors the health or latency of various services and displays the results on a single dashboard. It polls each service once per minute and visualizes up to one hour of historical data using simple line graphs.

## Features

- Dashboard web page with real-time service updates and history graphs
- Background thread checks services every minute
- Two monitoring modes:
  - **Latency mode**: Pings each service and records response time in milliseconds
  - **Status mode**: Performs HTTP checks and records "Operational" or "Issues Detected"
- Current value (latency or status) shown in the dashboard
- Test mode for offline environments with randomly generated values

## Setup

1. Ensure Python 3.8+ and `pip` are installed on your system.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
