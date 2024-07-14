// alert('OK'); // Commentato: alert di test

// Seleziona l'elemento con id 'row-lotti' e lo assegna alla variabile rowLotti
const rowLotti = document.querySelector('#row-lotti');

// Fa una fetch di un file JSON dall'API e lo stampa in console
fetch("/api/lotti?order=desc")
    // Qui Flask sta lavorando per prepararci la risposta
    // E alla fine ce la invia
    .then(response => response.json()) // Converte la risposta in formato JSON
    .then(data => { // Elabora i dati ricevuti
        for (lotto of data) { // Itera su ogni lotto ricevuto
            console.log(lotto); // Stampa il lotto in console (debugging)

            // Variabile per il pulsante da visualizzare
            let displayButton = '';
            if(lotto.sospeso) {
                // Se il lotto è sospeso, crea un pulsante rosso disabilitato
                displayButton = '<button class="btn btn-danger w-100" disabled>Sospeso</button>';
            }
            else if (lotto.get_qta_disponibile == 0) {
                // Se il lotto è esaurito, crea un pulsante giallo disabilitato
                displayButton = '<button class="btn btn-warning w-100" disabled>Esaurito</button>';
            } 
            else {
                // Altrimenti, crea un pulsante blu per prenotare il lotto
                displayButton = `<a class="btn btn-primary w-100" href="/lotto/${lotto.id}">Prenota</a>`;
            }

            // Aggiunge un nuovo elemento HTML per ogni lotto nella variabile rowLotti
            rowLotti.innerHTML += `
               <div class="col-lg-4 col-md-4 col-sm-6 my-2 d-flex align-items-stretch">
                    <div class="card h-100 d-flex flex-column">
                        <div class="card-header bg-gas-primary">
                            <h4 class="card-title text-gas-primary">${lotto.rel_prodotto.nome_prodotto}</h4>
                            <p class="text-end"><small>(cod. lotto: ${lotto.id})</small></p>
                        </div>
                        <div class="card-body flex-grow-1">
                            <p>Produttore: <b>${lotto.rel_prodotto.rel_produttore.nome_produttore}</b></p>
                            <p>Data consegna: <b>${lotto.get_date}</b></p>
                            <p>Q.tà TOT: <b>${lotto.qta_lotto} ${lotto.qta_unita_misura}</b></p>
                            <p>Q.tà Disp: <b>${lotto.get_qta_disponibile} ${lotto.qta_unita_misura}</b></p>
                            <p>Prezzo: <b>${lotto.get_prezzo_str}</b></p>
                        </div>
                        <img src="/static/imgs/${lotto.rel_prodotto.immagine}" class="rounded card-img-bottom" alt="${lotto.rel_prodotto.nome_prodotto}">
                        <div class="card-footer">
                            ${displayButton}
                        </div>
                    </div>
                </div>
            `;   
        }
    });

