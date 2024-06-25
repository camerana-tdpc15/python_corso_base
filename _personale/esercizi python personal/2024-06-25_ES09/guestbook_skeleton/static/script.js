// Quando il DOM è pronto, legge e mostra i messaggi (completa tu il codice)
// Questo serve perchè altrimenti all'apertura la pagina non verrebbe
// popolata con i messaggi
document.addEventListener('DOMContentLoaded', () => {
    getMessages();
    

});

/*  Recupera i messaggi dal server con metodo GET e fetch API
    poi aggiorna la lista dei messaggi */
function getMessages() {
    fetch('/api/guestbook')
    .then(response => response.json())
        // Legge la risposta come JSON
        // ...
    
    .then(messages => {
        // Aggiorna la visualizzazione dei messaggi
        const messagesContainer = document.getElementById('messages-container');
        messagesContainer.innerHTML = ''; // Svuota il contenitore dei messaggi

        messages.forEach(message => {
            const messageElement = document.createElement('div');
            messageElement.textContent = message;
            messagesContainer.appendChild(messageElement);
        });
    })
        // Aggiorna la lista dei messaggi con i dati ricevuti
        // Inserisce i messaggi nella lista <ul> con id="message-list"
        // ...
    
    .catch(error => console.error('Errore durante la richiesta al server:', error
        // In caso di errori, li mostra nella console, altimenti gli
        // errori non sarebbero visibili in quanto fetch è una Promise,
        // che è asincrona e quindi non blocca il codice in caso di errore.
        // ...
    ));
}

/* Invia un messaggio al server con metodo POST e fetch API
poi in base alla risposta del server, aggiorna la lista dei messaggi
oppure mostra un messaggio di errore */
function sendMessage() {
    nomeInput = document.getElementById('nome'),
    messaggioInput = document.getElementById('messaggio').value,
    let data = {
        'nome': nameInput.value,
        'messaggio': messaggioInput
    };
    // Invia la richiesta al server
    fetch('/api/guestbook', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            getMessages();
            nomeInput.value = '';
            messaggioInput.value = '';
            // @DA FARE: Reset dei campi del form
            // ...
        } else if (result.error) {
            alert(result.error)
        }
    })
    .catch(error => console.error('Error:', error));
}