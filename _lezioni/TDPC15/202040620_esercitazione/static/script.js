console.log('ciao')

const inputButton = document.getElementById('button');

inputButton.addEventListener('click', sendMessage);


function sendMessage() {
    let data = {
        'nome': document.getElementById('name').value,
        'messaggio': document.getElementById('message').value,
    };
    // Invia la richiesta al server
    fetch('/api/guestbook', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    })
    .then(response => response.json());
    let form = getElementById('msg-form');
    form.reset();
}