// alert('OK');
const rowLotti = document.querySelector('#row-prod');


// Fa fetch di un file JSON e lo stampa in console
fetch("/api/produttori?order=asc")
    // ......... QUI FLASK STA LAVORANDO PER PREPARARCI LA RISPOSTA
    // ......... E ALLA FINE CE LA INVIA
    .then(response => response.json())
    .then(data => {
        for (prod of data) {
            console.log(prod);

            // debugger;

            // let displayButton = '';
            // if(lotto.sospeso) {
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
                            <h4 class="card-title">${prod.nome_produttore}</h4>
                            <p class="text-end"><small>(cod. lotto: ${prod.id})</small><p>
                        </div>
                        <div class="card-body">
                            <p>Produttore: <b>${prod.nome_produttore}</b></p>
                            <p>Descrizione: <b>${prod.descrizione}</b></p>
                            <p>Email: <b>${prod.email}</b></p>
                            <p>Indirizzo: <b>${prod.indirizzo}</b></p>
                            <p>Telefono: <b>${prod.telefono}</b></p>

                           
                        </div>
                    </div>
                <div>
            `;   
        }
    });

    // <p>Prezzo: <b>${lotto.prezzo_unitario} €/${qta_unita_misura}</b></p>


    //   ${displayButton}
