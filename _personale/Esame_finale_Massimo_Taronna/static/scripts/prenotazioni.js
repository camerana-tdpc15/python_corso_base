document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/prenotazioni')
        .then(response => response.json())
        .then(prenotazioni => {
            const container = document.getElementById('prenotazioni-container');
            prenotazioni.forEach(prenotazione => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${prenotazione.rel_replica.rel_evento.nome_evento}</td>
                    <td>${prenotazione.rel_replica.data_ora}</td>
                    <td><input type="number" value="${prenotazione.quantita}" min="1" id="quantita-${prenotazione.id}"></td>
                    <td>
                        <button class="btn btn-primary" onclick="modificaPrenotazione(${prenotazione.id})">Modifica numero posti</button>
                        <button class="btn btn-danger" onclick="cancellaPrenotazione(${prenotazione.id})">Cancella</button>
                    </td>
                `;
                container.appendChild(row);
            });
        });
});

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