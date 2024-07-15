// Esegue fetchPrenotazioni quando il DOM è completamente caricato
document.addEventListener('DOMContentLoaded', fetchPrenotazioni);

// Oggetto contenente gli endpoint API per le operazioni sulle prenotazioni
const API_ENDPOINTS = {
    GET_PRENOTAZIONI: '/api/prenotazioni',
    UPDATE_PRENOTAZIONE: '/api/prenotazione/modifica',
    DELETE_PRENOTAZIONE: '/api/prenotazione/elimina'
};

/**
 * Recupera le prenotazioni dal server e le renderizza nella pagina.
 * Gestisce anche gli errori in caso di problemi con la richiesta.
 */
function fetchPrenotazioni() {
    fetch(API_ENDPOINTS.GET_PRENOTAZIONI)
        .then(response => {
            if (!response.ok) throw new Error('Errore nel recupero delle prenotazioni');
            return response.json();
        })
        .then(data => renderPrenotazioni(data))
        .catch(error => {
            console.error('Errore nel recupero delle prenotazioni:', error);
            alert('Si è verificato un errore nel recupero delle prenotazioni. Riprova più tardi.');
        });
}

/**
 * Renderizza le prenotazioni nella pagina.
 * Se non ci sono prenotazioni, mostra un messaggio appropriato.
 * Calcola e visualizza anche il prezzo totale di tutte le prenotazioni.
 * @param {Array} prenotazioni - Array di oggetti prenotazione
 */
function renderPrenotazioni(prenotazioni) {
    const container = document.getElementById('prenotazioni-container');
    const noPrenotazioniMessage = document.getElementById('no-prenotazioni-message');
    container.innerHTML = ''; // Pulisce il contenitore prima di aggiungere nuove prenotazioni
    
    if (prenotazioni.length === 0) {
        noPrenotazioniMessage.style.display = 'block';
        return;
    }
    
    noPrenotazioniMessage.style.display = 'none';
    const totalPrice = prenotazioni.reduce((total, prenotazione) => {
        container.appendChild(createPrenotazioneCard(prenotazione));
        return total + prenotazione.qta * prenotazione.rel_lotto.prezzo_unitario;
    }, 0);

    document.getElementById('total-price').textContent = `Totale complessivo: ${totalPrice.toFixed(2)} €`;
}

/**
 * Crea una card HTML per una singola prenotazione.
 * @param {Object} prenotazione - Oggetto contenente i dettagli della prenotazione
 * @returns {HTMLElement} - Elemento div rappresentante la card della prenotazione
 */
function createPrenotazioneCard(prenotazione) {
    const { id, qta, rel_lotto } = prenotazione;
    const { rel_prodotto, data_consegna, prezzo_unitario } = rel_lotto;
    
    const card = document.createElement('div');
    card.className = 'card mb-3';
    card.id = `prenotazione-${id}`;

    card.innerHTML = `
        <div class="card-body">
            <h5 class="card-title">${rel_prodotto.nome_prodotto}</h5>
            <p class="card-text">
                Data Consegna: ${formatDate(data_consegna)}<br>
                Prezzo per Unità: ${prezzo_unitario} €<br>
                Quantità: <span id="quantity-${id}">${qta}</span><br>
                Totale parziale: ${(qta * prezzo_unitario).toFixed(2)} €
            </p>
            ${createButtonGroup(id, qta)}
        </div>
    `;

    return card;
}

/**
 * Crea il gruppo di pulsanti per modificare ed eliminare una prenotazione.
 * @param {number} id - ID della prenotazione
 * @param {number} currentQuantity - Quantità attuale della prenotazione
 * @returns {string} - HTML string per il gruppo di pulsanti
 */
function createButtonGroup(id, currentQuantity) {
    return `
        <div class="btn-group mt-2">
            <button class="btn btn-primary" onclick="showEditForm(${id}, ${currentQuantity})">Modifica</button>
            <button class="btn btn-danger" onclick="deletePrenotazione(${id})">Elimina</button>
        </div>
    `;
}

/**
 * Formatta una data in formato italiano (dd/mm/yyyy).
 * @param {string} dateString - Data in formato ISO
 * @returns {string} - Data formattata
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('it-IT', { day: '2-digit', month: '2-digit', year: 'numeric' });
}

/**
 * Mostra il form per modificare la quantità di una prenotazione.
 * @param {number} id - ID della prenotazione
 * @param {number} currentQuantity - Quantità attuale della prenotazione
 */
function showEditForm(id, currentQuantity) {
    const card = document.getElementById(`prenotazione-${id}`);
    const quantitySpan = card.querySelector(`#quantity-${id}`);
    const buttonGroup = card.querySelector('.btn-group');

    // Nasconde la quantità attuale e i pulsanti
    quantitySpan.style.display = 'none';
    buttonGroup.style.display = 'none';

    // Crea e aggiunge il form di modifica
    const editForm = document.createElement('div');
    editForm.innerHTML = `
        <input type="number" id="edit-quantity-${id}" value="${currentQuantity}" min="1" class="form-control mb-2">
        <button class="btn btn-success mr-2" onclick="updateQuantity(${id})">Salva</button>
        <button class="btn btn-secondary" onclick="cancelEdit(${id})">Annulla</button>
    `;

    card.querySelector('.card-body').appendChild(editForm);
}

/**
 * Annulla la modifica di una prenotazione, ripristinando la visualizzazione originale.
 * @param {number} id - ID della prenotazione
 */
function cancelEdit(id) {
    const card = document.getElementById(`prenotazione-${id}`);
    card.querySelector(`#quantity-${id}`).style.display = 'inline';
    card.querySelector('.btn-group').style.display = 'block';
    card.querySelector('div:last-child').remove(); // Rimuove il form di modifica
}

/**
 * Aggiorna la quantità di una prenotazione sul server.
 * @param {number} id - ID della prenotazione
 */
function updateQuantity(id) {
    const newQuantity = parseInt(document.getElementById(`edit-quantity-${id}`).value, 10);
    if (isNaN(newQuantity) || newQuantity <= 0) {
        alert("Per favore, inserisci un numero valido maggiore di zero.");
        return;
    }

    fetch(API_ENDPOINTS.UPDATE_PRENOTAZIONE, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id, quantita: newQuantity })
    })
    .then(response => {
        if (!response.ok) throw new Error('Errore nell\'aggiornamento della quantità');
        return response.json();
    })
    .then(data => {
        alert(data.message);
        fetchPrenotazioni(); // Aggiorna la lista delle prenotazioni
    })
    .catch(error => {
        console.error('Errore nell\'aggiornamento della quantità:', error);
        alert('Si è verificato un errore nell\'aggiornamento della quantità. Riprova più tardi.');
    });
}

/**
 * Elimina una prenotazione dal server.
 * Chiede conferma all'utente prima di procedere.
 * @param {number} id - ID della prenotazione da eliminare
 */
function deletePrenotazione(id) {
    if (!confirm('Sei sicuro di voler eliminare questa prenotazione?')) return;

    fetch(API_ENDPOINTS.DELETE_PRENOTAZIONE, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id })
    })
    .then(response => {
        if (!response.ok) throw new Error('Errore nell\'eliminazione della prenotazione');
        return response.json();
    })
    .then(data => {
        alert(data.message);
        fetchPrenotazioni(); // Aggiorna la lista delle prenotazioni
    })
    .catch(error => {
        console.error('Errore nell\'eliminazione della prenotazione:', error);
        alert('Si è verificato un errore nell\'eliminazione della prenotazione. Riprova più tardi.');
    });
}