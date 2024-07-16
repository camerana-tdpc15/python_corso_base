// Aggiunge un listener per l'evento 'DOMContentLoaded' che carica le repliche una volta che il DOM è completamente caricato
document.addEventListener('DOMContentLoaded', () => {
    // Ottiene l'ID dell'evento dal dataset dell'elemento 'repliche-container'
    const eventoId = document.getElementById('repliche-container').dataset.eventoId;
    loadRepliche(eventoId);
});

// Funzione per caricare le repliche di un evento specifico
function loadRepliche(eventoId) {
    fetch(`/api/repliche/${eventoId}`)
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('repliche-container');
            // Aggiorna il contenuto del container con le informazioni dell'evento e le sue repliche
            container.innerHTML = `
                <h1 class="mb-4">Repliche di "${data.nome_evento}"</h1>
                <h2 class="mb-3">${data.locale}</h2>
                <p><strong>Luogo:</strong> ${data.luogo}</p>
                <div class="row">
                    ${data.repliche.map(replica => createReplicaCard(replica)).join('')}
                </div>
            `;
        })
        .catch(error => console.error('Error:', error));
}

// Funzione per creare una card HTML per ogni replica
function createReplicaCard(replica) {
    return `
        <div class="col-md-4 mb-3">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">${replica.data_ora}</h5>
                    
                    <p class="card-text">Posti disponibili: ${replica.posti_disponibili}</p>
                    ${replica.annullato 
                        ? '<p class="text-danger">Questa replica è stata annullata.</p>'
                        : `
                            <form onsubmit="prenota(event, ${replica.id})">
                                <div class="mb-3">
                                    <label for="quantita-${replica.id}" class="form-label">Quantità:</label>
                                    <input type="number" class="form-control" id="quantita-${replica.id}" name="quantita" value="1" min="1" max="${replica.posti_disponibili}">
                                </div>
                                <button type="submit" class="btn btn-primary">Prenota</button>
                            </form>
                        `
                    }
                </div>
            </div>
        </div>
    `;
}

// Funzione per gestire la prenotazione di una replica
function prenota(event, replicaId) {
    event.preventDefault();
    // Ottiene la quantità di posti prenotati dal campo di input
    const quantita = document.getElementById(`quantita-${replicaId}`).value;

    fetch('/api/prenotazioni', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            action: 'create',
            replica_id: replicaId,
            quantita: parseInt(quantita)
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
            // Ricarica le repliche per aggiornare i posti disponibili
            const eventoId = document.getElementById('repliche-container').dataset.eventoId;
            loadRepliche(eventoId);
        } else if (data.error) {
            alert(data.error);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('Si è verificato un errore durante la prenotazione.');
    });
}
