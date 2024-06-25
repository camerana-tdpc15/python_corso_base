function sendMessage() {
    let data = {
        'nome': document.getElementById('nome').value,
        'messaggio': document.getElementById('messaggio').value,
    };

    fetch('/api/guestbook', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(result => {
            console.log(result)
            getMessage()
        })
        
}

function getMessage() {

    fetch('/api/guestbook')
        .then(response => response.json())
        .then(result => {
            //console.log(result);
            const listaMessaggi = document.getElementById('lista-messaggi');
            listaMessaggi.innerHTML = '';
            for (lista of result) {
                listaMessaggi.innerHTML += `
                <li>${lista}</li>
            `;
            }
        })
        
}
