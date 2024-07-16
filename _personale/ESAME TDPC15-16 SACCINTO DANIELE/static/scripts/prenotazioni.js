document.addEventListener('DOMContentLoaded', function () {
    fetch('/api/prenotazioni')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('prenotazioni-container');
            data.forEach(prenotazione => {
                const card = document.createElement('div');
                card.className = 'col-md-4';
                card.innerHTML = `
                    <div class="card mb-4 shadow-sm">
                        <div class="card-body">
                            <h5 class="card-title">${prenotazione.rel_replica.rel_eventi.nome_evento}</h5>
                            <p class="card-text">Data: ${prenotazione.rel_replica.get_date}</p>
                            <p class="card-text">Quantità: ${prenotazione.quantita}</p>
                            <form action="/prenotazione/${prenotazione.id}" method="POST">
                                <div class="form-group">
                                    <input type="number" name="quantita" class="form-control" placeholder="Nuova quantità">
                                </div>
                                <button type="submit" name="azione" value="aggiorna" class="btn btn-primary">Aggiorna</button>
                                <button type="submit" name="azione" value="elimina" class="btn btn-danger">Elimina</button>
                            </form>
                        </div>
                    </div>
                `;
                container.appendChild(card);
            });
        })
        .catch(error => console.error('Error:', error));
});
