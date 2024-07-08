document.addEventListener('DOMContentLoaded', () => {
  const contentDiv = document.getElementById('content');

  fetch('report.json')
    .then(response => response.json())
    .then(data => {
      contentDiv.innerHTML = `
        <h3>AI News</h3>
        <p>${data.ai_news}</p>
        <h3>Stock Market News</h3>
        <p>${data.stock_news}</p>
        <h3>Crypto News</h3>
        <p>${data.crypto_news}</p>
      `;
    })
    .catch(error => {
      contentDiv.innerHTML = `<p>Failed to load the report: ${error}</p>`;
    });
});
