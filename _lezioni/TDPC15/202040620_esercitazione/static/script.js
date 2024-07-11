console.log('ciao')

const inputButton = document.getElementById('button');
const spazioPerTesto = document.getElementById('testoDaMostrare');


inputButton.onclick = function() {sendMessage()};


document.addEventListener('DOMContentLoaded', getMessage);

function getMessage() {
    fetch('/api/guestbook').then(response => response.json())
    .then(messages => {

        spazioPerTesto.innerHTML ='';

        messages.forEach(element => {
            spazioPerTesto.innerHTML += `<li>${element}</li>`;
        });
    }).catch(error => console.error('Error:', error));
};

function sendMessage() {
    let data = {
        'nome': document.getElementById('name').value,
        'messaggio': document.getElementById('message').value,
    };
    
    fetch('/api/guestbook', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    }).then(response => response.json())
    .then(result => {

        if (result.success) {
            getMessage();

            let form = getElementById('msg-form');
            form.reset();
        }

        else if (result.error){alert(result.error)}
        else {alert('errore')};



    }).catch(error => console.error('Errore: ', error));
    
};

