// elementi pagina
const rowProduttori = document.querySelector('#row-prod');

onLoad();

function onLoad() {

    // eseguo la chiamata per ottenere le prenotazioni
    // select delle Prenotazioni con in join Lotti, join con Prodotti e join con Produttori 

    const urlProduttori = '/api/produttori';

 // Fa fetch di un file JSON e lo stampa in console
fetch(urlProduttori)
// ......... QUI FLASK STA LAVORANDO PER PREPARARCI LA RISPOSTA
// ......... E ALLA FINE CE LA INVIA
.then(response => response.json())
.then(data => {
    for (prod of data) {
        console.log(prod);

     

        rowProduttori.innerHTML += `
            <div class="col-lg-3 my-2">
                <div class="card h-100">
                    <div class="card-header">
                        <h4 class="card-title">${prod.nome_produttore}</h4>
                        <p class="text-end"><small>(cod. lotto: ${prod.id})</small><p>
                    </div>
                    <div class="card-body">
                        <p>Produttore: <b>${prod.nome_produttore}</b></p>
                        <p>Descrizione: <b>${prod.descrizione}</b></p>
                        <p>Email: <b>${prod.email}</b></p>
                        <p>Indirizzo: <b>${prod.indirizzo}</b></p>
                        <p>Telefono: <b>${prod.telefono}</b></p>

                       
                    </div>
                </div>
            <div>
        `;   
    }
});
}



