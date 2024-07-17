// Ascolta l'evento 'DOMContentLoaded' per eseguire il codice quando il DOM è completamente caricato
document.addEventListener('DOMContentLoaded', function () {
    // Effettua una richiesta GET all'endpoint '/api/prenotazioni'
    fetch('/api/prenotazioni')
        .then(response => response.json())  // Converte la risposta in formato JSON
        .then(data => {
            // Seleziona il container dove inserire le prenotazioni
            const container = document.getElementById('prenotazioni-container');
            // Itera su ogni prenotazione ricevuta dal server
            data.forEach(prenotazione => {
                // Crea un nuovo elemento <div> per la card della prenotazione
                const card = document.createElement('div');
                card.className = 'col-md-4';  // Imposta la classe CSS per la card
                // Imposta il contenuto HTML della card
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
                // Aggiunge la card al container
                container.appendChild(card);
            });
        })
        // Gestisce eventuali errori durante la richiesta
        .catch(error => console.error('Error:', error));
});
