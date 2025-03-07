document.addEventListener("DOMContentLoaded", function () {
    const ctx = document.getElementById("btc-chart").getContext("2d");
    let btcChart;
    let labels = []; // Shared time labels for actual & predicted prices
    let actualPrices = []; // Live BTC prices (blue line)
    let predictedPrices = []; // Predicted BTC prices (red line)

    function fetchAndUpdateData() {
        Promise.all([
            fetch("/api/live").then((res) => res.json()),
            fetch("/api/predict").then((res) => res.json()),
        ])
        .then(([liveData, predictedData]) => {
            const currentTime = new Date();
            const nextMinuteTime = new Date(currentTime.getTime() + 60000); // 1 min ahead

            if (liveData.current_price) {
                document.getElementById("current-price").innerText = `Current BTC Price: $${liveData.current_price.toFixed(2)}`;
                
                // ✅ Ensure no duplicate timestamps
                if (!labels.includes(currentTime.toLocaleTimeString())) {
                    labels.push(currentTime.toLocaleTimeString()); // Blue line timestamps
                    actualPrices.push(liveData.current_price);
                    predictedPrices.push(null); // Keep prediction empty at actual timestamps
                }
            }

            if (predictedData.predicted_price) {
                document.getElementById("predicted-price").innerText = `Predicted BTC Price (Next Minute): $${predictedData.predicted_price.toFixed(2)}`;

                // ✅ Ensure predictions extend smoothly forward, not reset
                if (!labels.includes(nextMinuteTime.toLocaleTimeString())) {
                    labels.push(nextMinuteTime.toLocaleTimeString()); // Red line timestamps (1 min ahead)
                    actualPrices.push(null); // Keep actual price empty for predicted time
                    predictedPrices.push(predictedData.predicted_price);
                }
            }

            updateChart();
        })
        .catch((error) => console.error("Error fetching data:", error));
    }

    function updateChart() {
        if (labels.length > 20) {
            labels.shift(); // ✅ Keep last 20 points to maintain smooth graph updates
            actualPrices.shift();
            predictedPrices.shift();
        }

        if (btcChart) btcChart.destroy(); // ✅ Remove old chart before updating

        btcChart = new Chart(ctx, {
            type: "line",
            data: {
                labels: labels, // ✅ Keep a single continuous timeline
                datasets: [
                    {
                        label: "Live BTC Price",
                        data: actualPrices,
                        borderColor: "blue",
                        backgroundColor: "transparent",
                        borderWidth: 2,
                        pointStyle: "circle",
                        pointRadius: 4,
                        spanGaps: true,
                    },
                    {
                        label: "Predicted BTC Price (Next 1 min)",
                        data: predictedPrices,
                        borderColor: "red",
                        backgroundColor: "transparent",
                        borderWidth: 2,
                        borderDash: [5, 5], // Dashed line for prediction
                        pointStyle: "circle",
                        pointRadius: 4,
                        spanGaps: true,
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { display: true },
                    y: { display: true },
                },
            },
        });
    }

    fetchAndUpdateData();
    setInterval(fetchAndUpdateData, 60000); // ✅ Auto-refresh every 1 min
});
