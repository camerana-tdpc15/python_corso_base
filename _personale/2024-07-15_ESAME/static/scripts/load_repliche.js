// alert('OK');
const rowLotti = document.querySelector('#row-eventi');


// Fa fetch di un file JSON e lo stampa in console
// (abbiamo aggiunto un esempio di query string per modificare l'ordinamento)
fetch("/api/repliche?order=asc")
    // ......... QUI FLASK STA LAVORANDO PER PREPARARCI LA RISPOSTA
    // ......... E ALLA FINE CE LA INVIA
    .then(response => response.json())
    .then(data => {
        for (replica of data) {
            console.log(replica);

            // debugger;

            // let displayButton = '';
            // if(replica.annullato) {
            //     // button rosso
            //     displayButton = '<button class="btn btn-danger w-100" disabled>Sospeso</button>';
            // }
            // else if (replica.get_qta_disponibile == 0) {
            //     // button giallo
            //     displayButton = '<button class="btn btn-warning w-100" disabled>Esaurito</button>';
            // } 
            // else {
            //     // button blu
            //     displayButton = `<a class="btn btn-primary w-100" href="/lotto/${replica.id}">Prenota</a>`;
            // }

            

            rowLotti.innerHTML += `
                <div class="col-lg-3 my-2">
                    <div class="card h-100">
                        <div class="card-header">
                            <h4 class="card-title">${replica.rel_evento.nome_evento}</h4>
                            <p class="text-end"><small>(cod. evento: ${replica.id})</small><p>
                        </div>
                        <div class="card-body d-flex flex-column">
                            <p>Locale: <b>${replica.rel_evento.rel_locale.nome_locale}</b></p>
                            <p>Luogo: <b>${replica.rel_evento.rel_locale.luogo}</b></p>
                            <p>Data e ora: <b>${replica.data_ora}</b></p>
                            <p>Posti totali: <b>${replica.rel_evento.rel_locale.posti}</b></p>
                            <p>Posti prenotati: <b>${replica.rel_prenotazioni.quantita}</b></p>
                            

                            <div class="mt-auto">
                                
                            </div>
                        </div>
                    </div>
                <div>
            `;   
        }
    });

    // <p>Prezzo: <b>${lotto.prezzo_unitario} €/${qta_unita_misura}</b></p>

    //  ${displayButton}
