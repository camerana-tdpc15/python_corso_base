document.addEventListener('DOMContentLoaded', function () {
    fetch('/api/lotti')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('lotti-container');
            data.forEach(lotto => {
                fetch(`/api/prodotti/${lotto.prodotto}`)
                    .then(response => response.json())
                    .then(prodotto => {
                        const col = document.createElement('div');
                        col.className = 'col-md-4';
                        col.innerHTML = `
                            <div class="card mb-4">
                                <div class="card-body">
                                    <h5 class="card-title">Prodotto: ${prodotto.nome_prodotto}</h5>
                                    <p class="card-text">Data Consegna: ${lotto.data_consegna}</p>
                                    <p class="card-text">Quantità Disponibile: ${lotto.qta_disponibile}</p>
                                    <p class="card-text">Prezzo Unitario: ${lotto.prezzo_unitario}€</p>
                                    <a href="/prenotazione/${lotto.id}" class="btn btn-primary">Prenota</a>
                                </div>
                            </div>
                        `;
                        container.appendChild(col);
                    });
            });
        })
        .catch(error => console.error('Error fetching lotti:', error));
});
