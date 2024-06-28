// Quando il DOM è pronto, legge e mostra i messaggi (completa tu il codice)
// Questo serve perchè altrimenti all'apertura la pagina non verrebbe
// popolata automaticamente con i messaggi.
document.addEventListener('DOMContentLoaded', () => {
    // Legge e mostra i messaggi nell'elenco
    getMessages();

    // Se non avessimo usato onclick="sendMessage()" nel bottone, avremmo
    // dovuto usare addEventListener per intercettare l'evento click sul bottone
    // e chiamare la funzione sendMessage:
    // document.getElementById('submit-btn').addEventListener('click', sendMessage);

});

/*  Funzione per recuperare i messaggi dal server con metodo GET e fetch API
    e poi aggiornare la lista dei messaggi.
    NOTA: Questa parte è come l'esercitazione sui cocktail che avete svolto
          nella parte di front-end.
    */
function getMessages() {
    fetch('/api/guestbook')  // Dato che non dobbiamo inviare dati, basta solo l'URL
    .then(
        // Legge la risposta come JSON
        // ...
    )
    .then(
        // Aggiorna la lista dei messaggi con i dati ricevuti
        // Inserisce i messaggi nella lista <ul> con id="message-list"
        // NOTA: usare i tag <li> per inserire i messaggi!
        // ...
    )
    .catch(error => console.error('Error:', error));
        // In caso di errori, li mostra nella console, altimenti gli
        // errori non sarebbero visibili in quanto fetch è una Promise,
        // che è asincrona e quindi non blocca il codice in caso di errore.
        
    
}

/* Invia un messaggio al server con metodo POST e fetch API
poi in base alla risposta del server, aggiorna la lista dei messaggi
oppure mostra un messaggio di errore */
function sendMessage() {
    let data = {
        'nome': document.getElementById('nome').value,
        'messaggio': document.getElementById('messaggio').value,
    };
    // Invia la richiesta al server
    fetch('/api/guestbook', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    })
    // Legge la risposta come JSON
    .then(response => response.json())
    // Aggiorna la lista dei messaggi con i dati ricevuti
    .then(result => {
        // Controlla se la risposta contiene la chiave 'success' o 'error'
        if (result.success) {  // è come se scrivessimo result['success']
            getMessages();
            // Resetta i campi del form
            let form = document.getElementById('msg-form');
            form.reset();
        } else if (result.error) {  // è come se scrivessimo result['error']
            alert(result.error);
        // Aggiungiamo anche un controllo per il caso in cui il server
        // ci invia una risposta che non contiene né la chiave 'success' né 'error'
        } else {
            alert('Errore sconosciuto!');
        }
    })
    .catch(error => console.error('Error:', error));
}