async function fetchPredictions() {
    const response = await fetch('/predict');
    const data = await response.json();

    // Extract timestamps and predictions
    const timestamps = data.map(item => new Date(item.timestamp * 1000)); // Convert Unix timestamp to JS date
    const predictedPrices = data.map(item => item.predicted);

    // Shift predictions ahead by adding future timestamps
    const futureTimestamps = timestamps.map(t => new Date(t.getTime() + 5 * 60 * 1000)); // Add 5 minutes to each

    updateChart(timestamps, futureTimestamps, predictedPrices);
}

function updateChart(actualTimestamps, futureTimestamps, predictedPrices) {
    const ctx = document.getElementById('priceChart').getContext('2d');

    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: actualTimestamps.concat(futureTimestamps), // Combine timestamps
            datasets: [
                {
                    label: 'Actual Price',
                    data: [], // Will be filled later
                    borderColor: 'blue',
                    borderWidth: 2,
                    fill: false
                },
                {
                    label: 'Predicted Price',
                    data: predictedPrices,
                    borderColor: 'red',
                    borderWidth: 2,
                    fill: false,
                    pointRadius: 0, // Hide points for smoothness
                    borderDash: [5, 5] // Make prediction line dashed
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                x: { type: 'time', time: { unit: 'minute' } },
                y: { beginAtZero: false }
            }
        }
    });

    // Fetch actual prices separately
    fetchActualPrices(chart);
}

async function fetchActualPrices(chart) {
    const response = await fetch('/actual'); // Assuming you have an API for actual prices
    const data = await response.json();

    const actualPrices = data.map(item => item.price);
    chart.data.datasets[0].data = actualPrices;
    chart.update();
}

// Fetch predictions and update chart every minute
fetchPredictions();
setInterval(fetchPredictions, 60000);
