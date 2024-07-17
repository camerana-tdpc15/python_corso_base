// Ascolta l'evento 'DOMContentLoaded' per eseguire il codice quando il DOM è completamente caricato
document.addEventListener('DOMContentLoaded', function () {
    // Effettua una richiesta GET all'endpoint '/api/eventi' con il parametro 'order=asc' per ottenere eventi ordinati in ordine crescente
    fetch('/api/eventi?order=asc')
        .then(response => response.json())  // Converte la risposta in formato JSON
        .then(data => {
            // Seleziona il container dove inserire gli eventi
            const container = document.getElementById('eventi-container');
            // Itera su ogni evento ricevuto dal server
            data.forEach(evento => {
                // Crea un nuovo elemento <div> per la card dell'evento
                const card = document.createElement('div');
                card.className = 'col-md-4';  // Imposta la classe CSS per la card

                // Verifica se l'evento è annullato
                const isAnnullato = evento.annullato;
                
                // Imposta il contenuto HTML della card
                card.innerHTML = `
                    <div class="card mb-4 shadow-sm">
                        <div class="card-body">
                            <h5 class="card-title">${evento.rel_eventi.nome_evento}</h5>
                            <p class="card-text">Data: ${evento.get_date}</p>
                            <p class="card-text">Disponibili: ${evento.get_qta_disponibile}</p>
                            <a href="/replica/${evento.id}" class="btn ${isAnnullato ? 'btn-danger' : 'btn-primary'}" ${isAnnullato ? 'disabled' : ''}>Prenota</a>
                        </div>
                    </div>
                `;
                // Aggiunge la card al container
                container.appendChild(card);
            });
        })
        // Gestisce eventuali errori durante la richiesta
        .catch(error => console.error('Errore:', error));
});
