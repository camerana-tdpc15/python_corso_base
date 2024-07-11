document.addEventListener('DOMContentLoaded', function() {
    fetchPrenotazioni();
});

function fetchPrenotazioni() {
    fetch("/api/prenotazioni")
        .then(response => response.json())
        .then(data => {
            console.log('Fetched data:', data);
            const container = document.getElementById('prenotazioni-container');
            container.innerHTML = ''; // Clear existing content
            let totalPrice = 0;

            if (data.error) {
                alert(data.error);
                return;
            }
            if (data.length === 0) {
                document.getElementById('no-prenotazioni-message').style.display = 'block';
                return;
            }
            data.forEach(prenotazione => {
                const card = createPrenotazioneCard(prenotazione);
                container.appendChild(card);

                const prezzoTotale = prenotazione.qta * prenotazione.rel_lotto.prezzo_unitario;
                totalPrice += prezzoTotale;
            });

            document.getElementById('total-price').textContent = `Totale complessivo: ${totalPrice.toFixed(2)} €`;
        })
        .catch(error => {
            console.error('Error fetching prenotazioni:', error);
        });
}

function createPrenotazioneCard(prenotazione) {
    const card = document.createElement('div');
    card.className = 'card mb-3';
    card.id = `prenotazione-${prenotazione.id}`;

    const cardBody = document.createElement('div');
    cardBody.className = 'card-body';

    const cardTitle = document.createElement('h5');
    cardTitle.className = 'card-title';
    cardTitle.textContent = prenotazione.rel_lotto.rel_prodotto.nome_prodotto;

    const cardText = document.createElement('p');
    cardText.className = 'card-text';
    const prezzoTotale = (prenotazione.qta * prenotazione.rel_lotto.prezzo_unitario).toFixed(2);

    const dataConsegna = new Date(prenotazione.rel_lotto.data_consegna);
    const formattedDate = `${String(dataConsegna.getDate()).padStart(2, '0')}/${String(dataConsegna.getMonth() + 1).padStart(2, '0')}/${dataConsegna.getFullYear()}`;

    cardText.innerHTML = `
        Data Consegna: ${formattedDate}<br>
        Prezzo per Unità: ${prenotazione.rel_lotto.prezzo_unitario} €<br>
        Quantità: <span id="quantity-${prenotazione.id}">${prenotazione.qta}</span><br>
        Totale parziale: ${prezzoTotale} €
    `;

    const buttonGroup = document.createElement('div');
    buttonGroup.className = 'btn-group mt-2';

    const editButton = document.createElement('button');
    editButton.textContent = 'Modifica';
    editButton.className = 'btn btn-primary';
    editButton.addEventListener('click', () => showEditForm(prenotazione.id, prenotazione.qta));

    const deleteButton = document.createElement('button');
    deleteButton.textContent = 'Elimina';
    deleteButton.className = 'btn btn-danger';
    deleteButton.addEventListener('click', () => deletePrenotazione(prenotazione.id));

    buttonGroup.appendChild(editButton);
    buttonGroup.appendChild(deleteButton);

    cardBody.appendChild(cardTitle);
    cardBody.appendChild(cardText);
    cardBody.appendChild(buttonGroup);
    card.appendChild(cardBody);

    return card;
}

function showEditForm(id, currentQuantity) {
    const card = document.getElementById(`prenotazione-${id}`);
    const quantitySpan = card.querySelector(`#quantity-${id}`);
    const buttonGroup = card.querySelector('.btn-group');

    // Hide the current quantity and buttons
    quantitySpan.style.display = 'none';
    buttonGroup.style.display = 'none';

    // Create and show the edit form
    const editForm = document.createElement('div');
    editForm.innerHTML = `
        <input type="number" id="edit-quantity-${id}" value="${currentQuantity}" min="1" class="form-control mb-2">
        <button class="btn btn-success mr-2" onclick="updateQuantity(${id})">Salva</button>
        <button class="btn btn-secondary" onclick="cancelEdit(${id})">Annulla</button>
    `;

    card.querySelector('.card-body').appendChild(editForm);
}

function cancelEdit(id) {
    const card = document.getElementById(`prenotazione-${id}`);
    const quantitySpan = card.querySelector(`#quantity-${id}`);
    const buttonGroup = card.querySelector('.btn-group');
    const editForm = card.querySelector('div:last-child');

    // Show the current quantity and buttons
    quantitySpan.style.display = 'inline';
    buttonGroup.style.display = 'block';

    // Remove the edit form
    editForm.remove();
}

function updateQuantity(id) {
    const newQuantity = parseInt(document.getElementById(`edit-quantity-${id}`).value, 10);
    if (isNaN(newQuantity) || newQuantity <= 0) {
        alert("Per favore, inserisci un numero valido maggiore di zero.");
        return;
    }
    fetch('/api/prenotazione/modifica', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ id: id, quantita: newQuantity }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            alert(data.message);
            fetchPrenotazioni(); // Refresh the list
        }
    })
    .catch(error => {
        console.error('Error updating quantity:', error);
    });
}

function deletePrenotazione(id) {
    if (confirm('Sei sicuro di voler eliminare questa prenotazione?')) {
        fetch('/api/prenotazione/elimina', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ id: id }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                alert(data.message);
                fetchPrenotazioni(); // Refresh the list
            }
        })
        .catch(error => {
            console.error('Error deleting prenotazione:', error);
        });
    }
}