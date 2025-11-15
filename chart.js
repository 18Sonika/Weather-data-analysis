async function loadData() {
  const city = document.getElementById("city").value;
  const res = await fetch(`/data/${city}`);
  const data = await res.json();

  const ctx = document.getElementById("chart").getContext("2d");
  new Chart(ctx, {
    type: "line",
    data: {
      labels: data.dates,
      datasets: [
        { label: "Avg Temp (°C)", data: data.avg_temp, borderColor: "red", fill: false },
        { label: "Precipitation (mm)", data: data.precip, borderColor: "blue", fill: false },
        { label: "Wind Speed (km/h)", data: data.wind, borderColor: "green", fill: false }
      ]
    },
    options: {
      responsive: true,
      plugins: { legend: { position: "top" } },
      scales: { x: { display: true }, y: { display: true } }
    }
  });
}

window.onload = loadData;
