const charts = {};

function statusClass(status) {
    return status === 'Operational' ? 'text-success' : 'text-danger';
}

function slug(name) {
    return name.replace(/\s+/g, '-').toLowerCase();
}

async function fetchData() {
    try {
        const [statusResp, historyResp] = await Promise.all([
            axios.get('/api/status'),
            axios.get('/api/history')
        ]);
        updateTable(statusResp.data.services);
        updateCharts(historyResp.data);
    } catch (err) {
        console.error('Failed to fetch data:', err);
    }
}

function updateTable(services) {
    const tbody = document.querySelector('#status-table tbody');
    tbody.innerHTML = '';
    for (const [name, status] of Object.entries(services)) {
        const row = document.createElement('tr');
        const nameCell = document.createElement('td');
        nameCell.textContent = name;
        const statusCell = document.createElement('td');
        statusCell.textContent = status;
        statusCell.classList.add(statusClass(status));
        row.appendChild(nameCell);
        row.appendChild(statusCell);
        tbody.appendChild(row);
    }
}

function ensureChartContainer(name) {
    const chartsDiv = document.getElementById('charts');
    const id = slug(name);
    let wrapper = document.getElementById('chart-' + id);
    if (!wrapper) {
        wrapper = document.createElement('div');
        wrapper.className = 'col-md-4';
        wrapper.id = 'chart-' + id;

        const card = document.createElement('div');
        card.className = 'card';

        const header = document.createElement('div');
        header.className = 'card-header';
        header.textContent = name;

        const body = document.createElement('div');
        body.className = 'card-body';

        const canvas = document.createElement('canvas');
        canvas.id = 'canvas-' + id;

        body.appendChild(canvas);
        card.appendChild(header);
        card.appendChild(body);
        wrapper.appendChild(card);
        chartsDiv.appendChild(wrapper);
    }
}

function updateCharts(historyData) {
    for (const [name, points] of Object.entries(historyData)) {
        ensureChartContainer(name);
        const id = slug(name);
        const labels = points.map(p => new Date(p.timestamp).toLocaleTimeString());
        const data = points.map(p => p.value);

        let chart = charts[id];
        if (!chart) {
            const ctx = document.getElementById('canvas-' + id).getContext('2d');
            chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        data: data,
                        borderColor: '#0d6efd',
                        fill: false,
                        tension: 0.3,
                        pointRadius: 0
                    }]
                },
                options: {
                    animation: false,
                    responsive: true,
                    scales: {
                        y: { min: 0, max: 1, ticks: { stepSize: 1 } }
                    },
                    plugins: { legend: { display: false } }
                }
            });
            charts[id] = chart;
        } else {
            chart.data.labels = labels;
            chart.data.datasets[0].data = data;
            chart.update();
        }
    }
}

fetchData();
setInterval(fetchData, 30000); // refresh every 30 seconds
