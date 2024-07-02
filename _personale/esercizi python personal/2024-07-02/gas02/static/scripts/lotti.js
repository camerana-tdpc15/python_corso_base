// alert('OK')
const rowlotti = document.querySelector('#row-lotti');


// Fa fetch di un file JSON e lo stampa in console
fetch('../static/data/dati_lotti.json')
    .then(response => response.json())
    .then(data => {
        for (lotto of data){
            //console.log(lotto);
            let displayButton='';
            if (lotto.sospeso){
                displayButton ='<button class="btn btn-warning w-100" disabled>Sospeso</Button>'
            }
            else{
                if(lotto.get_qta_disponibile==0){
                    dispalyButton='<button class="btn btn-danger w-100" disabled>Esaurito</Button>'
                }
                else{
                    dispalyButton='<button class="btn btn-primary w-100">Prenota</Button>'
                }
            }


            rowlotti.innerHTML +=`
            <div class="col-lg-3 my-2">
               <div class="card">
                    <div class="card-header">
                        <h4 class="card-title">${lotto.prodotto.nome}</h4>
                        <p class="text-end"><small>(cod. lotto${lotto.id})</small></p>
                    </div>
                    <div class="card-body">
                        <p> Produttore: <b>${lotto.prodotto.produttore.nome}</b></p>
                        <p> Produttore: <b>${lotto.get_date}</b></p>
                        <p> Produttore: <b>${lotto.qta_lotto}</b></p>
                        <p> Produttore: <b>${lotto.qta_lotto} ${lotto.qta_unita_di_misura}</b></p>
                        <p> Produttore: <b>${lotto.get_qta_disponibile} ${lotto.qta_unita_di_misura}</b></p>
                        <p> Produttore: <b>${lotto.get_prezzo_str}</b></p>
                        ${displayButton}
                    </div>
                </div>
            </div>
            `;
        } 
    });
