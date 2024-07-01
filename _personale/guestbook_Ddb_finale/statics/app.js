    // Azioni da eseguire quando il DOM è pronto
    document.addEventListener('DOMContentLoaded', () => {
        // Legge e mostra i messaggi al caricamento della pagina
        loadMessages();
        // Aggiunge un event listener al pulsante di invio del messaggio
        document.getElementById('message-form').addEventListener('submit', sendMessage);
    });

    // Funzione per inviare un messaggio al guestbook
    async function sendMessage(event) {
        event.preventDefault();
        let messageTextarea = document.getElementById('message')
        const message = messageTextarea.value;
        const response = await fetch('/api/guestbook', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({messaggio: message})
        });
        const result = await response.json();
        if (result.success) {
            loadMessages();
            messageTextarea.value = '';
            // document.getElementById('message-form').reset();
        } else if (result.error){
            alert(result.error);
        } else {
            alert("Errore sconosciuto durante l'invio del messaggio.");
        }
    }

    // Funzione per leggere i messaggi dal guestbook
    async function loadMessages() {
        const response = await fetch('/api/guestbook');
        const messages = await response.json();
        const messagesList = document.getElementById('messages-list');
        messagesList.innerHTML = '';
        messages.forEach(message => {
            const li = document.createElement('li');
            li.textContent = `${message.nickname}: ${message.messaggio}`;
            messagesList.appendChild(li);
        });
    }