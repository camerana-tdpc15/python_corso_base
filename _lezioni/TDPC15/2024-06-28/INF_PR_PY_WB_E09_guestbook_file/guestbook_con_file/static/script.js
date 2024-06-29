// Quando il DOM è pronto, legge e mostra i messaggi.
// Questo serve perchè altrimenti all'apertura, la pagina non verrebbe
// popolata automaticamente con i messaggi.
// NOTA: DOMContentLoaded è l'evento che viene innescato quando la pagina
//       completamente caricata (il DOM è l'ambiente di esecuzione
//       in cui c'è tutto il contenuto, html, js, css...)

function avviaApp() {
    // Legge e mostra i messaggi nell'elenco
    getMessages();

    // Se non avessimo usato onclick="sendMessage()" nel <button>, avremmo
    // dovuto usare addEventListener per intercettare l'evento click sul bottone
    // e chiamare la funzione sendMessage:
    // document.getElementById('submit-btn').addEventListener('click', sendMessage);
}

document.addEventListener('DOMContentLoaded', avviaApp);

/*  Funzione per recuperare i messaggi dal server con metodo GET e fetch API
    e poi aggiornare la lista dei messaggi.
    NOTA: Questa parte è come l'esercitazione sui cocktail che avete svolto
          nella parte di front-end.
    */
function getMessages() {
    // Invia la richiesta GET al server
    // NOTA: Dato che non dobbiamo inviare dati, basta solo l'URL
    fetch('/api/guestbook')
    // Legge la risposta come JSON
    .then(response => response.json())
    .then(messages => {
        // Aggiorna la lista dei messaggi con i dati ricevuti.
        // Inserisce i messaggi nella lista <ul> con id="message-list"
        // NOTA: usare i tag <li> per inserire i messaggi!

        // Recupera l'elemento <ul> in cui inserire i messaggi
        const messageList = document.getElementById('message-list');
        // Svuota la lista dei messaggi precedenti (se presenti)
        messageList.innerHTML = '';
        // Aggiunge i messaggi alla lista
        messages.forEach(msg => {
            messageList.innerHTML += `<li>${msg}</li>`;
        });

        // for (let msg of messages) {
        //     messageList.innerHTML += `<li>${msg}</li>`;
        // }

        // Da manuale, avremmo potuto fare anche così, perché è
        // meno oneroso in termini di carico computazionale
        messages.forEach(msg => {
            const li = document.createElement('li');
            li.textContent = msg;
            messageList.appendChild(li);
        });

    })
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
    // Invia la richiesta POST al server
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
        // ci invii una risposta che non contiene né la chiave 'success' né 'error'
        } else {
            alert('Errore sconosciuto!');
        }
    })
    .catch(error => console.error('Error:', error));
    // Come per l'altro fetch, mostra nella console eventuali errori.
}