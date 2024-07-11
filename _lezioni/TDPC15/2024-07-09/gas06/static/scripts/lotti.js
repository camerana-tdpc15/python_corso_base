// alert('OK');
const rowLotti = document.querySelector('#row-lotti');


// Fa fetch di un file JSON e lo stampa in console
fetch("/api/lotti?order=desc")
    // ......... QUI FLASK STA LAVORANDO PER PREPARARCI LA RISPOSTA
    // ......... E ALLA FINE CE LA INVIA
    .then(response => response.json())
    .then(data => {
        for (lotto of data) {
            console.log(lotto);

            // debugger;

            let displayButton = '';
            if(lotto.sospeso) {
                // button rosso
                displayButton = '<button class="btn btn-danger w-100" disabled>Sospeso</button>';
            }
            else if (lotto.get_qta_disponibile == 0) {
                // button giallo
                displayButton = '<button class="btn btn-warning w-100" disabled>Esaurito</button>';
            } 
            else {
                // button blu
                displayButton = `<a class="btn btn-primary w-100" href="/lotto/${lotto.id}">Prenota</a>`;
            }

            // if(lotto.sospeso) {
            //     // button rosso
            //     displayButton = '<button class="btn btn-danger w-100" disabled>Sospeso</button>';
            // }
            // else {
            //     if(lotto.get_qta_disponibile == 0) {
            //         // button giallo
            //         displayButton = '<button class="btn btn-warning w-100" disabled>Esaurito</button>';
            //     }
            //     else {
            //         // button verde
            //         displayButton = '<button class="btn btn-primary w-100">Prenota</button>';
            //     }
            // }

            rowLotti.innerHTML += `
                <div class="col-lg-3 my-2">
                    <div class="card h-100">
                        <div class="card-header">
                            <h4 class="card-title">${lotto.rel_prodotto.nome_prodotto}</h4>
                            <p class="text-end"><small>(cod. lotto: ${lotto.id})</small><p>
                        </div>
                        <div class="card-body">
                            <p>Produttore: <b>${lotto.rel_prodotto.rel_produttore.nome_produttore}</b></p>
                            <p>Data consegna: <b>${lotto.get_date}</b></p>
                            <p>Q.tà TOT: <b>${lotto.qta_lotto} ${lotto.qta_unita_misura}</b></p>
                            <p>Q.tà Disp: <b>${lotto.get_qta_disponibile} ${lotto.qta_unita_misura}</b></p>
                            <p>Prezzo: <b>${lotto.get_prezzo_str}</b></p>

                            ${displayButton}
                        </div>
                    </div>
                <div>
            `;   
        }
    });

    // <p>Prezzo: <b>${lotto.prezzo_unitario} €/${qta_unita_misura}</b></p>
