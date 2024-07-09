// alert('OK')
const rowlotti = document.querySelector('#row-lotti');


// Fa fetch di un file JSON e lo stampa in console
fetch('/api/lotti')
    .then(response => response.json())
    .then(data => {
        for (lotto of data) {
            //console.log(lotto);
            
            let displayButton = '';
            if (lotto.sospeso) {
                displayButton = '<button class="btn btn-warning w-100" disabled>Sospeso</button>'
            }
            else if (lotto.get_qta_disponibile == 0) {
                displayButton = '<button class="btn btn-danger w-100" disabled>Esaurito</button>'
            }
            else {
                displayButton = '<a class="btn btn-primary w-100" href="/lotto/${loto_id}">Prenota</button>'
            }



            rowlotti.innerHTML += `
            <div class="col-lg-3 my-2">
               <div class="card">
                    <div class="card-header">
                        <h4 class="card-title">${lotto.prodotto.nome_prodotto}</h4>
                        <p class="text-end"><small>(cod. lotto${lotto.id})</small></p>
                    </div>
                    <div class="card-body">
                        <p> Produttore: <b>${lotto.prodotto.produttore.nome_produttore}</b></p>
                        <p> Data_consegna: <b>${lotto.get_date}</b></p>
                        <p> Q.ta_tot: <b>${lotto.qta_lotto}</b></p>
                        <p> Q.ta disp: <b>${lotto.qta_lotto} ${lotto.qta_unita_di_misura}</b></p>
                        <p> Q.ta: <b>${lotto.get_qta_disponibile} ${lotto.qta_unita_di_misura}</b></p>
                        <p> Prezzo: <b>${lotto.prezzo_unitario} €/${qta_unita_di_misura}</b></p>
                        <p> Prezzo: <b>${lotto.get_prezzo_str}</b></p>
                        ${displayButton}
                    </div>
                </div>
            </div>
            `;
        }
    });
