// Aggiunge un listener per l'evenuser_idto 'DOMContentLoaded' che carica le prenotazioni una volta che il DOM è completamente caricato
document.addEventListener('DOMContentLoaded', () => {
    loadPrenotazioni();
});

// Funzione per caricare le prenotazioni dall'API
function loadPrenotazioni() {
    fetch('/api/prenotazioni')
        .then(response => response.json())
        .then(prenotazioni => {
            // Ottiene il container delle prenotazioni
            const container = document.getElementById('prenotazioni-container');
            // Controlla se ci sono prenotazioni
            if (prenotazioni.length === 0) {
                // Se non ci sono prenotazioni, mostra un messaggio
                container.innerHTML = '<p>Non hai ancora effettuato prenotazioni.</p>';
            } else {
                // Se ci sono prenotazioni, crea una tabella per visualizzarle
                container.innerHTML = `
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Evento</th>
                                <th>Locale</th>
                                <th>Data e Ora</th>
                                <th>Quantità</th>
                                <th>Stato</th>
                                <th>Azioni</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${prenotazioni.map(p => `
                                <tr>
                                    <td>${p.evento}</td>
                                    <td>${p.locale}</td>
                                    <td>${p.data_ora}</td>
                                    <td>
                                        <input type="number" min="1" value="${p.quantita}" id="quantita-${p.id}" ${p.annullato ? 'disabled' : ''}>
                                    </td>
                                    <td>${p.annullato ? '<span class="text-danger">Annullato</span>' : '<span class="text-success">Confermato</span>'}</td>
                                    <td>
                                        ${p.annullato ? '' : `
                                            <button onclick="modificaPrenotazione(${p.id})" class="btn btn-sm btn-primary">Modifica</button>
                                            <button onclick="cancellaPrenotazione(${p.id})" class="btn btn-sm btn-danger">Cancella</button>
                                        `}
                                    </td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                `;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            // Mostra un messaggio di errore se il caricamento delle prenotazioni fallisce
            document.getElementById('prenotazioni-container').innerHTML = '<p>Si è verificato un errore nel caricamento delle prenotazioni.</p>';
        });
}

// Funzione per modificare una prenotazione
function modificaPrenotazione(prenotazioneId) {
    // Ottiene la nuova quantità dal campo di input
    const nuovaQuantita = document.getElementById(`quantita-${prenotazioneId}`).value;
    fetch('/api/prenotazioni', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            action: 'update',
            prenotazione_id: prenotazioneId,
            quantita: nuovaQuantita
        }),
    })
    .then(response => response.json())
    .then(data => {
        // Mostra un messaggio di successo o di errore
        if (data.message) {
            alert(data.message);
            // Ricarica le prenotazioni dopo la modifica
            loadPrenotazioni();
        } else if (data.error) {
            alert(data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        // Mostra un messaggio di errore se la modifica fallisce
        alert('Si è verificato un errore durante la modifica della prenotazione.');
    });
}

// Funzione per cancellare una prenotazione
function cancellaPrenotazione(prenotazioneId) {
    // Chiede conferma all'utente prima di cancellare la prenotazione
    if (confirm('Sei sicuro di voler cancellare questa prenotazione?')) {
        fetch('/api/prenotazioni', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                action: 'delete',
                prenotazione_id: prenotazioneId
            }),
        })
        .then(response => response.json())
        .then(data => {
            // Mostra un messaggio di successo o di errore
            if (data.message) {
                alert(data.message);
                // Ricarica le prenotazioni dopo la cancellazione
                loadPrenotazioni();
            } else if (data.error) {
                alert(data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            // Mostra un messaggio di errore se la cancellazione fallisce
            alert('Si è verificato un errore durante la cancellazione della prenotazione.');
        });
    }
}
