# Service Health Monitoring App

This Flask application pings a collection of services and displays their latency on a single dashboard of graphs. Each service is checked once per minute and the last hour of results is shown.

## Features

- Dashboard web page with a graph for each service
- Background thread that pings services every minute and stores the last hour of latency values
- Test mode that generates random latency values without making network requests
- `TEST_MODE=1` – Do not run real ping commands and instead use random latency values. Useful if the server does not have internet access or while developing.
Edit the `SERVICES` dictionary in `app.py` to change or add service URLs. The hostname of each URL is pinged to measure response time.
ping results (one check per minute). Latency is shown in milliseconds and the
graphs update automatically.
The built-in ping checks are simplistic and may not reflect the real status of each provider. For production use, replace `measure_latency` with logic specific to each service's official status API or performance metrics.

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

968ucl-codex/create-real-time-service-health-monitoring-app
## History Graphs

The dashboard shows a small graph for each service representing the last hour of
recorded status checks (one check per minute). Values above the line indicate
"Operational" status. These graphs refresh automatically when new data arrives.

=======
main
## Disclaimer

The built-in checks are simplistic and may not reflect the real status of each provider. For production use, replace `check_service` with logic specific to each service's official status API.
