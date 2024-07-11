// alert('OK');
const rowLotti = document.querySelector('#row-utenti');


// Fa fetch di un file JSON e lo stampa in console
fetch("/api/utenti?order=asc")
    // ......... QUI FLASK STA LAVORANDO PER PREPARARCI LA RISPOSTA
    // ......... E ALLA FINE CE LA INVIA
    .then(response => response.json())
    .then(data => {
        for (utente of data) {
            console.log(utente);

            // debugger;

            // let displayButton = '';
            // if(.sospeso) {
            //     // button rosso
            //     displayButton = '<button class="btn btn-danger w-100" disabled>Sospeso</button>';
            // }
            // else if (lotto.get_qta_disponibile == 0) {
            //     // button giallo
            //     displayButton = '<button class="btn btn-warning w-100" disabled>Esaurito</button>';
            // } 
            // else {
            //     // button blu
            //     displayButton = '<button class="btn btn-primary w-100">Prenota</button>';
            // }

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
                            <h4 class="card-title">${utente.nome} ${utente.cognome}</h4>
                            <p class="text-end"><small>(cod. lotto: ${utente.id})</small><p>
                        </div>
                        <div class="card-body">
                            <p>Nome utente: <b>${utente.nome}</b></p>
                            <p>Cognome utente: <b>${utente.cognome}</b></p>
                            <p>Email: <b>${utente.email}</b></p>
                            <p>Telefono: <b>${utente.telefono}</b></p>
                            

                           
                        </div>
                    </div>
                <div>
            `;   
        }
    });

    // <p>Prezzo: <b>${lotto.prezzo_unitario} €/${qta_unita_misura}</b></p>

    //  ${displayButton}

    