# Service Health Monitoring App

This Flask application pings a collection of services and displays their latency on a single dashboard of graphs. Each service is checked once per minute and the last hour of results is shown.

## Features

- Dashboard web page with a graph for each service
- Background thread that pings services every minute and stores the last hour of latency values
- Current latency displayed next to each graph's title
- Test mode that generates random latency values without making network requests

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

- `TEST_MODE=1` – Do not run real ping commands and instead use random latency values. Useful if the server does not have internet access or while developing.

## Adding Services

Edit the `SERVICES` dictionary in `app.py` to change or add service URLs. The hostname of each URL is pinged to measure response time.

## History Graphs

The dashboard shows a small graph for each service representing the last hour of
ping results (one check per minute). Latency is shown in milliseconds and the
graphs update automatically. The most recent latency value appears next to the
service name above each graph. For real data the server running the application
must be able to reach the target services with ICMP traffic. If the environment
does not allow external network access you will only see zeros. In that case
enable `TEST_MODE` to populate the graphs with random latency values for
demonstration purposes.

## Disclaimer

The built-in ping checks are simplistic and may not reflect the real status of each provider. For production use, replace `measure_latency` with logic specific to each service's official status API or performance metrics.
