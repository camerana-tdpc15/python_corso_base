//alert('ok')

// creo varibile che abbia id
const rowProduttori = document.querySelector('#row-produttori')

 // Fa fetch di un file JSON e lo stampa in console
 fetch("../static/data/dati_produttori.json")
 .then(response => response.json())
 .then(data => {
    for(produttore of data){
    //console.log(produttore.nome);

    // dichiaro la lista dei nomi dei prodotti
    let nomi_prodotti_list = '';

    // creo un ciclo for che per ogni prodotto mi tiri fuori il nome
    for(prodotto of produttore.prodotti){
        nomi_prodotti_list += `<li>${prodotto.nome}</li>`
    }
    
        rowProduttori.innerHTML += `
            <div class="col-lg-3 my-5">
                <div class="card">
                    <h4 class="card-title bg-secondary">${produttore.nome}</h4>
                    <p class ="text-end"><small>(descrizione: ${produttore.descrizione})</small></p>
                    <div class="card-body">
                        <p>Indirizzo: <b>${produttore.indirizzo}</b></p>
                        <p>Email: ${produttore.email}</p>                        
                    </div>


                    <button type="button" class="btn btn-primary" data-bs-toggle="collapse" data-bs-target="#${collapseId}">Prodotti</button>
                    <div id="${collapseId}o" class="collapse">
                        Prodotti:
                                <ul>
                                    ${nomi_prodotti_list}
                                </ul>
                        </div>
                    </div>
                
            </div>

            
         `;
     }
    }
 );

 function create_card(){

 }