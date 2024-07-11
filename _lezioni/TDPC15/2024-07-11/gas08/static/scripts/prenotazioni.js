// alert('OK');
const rowPrenotazioni = document.querySelector('#row-prenotazioni');


// Fa fetch di un file JSON e lo stampa in console
fetch("/api/prenotazioni")
    // ......... QUI FLASK STA LAVORANDO PER PREPARARCI LA RISPOSTA
    // ......... E ALLA FINE CE LA INVIA
    .then(response => response.json())
    .then(data => {
        for (prenot of data) {
            console.log(prenot);

            // debugger;

            let displayButton = '';
            if(prenot.rel_lotto.sospeso) {
                // button rosso
                displayButton = '<button class="btn btn-danger w-100" disabled>Sospeso</button>';
            }
            else if (prenot.rel_lotto.get_qta_disponibile == 0) {
                // button giallo
                displayButton = '<button class="btn btn-warning w-100" disabled>Esaurito</button>';
            } 
            else {
                // button blu
                displayButton = `<a class="btn btn-primary w-100" href="/prenotazione/${prenot.id}">Modifica</a>`;
            }

            rowPrenotazioni.innerHTML += `
                <div class="col-lg-3 my-2">
                    <div class="card h-100">
                        <div class="card-header">
                            <h4 class="card-title">${prenot.rel_lotto.rel_prodotto.nome_prodotto}</h4>
                            <p class="text-end"><small>(cod. lotto: ${prenot.rel_lotto.id})</small><p>
                        </div>
                        <div class="card-body">
                            <p>Produttore: <b>${prenot.rel_lotto.rel_prodotto.rel_produttore.nome_produttore}</b></p>
                            <p>Data consegna: <b>${prenot.rel_lotto.get_date}</b></p>
                            <p>Q.tà TOT: <b>${prenot.rel_lotto.qta_lotto} ${prenot.rel_lotto.qta_unita_misura}</b></p>
                            <p>Q.tà Disp: <b>${prenot.rel_lotto.get_qta_disponibile} ${prenot.rel_lotto.qta_unita_misura}</b></p>
                            <p>Prezzo: <b>${prenot.rel_lotto.get_prezzo_str}</b></p>

                            <p>Q.ta prenotata: <b>${prenot.qta} ${prenot.rel_lotto.qta_unita_misura}</b></p>

                            ${displayButton}
                        </div>
                    </div>
                <div>
            `;   
        }
    });

    // <p>Prezzo: <b>${lotto.prezzo_unitario} €/${qta_unita_misura}</b></p>
