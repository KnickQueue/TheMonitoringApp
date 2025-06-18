# Service Health Monitoring App

This Flask application monitors the health or latency of various services and displays the results on a single dashboard. It polls each service once per minute and visualizes up to one hour of historical data with simple line graphs.

## Features

- Dashboard web page with live service updates and history graphs
- Background thread checks services every minute
- Two modes:
  - **Latency mode**: Pings each service and records response time in milliseconds
  - **Status mode**: Performs HTTP checks and records operational status
- Test mode that generates random results without making real network requests

## Setup

1. Ensure Python 3.8+ and `pip` are installed on your system.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
