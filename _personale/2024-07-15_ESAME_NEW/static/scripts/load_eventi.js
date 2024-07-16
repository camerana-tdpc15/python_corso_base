// alert('OK');
const rowLotti = document.querySelector('#row-eventi');


// Fa fetch di un file JSON e lo stampa in console
// (abbiamo aggiunto un esempio di query string per modificare l'ordinamento)
fetch("/api/eventi")
    // ......... QUI FLASK STA LAVORANDO PER PREPARARCI LA RISPOSTA
    // ......... E ALLA FINE CE LA INVIA
    .then(response => response.json())
    .then(data => {
        for (evento of data) {
            console.log(evento);

            // debugger;

            let displayButton = '';
            if(evento.sospeso) {
                // button rosso
                displayButton = '<button class="btn btn-danger w-100" disabled>Sospeso</button>';
            }
            else if (evento.get_qta_disponibile == 0) {
                // button giallo
                displayButton = '<button class="btn btn-warning w-100" disabled>Esaurito</button>';
            } 
            else {
                // button blu
                displayButton = `<a class="btn btn-primary w-100" href="/lotto/${evento.id}">Prenota</a>`;
            }

            rowLotti.innerHTML += `
                <div class="col-lg-3 my-2">
                    <div class="card h-100">
                        <div class="card-header">
                            <h4 class="card-title">${evento.rel_prodotto.nome_prodotto}</h4>
                            <p class="text-end"><small>(cod. evento: ${evento.id})</small><p>
                        </div>
                        <div class="card-body d-flex flex-column">
                            <p>Produttore: <b>${evento.rel_prodotto.rel_produttore.nome_produttore}</b></p>
                            <p>Data consegna: <b>${evento.get_date}</b></p>
                            <p>Q.tà TOT: <b>${evento.evento} ${evento.qta_unita_misura}</b></p>
                            <p>Q.tà Disp: <b>${evento.get_qta_disponibile} ${evento.qta_unita_misura}</b></p>
                            <p>Prezzo: <b>${evento.get_prezzo_str}</b></p>

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
