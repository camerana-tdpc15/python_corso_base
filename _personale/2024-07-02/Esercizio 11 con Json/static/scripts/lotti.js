// alert('OK')

const rowlotti = document.querySelector('#row-lotti');

 // Fa fetch di un file JSON e lo stampa in console
 fetch("../static/data/dati_lotti.json")
 .then(response => response.json())
 .then(data => {
     for (lotto of data) {
     //console.log(lotto.prodotto.produttore)        // ciclo i lotti per trovare il nome prodotto
        let displayButton = '';
        if(lotto.sospeso) {
            // bottone rosso
            displayButton = '<a button class="btn btn-danger w-100" disable>Sospeso</a>';
        }

        else {
            if(lotto.get_qta_disponibile == 0) {
                //button giallo
            displayButton = '<a button class="btn btn-warning w-100" disable>Esaurito</a>';
        }
            else {
                {
                displayButton = '<a button class="btn btn-primary w-100">Prenota</a>';
                }
        }}

        rowlotti.innerHTML += `
            <div class="col-lg-4 my-2">
            <div class="card h-100">
                <div class="card-header">
                <h4 class="card-title">${lotto.prodotto.nome}</h4>
                <p class="text-end"><small>(cod. lotto: ${lotto.id})</small></p>
                </div>
                <div class="card-body">
                <p><b>${lotto.prodotto.produttore.nome}</b></p>
                <p>Data consegna: <b>${lotto.data_consegna}</b></p>
                <p>Quantità lotto: <b>${lotto.qta_lotto} ${lotto.qta_unita_misura}</b></p>
                <p>Quantità disponibile: <b>${lotto.get_qta_disponibile} ${lotto.qta_unita_misura}</b></p>
                <p>Prezzo: <b>${lotto.get_prezzo_str}</b></p>
                ${displayButton}
                </div>
            </div>
            </div>`
    }
 });
