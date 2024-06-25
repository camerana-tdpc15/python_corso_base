// Quando il DOM è pronto, legge e mostra i messaggi
// Questo serve perché altrimenti all'apertura la pagina non verrebbe
// popolata con i messaggi
document.addEventListener('DOMContentLoaded', () => {
    getMessages();
});

/* Recupera i messaggi dal server con metodo GET e fetch API
   poi aggiorna la lista dei messaggi */
function getMessages() {
    fetch('/api/guestbook')
        .then(response => response.json())
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
        .catch(error => console.error('Errore durante la richiesta al server:', error));
}

function sendMessage() {
    const nomeInput = document.getElementById('nome');
    const messaggioInput = document.getElementById('messaggio');

    const nome = nomeInput.value;
    const messaggio = messaggioInput.value;

    // Invia la richiesta al server
    fetch('/api/guestbook', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            name: nome,
            messaggi: messaggio
        })
    })
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                getMessages(); // Aggiorna la lista dei messaggi dopo l'invio
                nomeInput.value = ''; // Resetta il campo nome
                messaggioInput.value = ''; // Resetta il campo messaggio
            } else if (result.error) {
                alert(result.error);
            }
        })
        .catch(error => console.error('Errore durante la richiesta al server:', error));
}
