//alert('ok')

// creo varibile che abbia id
const rowLotti = document.querySelector('#row-lotti')

 // Fa fetch di un file JSON e lo stampa in console
 fetch("../static/data/dati_lotti.json")
 .then(response => response.json())
 .then(data => {
     for (lotto of data){
         //console.log(lotto.prodotto.nome);
         
         //creo variabile 
         let displayButton = ''
        if(lotto.sospeso) {
            // button rosso
            displayButton = '<button class = "btn btn-danger w=100 disable">Non disponibile</button>'
        }
        else {
            if(lotto.get_qta_disponibile == 0){
                // button giallo
                displayButton = '<button class = "btn btn-warning w=100 disable">Esautiro</button>'
            }
            else{
                // button verde
                displayButton = '<button class = "btn btn-primary w=100">Prenota ora</button>'
            }
        }
         rowLotti.innerHTML += `
            <div class="col-lg-3 my-5">
                <div class="card">
                    <h4 class="card-title bg-secondary">${lotto.prodotto.nome}</h4>
                    <p class ="text-end"><small>(cod.lotto: ${lotto.id})</small></p>
                    <div class="card-body">
                        <p>Produttore: <b>${lotto.prodotto.produttore.nome}</b></p>
                        <p>Data consegna: ${lotto.get_date}</p>
                        <p>Quantità totale: ${lotto.qta_lotto} ${lotto.qta_unita_misura}</p>
                        <p>Quantità totale disponibile: ${lotto.get_qta_disponibile} ${lotto.qta_unita_misura}</p>
                        <p>Prezzo: <b>${lotto.get_prezzo_str}</b></p>

                        ${displayButton}
                    </div>
                </div>
            </div>
         `;
     }
 });

 function create_card(){

 }