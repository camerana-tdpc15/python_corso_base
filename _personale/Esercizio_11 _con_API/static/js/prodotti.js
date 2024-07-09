document.addEventListener('DOMContentLoaded', function () {
    fetch('/api/prodotti')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('prodotti-container');
            data.forEach(prodotto => {
                const col = document.createElement('div');
                col.className = 'col-md-4';
                col.innerHTML = `
                    <div class="card mb-4">
                        <img src="/static/images/${prodotto.image_url}" class="card-img-top" alt="${prodotto.nome_prodotto}">
                        <div class="card-body">
                            <h5 class="card-title">${prodotto.nome_prodotto}</h5>
                            <p class="card-text">Produttore: ${prodotto.produttore_id}</p>
                        </div>
                    </div>
                `;
                container.appendChild(col);
            });
        })
        .catch(error => console.error('Error fetching prodotti:', error));
});
