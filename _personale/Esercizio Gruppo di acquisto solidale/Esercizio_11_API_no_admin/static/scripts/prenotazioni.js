// Aggiunge un listener all'evento 'DOMContentLoaded' per chiamare la funzione fetchPrenotazioni
document.addEventListener('DOMContentLoaded', fetchPrenotazioni);

// Funzione per recuperare le prenotazioni dall'API
function fetchPrenotazioni() {
    fetch("/api/prenotazioni")
        .then(response => response.json())
        .then(data => {
            // Se c'è un errore, mostra un avviso e termina
            if (data.error) {
                alert(data.error);
                return;
            }

            // Seleziona il container dove verranno aggiunte le prenotazioni
            const container = document.getElementById('prenotazioni-container');
            container.innerHTML = ''; // Cancella il contenuto esistente
            let totalPrice = 0;

            // Se non ci sono prenotazioni, mostra il messaggio appropriato e termina
            if (data.length === 0) {
                document.getElementById('no-prenotazioni-message').style.display = 'block';
                return;
            }

            // Per ogni prenotazione, crea una card e aggiungila al container
            data.forEach(prenotazione => {
                container.appendChild(createPrenotazioneCard(prenotazione));
                // Calcola il totale complessivo
                totalPrice += prenotazione.qta * prenotazione.rel_lotto.prezzo_unitario;
            });

            // Aggiorna il totale complessivo visualizzato
            document.getElementById('total-price').textContent = `Totale complessivo: ${totalPrice.toFixed(2)} €`;
        })
        .catch(error => console.error('Error fetching prenotazioni:', error)); // Gestione degli errori
}

// Funzione per creare una card per ciascuna prenotazione
function createPrenotazioneCard(prenotazione) {
    const card = document.createElement('div');
    card.className = 'card mb-3';
    card.id = `prenotazione-${prenotazione.id}`;

    const cardBody = document.createElement('div');
    cardBody.className = 'card-body';

    // HTML per il corpo della card
    cardBody.innerHTML = `
        <h5 class="card-title">${prenotazione.rel_lotto.rel_prodotto.nome_prodotto}</h5>
        <p class="card-text">
            Data Consegna: ${formatDate(prenotazione.rel_lotto.data_consegna)}<br>
            Prezzo per Unità: ${prenotazione.rel_lotto.prezzo_unitario} €<br>
            Quantità: <span id="quantity-${prenotazione.id}">${prenotazione.qta}</span><br>
            Totale parziale: ${(prenotazione.qta * prenotazione.rel_lotto.prezzo_unitario).toFixed(2)} €
        </p>
    `;

    // Aggiunge il gruppo di pulsanti (Modifica, Elimina) al corpo della card
    cardBody.appendChild(createButtonGroup(prenotazione.id, prenotazione.qta));
    card.appendChild(cardBody);

    return card;
}

// Funzione per creare il gruppo di pulsanti (Modifica, Elimina) per ciascuna prenotazione
function createButtonGroup(id, currentQuantity) {
    const buttonGroup = document.createElement('div');
    buttonGroup.className = 'btn-group mt-2';

    const editButton = document.createElement('button');
    editButton.textContent = 'Modifica';
    editButton.className = 'btn btn-primary';
    editButton.addEventListener('click', () => showEditForm(id, currentQuantity));

    const deleteButton = document.createElement('button');
    deleteButton.textContent = 'Elimina';
    deleteButton.className = 'btn btn-danger';
    deleteButton.addEventListener('click', () => deletePrenotazione(id));

    buttonGroup.appendChild(editButton);
    buttonGroup.appendChild(deleteButton);

    return buttonGroup;
}

// Funzione per formattare la data in formato DD/MM/YYYY
function formatDate(dateString) {
    const date = new Date(dateString);
    return `${String(date.getDate()).padStart(2, '0')}/${String(date.getMonth() + 1).padStart(2, '0')}/${date.getFullYear()}`;
}

// Funzione per mostrare il form di modifica per una prenotazione
function showEditForm(id, currentQuantity) {
    const card = document.getElementById(`prenotazione-${id}`);
    const quantitySpan = card.querySelector(`#quantity-${id}`);
    const buttonGroup = card.querySelector('.btn-group');

    // Nascondi la quantità corrente e i pulsanti
    quantitySpan.style.display = 'none';
    buttonGroup.style.display = 'none';

    // Crea il form di modifica
    const editForm = document.createElement('div');
    editForm.innerHTML = `
        <input type="number" id="edit-quantity-${id}" value="${currentQuantity}" min="1" class="form-control mb-2">
        <button class="btn btn-success mr-2" onclick="updateQuantity(${id})">Salva</button>
        <button class="btn btn-secondary" onclick="cancelEdit(${id})">Annulla</button>
    `;

    card.querySelector('.card-body').appendChild(editForm);
}

// Funzione per annullare la modifica di una prenotazione
function cancelEdit(id) {
    const card = document.getElementById(`prenotazione-${id}`);
    const quantitySpan = card.querySelector(`#quantity-${id}`);
    const buttonGroup = card.querySelector('.btn-group');
    const editForm = card.querySelector('div:last-child');

    // Mostra la quantità corrente e i pulsanti
    quantitySpan.style.display = 'inline';
    buttonGroup.style.display = 'block';
    // Rimuovi il form di modifica
    editForm.remove();
}

// Funzione per aggiornare la quantità di una prenotazione
function updateQuantity(id) {
    const newQuantity = parseInt(document.getElementById(`edit-quantity-${id}`).value, 10);
    if (isNaN(newQuantity) || newQuantity <= 0) {
        alert("Per favore, inserisci un numero valido maggiore di zero.");
        return;
    }

    fetch('/api/prenotazione/modifica', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id, quantita: newQuantity })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            alert(data.message);
            fetchPrenotazioni(); // Aggiorna la lista delle prenotazioni
        }
    })
    .catch(error => console.error('Errore agggiornando la quantità', error)); // Gestione degli errori
}

// Funzione per eliminare una prenotazione
function deletePrenotazione(id) {
    if (confirm('Sei sicuro di voler eliminare questa prenotazione?')) {
        fetch('/api/prenotazione/elimina', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                alert(data.message);
                fetchPrenotazioni(); // Aggiorna la lista delle prenotazioni
            }
        })
        .catch(error => console.error('Errore cancellando la prenotazione', error)); // Gestione degli errori
    }
}
