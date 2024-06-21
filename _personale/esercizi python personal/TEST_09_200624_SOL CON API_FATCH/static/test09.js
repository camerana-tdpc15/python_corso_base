function sendMessage() {
    let data = {
        'nome': document.getElementBYId('nome').value,
        'messaggio': document.getElementBYId('messaggio').value,
    };
    fetch('/api/guestbook', {
        method : 'POST',
        headers: {'Countent-Type': 'application/json'},
        body:JSON.stringify(data)
    })
    .then(respose0=>respose0.json())
    .then(result=>{
        if (result.succes) {
            fetchMessages();
        }
        else if (result.error){
            alert(result.error)
        }
    })
    .catch(error =>console.error('Error:',error));
}
document.querySelector('form').addEventListener('submit', function(event) {
    event.preventDefault(); 
});