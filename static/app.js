async function fetchStatus() {
    try {
        const resp = await axios.get('/api/status');
        const tbody = document.querySelector('#status-table tbody');
        tbody.innerHTML = '';
        for (const [name, status] of Object.entries(resp.data.services)) {
            const row = document.createElement('tr');
            const nameCell = document.createElement('td');
            nameCell.textContent = name;
            const statusCell = document.createElement('td');
            statusCell.textContent = status;
            row.appendChild(nameCell);
            row.appendChild(statusCell);
            tbody.appendChild(row);
        }
    } catch (err) {
        console.error('Failed to fetch status:', err);
    }
}

fetchStatus();
setInterval(fetchStatus, 30000); // refresh every 30 seconds
