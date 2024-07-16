// alert('OK');
const rowEventi = document.querySelector('#row-eventi');


// Fa fetch di un file JSON e lo stampa in console
// (abbiamo aggiunto un esempio di query string per modificare l'ordinamento)
fetch("/api/eventi?order=asc")
    // ......... QUI FLASK STA LAVORANDO PER PREPARARCI LA RISPOSTA
    // ......... E ALLA FINE CE LA INVIA
    .then(response => response.json())
    .then(data => {
        for (evento of data) {
            console.log(evento);

            // debugger;

            let displayButton = '';
            if(replica.annullato) {
                // button rosso
                displayButton = '<button class="btn btn-danger w-100" disabled>ANNULLATO</button>';
            }
            else if (replica.get_qta_disponibile == 0) {
                // button giallo
                displayButton = '<button class="btn btn-warning w-100" disabled>Esaurito</button>';
            } 
            else {
                // button blu
                displayButton = `<a class="btn btn-primary w-100" href="/replica/${replica.id}">Prenota</a>`;
            }

            rowLotti.innerHTML += `
                <div class="col-lg-3 my-2">
                    <div class="card h-100">
                        <div class="card-header">
                            <h4 class="card-title">${evento.rel_repliche.rel_eventi.nome_evento}</h4>
                            <p class="text-end"><small>(cod. replica: ${evento.rel_replica.id})</small><p>
                        </div>
                        <div class="card-body d-flex flex-column">
                              <p>Locale: <b>${evento.rel_repliche.rel_eventi.rel_locali.nome_locale}</b></p>
                            <p>Data e ora: <b>${evento.rel_repliche.get_date}</b></p>
                            <p>Q.tà TOT: <b>${evento.rel_repliche.rel_eventi.rel_locali.posti} Posti </b></p>
                            <p>Q.tà Disp: <b>${evento.rel_repliche.get_qta_disponibile} Posti</b></p>
            
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
