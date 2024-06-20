const messagesContainer = document.getElementById('messages');
const url = '/api/guestbook'


function submit() {
    let data = {
        'nome': document.getElementById('nome').value,
        'messaggio': document.getElementById('messaggio').value,

    };

//Invia la richiesta al server

fetch('api/guestbook',{

method:'POST',
headers:{'Content-types:':'application/json'},
body:JSON.stringify(data)
})
.then(response=> response.json())
.then(result => {
    if(result.success){
        fetchMessages();
                
            document.getElementById('nome').value = '';
            document.getElementById('messaggio').value = '';
    

    }else if(result.error){
        alert(result.error)
    }
})
.catch(error => console.error('Error:', error));
}


function stampa(){
    
    fetch(url)
    .then(response => response.json())
    .then(data => {
        console.log(data);
        document.getElementById('messagio').innerText = data
        
    })
   

    
}



