
//creiamo una funzione asincrona di inviare messaggi che riceve un paramtro 'EVENT'
async function sendMessage(event) {
    event.preventDefault(); // questo fa che il form non si invie e si ricarica la paggina

    let formData = new URLSearchParams();  //facio una variabile per con l'oggetto URLSearchParams() dove se impostara chiave valore che saranno i campi sotto
    formData.append('nome', document.getElementById('nome').value);  //appendiamo i campi 
    formData.append('messaggio', document.getElementById('messaggio').value);

    try {   // come utiliziamo una funzione asincrona usiamo try e catch per manipolare tutti gli errori nella esecuzione
        let response = await fetch('/api/guestbook', { // creamo la variabile response che dentro di questa faremo la fetch ma prima utiliziamo AWAY per aspettare che si complete tutta la richiesta
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, //il tipo di contenuto sara codificato in formato url
            body: formData.toString() // il corpo si transforma in stringa
        });

        let result = await response.json(); //una vez tutta completa a risposta la manipoliamo come json

        if (result.success) {
            fetchMessages(); // si tutto va ben attualiza i emssaggi dopo di inviare il form

            document.getElementById('nome').value = '';  // e svuota i campi
            document.getElementById('messaggio').value = '';
        } else {
            alert(result.error);  // oppure da errore
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

async function fetchMessages() {  
    try {
        const response = await fetch('/api/guestbook');
        const messages = await response.json();
        const messagesList = document.getElementById('messages');
        messagesList.innerHTML = '';
        Object.entries(messages).forEach(([key, value]) => {
            const listItem = document.createElement('li');
            listItem.textContent = `${key}: ${value}`;
            messagesList.appendChild(listItem);
        });
    } catch (error) {
        console.error('Error fetching messages:', error);
    }
}

document.addEventListener('DOMContentLoaded', fetchMessages);  // Carga los mensajes cuando se carga la página