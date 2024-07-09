document.addEventListener('DOMContentLoaded', function () {
    fetch('/api/prenotazioni')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('prenotazioni-container');
            data.forEach(prenotazione => {
                fetch(`/api/prodotti/${prenotazione.prodotto_id}`)
                    .then(response => response.json())
                    .then(prodotto => {
                        const col = document.createElement('div');
                        col.className = 'col-md-4';
                        col.innerHTML = `
                            <div class="card mb-4">
                                <div class="card-body">
                                    <h5 class="card-title">Prodotto: ${prodotto.nome_prodotto}</h5>
                                    <p class="card-text">Data Consegna: ${prenotazione.data_consegna}</p>
                                    <p class="card-text">Quantità: ${prenotazione.qta}</p>
                                    <p class="card-text">Prezzo Unitario: ${prenotazione.prezzo_unitario}€</p>
                                    <a href="/modifica-prenotazione/${prenotazione.id}" class="btn btn-primary">Modifica</a>
                                    <form action="/elimina-prenotazione/${prenotazione.id}" method="POST" style="display:inline;">
                                        <button type="submit" class="btn btn-danger">Elimina</button>
                                    </form>
                                </div>
                            </div>
                        `;
                        container.appendChild(col);
                    });
            });
        })
        .catch(error => console.error('Error fetching prenotazioni:', error));
});
