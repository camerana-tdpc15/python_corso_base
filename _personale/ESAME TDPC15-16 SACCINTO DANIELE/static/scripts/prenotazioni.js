// alert('OK');
const rowPrenotazioni = document.querySelector('#row-prenotazioni');


// Fa la fetch di un file JSON e lo stampa in console
fetch("/api/prenotazioni")
    // ......... QUI FLASK STA LAVORANDO PER PREPARARCI LA RISPOSTA
    // ......... E ALLA FINE CE LA INVIA
    .then(response => response.json())
    .then(data => {
        for (prenot of data) {
            console.log(prenot);

            // debugger;

            let displayButton = '';
            if(prenot.rel_repliche.annullato) {
                // button rosso
                displayButton = '<button class="btn btn-danger w-100" disabled>ANNULLATO</button>';
            }
            else if (prenot.rel_repliche.get_qta_disponibile == 0) {
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
                            <h4 class="card-title">${prenot.rel_repliche.rel_eventi.nome_evento}</h4>
                            <p class="text-end"><small>(cod. replica: ${prenot.rel_replica.id})</small><p>
                        </div>
                        <div class="card-body d-flex flex-column">
                            <p>Locale: <b>${prenot.rel_repliche.rel_eventi.rel_locali.nome_locale}</b></p>
                            <p>Data e ora: <b>${prenot.rel_repliche.get_date}</b></p>
                            <p>Q.tà TOT: <b>${prenot.rel_repliche.rel_eventi.rel_locali.posti} Posti </b></p>
                            <p>Q.tà Disp: <b>${prenot.rel_repliche.get_qta_disponibile} Posti</b></p>
            
                            <p>Q.ta prenotata: <b>${prenot.quantita}</b></p>

                            <div class="mt-auto">
                                ${displayButton}
                            </div>
                        </div>
                    </div>
                <div>
            `;   
        }
    });

    // <p>Prezzo: <b>${lotto.prezzo_unitario} €/${qta_unita_misura}</b></p>
