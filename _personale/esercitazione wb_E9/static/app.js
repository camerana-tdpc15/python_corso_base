const messagesContainer = document.getElementById('messages-container');
const url = '/api/guestbook'




//document.addEventListener("DOMContentLoaded", () => {
  //  getMessages()
  document.getElementById('submitBtn').addEventListener('click',sendMessage)
  
//});


function getMessages() {
    fetch('/api/guestbook')
        .then(response => {
            if (!response.ok) {
                throw new Error('Errore nella richiesta: ' + response.status);
            }
            return response.json(); 
        })
        .then(data => {
            // Usa i dati qui (es. visualizza i messaggi)
            const messagesContainer = document.getElementById('messages-container');
            data.forEach(message => {
                const messageElement = document.createElement('li'); 
                messageElement.textContent = message.text;
                messagesContainer.appendChild(messageElement);
            });
        })
        .catch(error => {
            console.error('Errore durante la richiesta:', error);
        });
}






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
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            getMessages();
             // @DA FARE: Reset dei campi del form
            document.getElementById('nome').value='';
            document.getElementById('messaggio').value='';
            
            // ...
        } else if (result.error) {
            alert(result.error)
        }
    })
    .catch(error => console.error('Error:', error));
}