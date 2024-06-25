

document.addEventListener('DOMContentLoaded', () => {
    getMessage();
    
});


const btnUno = document.getElementById('btn1');

btnUno.onclick = sendMessage


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
            console.log(result);
            if (result.success) {
                getMessage();
                let form = document.getElementById('msg-form');
                form.reset();

            } else if (result.error) {
                alert(result.error);
            }
        })
        .catch(error => console.error('Error:', error));
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
                <li class="list-group-item">${lista}</li>
            `;
            }
        })
        
}
