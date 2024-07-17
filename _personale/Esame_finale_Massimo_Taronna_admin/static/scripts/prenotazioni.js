// Carica le prenotazioni quando il DOM è completamente caricato
document.addEventListener('DOMContentLoaded', function() {
    caricaPrenotazioni();
});

// Funzione per caricare le prenotazioni dell'utente
function caricaPrenotazioni() {
    fetch('/api/prenotazioni')
        .then(response => response.json())
        .then(prenotazioni => {
            const container = document.getElementById('prenotazioni-container');
            container.innerHTML = ''; // Pulisce il contenitore prima di aggiungere nuove righe
            prenotazioni.forEach(prenotazione => {
                aggiungiRigaPrenotazione(prenotazione, container);
            });
        });
}

// Funzione per aggiungere una riga di prenotazione alla tabella
function aggiungiRigaPrenotazione(prenotazione, container) {
    fetch(`/api/replica/${prenotazione.replica_id}/data_formattata`)
        .then(response => response.json())
        .then(data => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${prenotazione.rel_replica.rel_evento.nome_evento}</td>
                <td>${data.data_formattata}</td>
                <td><input type="number" value="${prenotazione.quantita}" min="1" id="quantita-${prenotazione.id}"></td>
                <td>
                    <button class="btn btn-primary" onclick="modificaPrenotazione(${prenotazione.id})">Modifica numero posti</button>
                    <button class="btn btn-danger" onclick="cancellaPrenotazione(${prenotazione.id})">Elimina</button>
                </td>
            `;
            container.appendChild(row);
        });
}

// Funzione per modificare una prenotazione
function modificaPrenotazione(prenotazioneId) {
    const quantita = document.getElementById(`quantita-${prenotazioneId}`).value;
    fetch(`/api/prenotazioni/${prenotazioneId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ quantita: quantita })
    }).then(response => {
        if (response.ok) {
            alert('Prenotazione modificata con successo!');
        } else {
            alert('Errore nella modifica della prenotazione.');
        }
    });
}

// Funzione per cancellare una prenotazione
function cancellaPrenotazione(prenotazioneId) {
    fetch(`/api/prenotazioni/${prenotazioneId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => {
        if (response.ok) {
            alert('Prenotazione cancellata con successo!');
            document.location.reload();
        } else {
            alert('Errore nella cancellazione della prenotazione.');
        }
    });
}