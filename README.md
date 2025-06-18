# Service Health Monitoring App

This simple Flask application displays the health status of various services used by an MSP on a single dashboard page. It polls a set of status URLs and shows the current state, refreshing automatically on the page.

## Features

- Dashboard web page with live status updates and status history graphs
- Background thread that checks services every minute and stores the last hour of results
- Test mode that generates random status results without making network requests

## Setup

1. Ensure Python 3.8+ and `pip` are installed on your Ubuntu server.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   python app.py
   ```
4. Open `http://localhost:8000` in your browser to view the dashboard.

## Environment Variables

- `TEST_MODE=1` – Do not make real HTTP requests and instead use random statuses. Useful if the server does not have internet access or while developing.

## Adding Services

Edit the `SERVICES` dictionary in `app.py` to change or add service status URLs. Each entry should map the display name to a URL that returns HTTP `200` when the service is healthy.

## History Graphs

The dashboard shows a small graph for each service representing the last hour of
recorded status checks (one check per minute). Values above the line indicate
"Operational" status. These graphs refresh automatically when new data arrives.

## Disclaimer

The built-in checks are simplistic and may not reflect the real status of each provider. For production use, replace `check_service` with logic specific to each service's official status API.
