const charts = {};

function slug(name) {
    return name.replace(/\s+/g, '-').toLowerCase();
}

async function fetchData() {
    try {
        const resp = await axios.get('/api/history');
        updateCharts(resp.data);
    } catch (err) {
        console.error('Failed to fetch data:', err);
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

        const numeric = data.filter(v => v !== null);
        const maxVal = numeric.length ? Math.max(...numeric) : 100;
                        y: {
                            beginAtZero: true,
                            suggestedMax: maxVal + 50
                        }
            chart.options.scales.y.suggestedMax = maxVal + 50;
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
