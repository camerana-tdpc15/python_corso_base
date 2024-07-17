// Aggiunge un listener per l'evento 'DOMContentLoaded' che carica le prenotazioni una volta che il DOM è completamente caricato
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
                container.innerHTML = '<H4>Non hai ancora effettuato prenotazioni.</H4>';
            } else {
                // Se ci sono prenotazioni, crea una tabella per visualizzarle
                console.log(prenotazioni);
                for (evento of prenotazioni) {
                   
        


                    container.innerHTML += `
                        <div class="col-lg-4 my-2">
                            <div class="card h-100 rounded-4 shadow">
                                <div id="bg-gas-primary" class="card-header">
                                    <h4 class="card-title">${evento.evento}</h4>
                                    <p class="text-end"><small>(codice: ${evento.id})</small><p>
                                </div>
                                <div class="card-body d-flex flex-column">
                                    <p>Evento: <b>${evento.evento}</b></p>
                                    <p>Locale: <b>${evento.locale}</b></p>
                                    <p>Luogo: <b>${evento.luogo}</b></p>
                                    <p>Data: <b>${evento.data}</b>&nbsp;&nbsp;&nbsp;&nbsp;Ora: <b>${evento.ora}</b></p>
                                    <p>Q.tà Disp: <b><input type="number" min="1" value="${evento.quantita}" id="quantita-${evento.id}" ${evento.annullato ? 'disabled' : ''}></b></p>
                                    <p>Stato: <b>${evento.annullato ? '<span class="text-danger">Annullato</span>' : '<span class="text-success">Confermato</span>'}</b></p>
                                    <p>Azione: <b>${evento.annullato ? '' : `
                                    <button onclick="modificaPrenotazione(${evento.id})" class="btn btn-sm btn-primary">Modifica</button>
                                    <button onclick="cancellaPrenotazione(${evento.id})" class="btn btn-sm btn-danger">Cancella</button>
                                `}</b></p>
                                   
        
                                </div>
                            </div>
                        <div>
                    `;   
                }

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
            window.location.href = "/prenotazioni";
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
                window.location.href = "/prenotazioni";
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
