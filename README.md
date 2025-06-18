# Service Health Monitoring App

This Flask application monitors the health of various services and displays their current status and history on a single dashboard. It polls service status pages once per minute and visualizes up to one hour of historical data with simple line graphs.

## Features

- Dashboard web page with live status updates and status history graphs
- Background thread that checks services every minute and stores the last hour of results
- Test mode that generates random status results without making network requests

## Setup

1. Ensure Python 3.8+ and `pip` are installed on your system.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
