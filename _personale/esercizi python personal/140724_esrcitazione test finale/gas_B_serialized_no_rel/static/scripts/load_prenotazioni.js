// elementi pagina
const rowPrenotazioni = document.querySelector('#row-prenotazioni');

onLoad();

function onLoad() 

    {
    
    // eseguo la chiamata per ottenere le prenotazioni
    // select delle Prenotazioni con in join Lotti, join con Prodotti e join con Produttori 
    
    const urlPrenotazioni = '/api/dati_prenotazioni';
    
    // Questa funzione viene chiamata quando la pagina si carica.
    // Effettua una chiamata API per recuperare i dati delle prenotazioni.
    // I dati vengono prelevati dall’URL /api/dati_prenotazioni.

    fetch(urlPrenotazioni).then(res => res.json()).then(data => {
        console.log(data);

        // La riga fetch(urlPrenotazioni) recupera i dati dall’URL specificato.
        // La parte .then(res => res.json()) analizza la risposta come JSON.
        // Il blocco successivo .then(data => { ... }) elabora i dati recuperati.

        if (data.length == 0) {
            rowPrenotazioni.innerHTML = `<p>Non hai ancora effettuato prenotazioni, <a href="/">scopri i prodotti disponibili</a>!</p>`;
        }       
            // La condizione if (data.length == 0) verifica se l’array data (contenente le prenotazioni) è vuoto.
            // Se non ci sono prenotazioni (lunghezza dell’array uguale a 0), viene eseguito il blocco di 
            // codice all’interno delle parentesi graffe { ... }.   

        for(prenot of data) {

                // viene eseguito un ciclo for per ogni prenotazione presente nei dati.

            let renderModifica = '';
            if(!prenot.lotto.sospeso) {
                renderModifica = `<a href="/prenotazione/${prenot.id}" class="btn btn-primary w-100">Modifica prenotazione</a>`;
            } else {
                renderModifica = '<a href="#" class="btn btn-danger disabled">Annullato</a>';                
            }
                // Per ciascuna prenotazione:
                // Si determina se il lotto associato alla prenotazione è sospeso (prenot.lotto.sospeso).
                // In base a questa condizione, viene generato un pulsante per la modifica della 
                // prenotazione o un messaggio di annullamento.
                // Vengono costruite le card con i dettagli della prenotazione (nome del prodotto, 
                // data di disponibilità, produttore, prezzo, ecc.) e aggiunte all’elemento rowPrenotazioni.
            

            rowPrenotazioni.innerHTML += `
            <div class="col-lg-3 mb-3">
                <div class="card mb-3 w-100 h-100">
                    <div class="card-header">
                        <h4 class="card-title">
                            ${prenot.lotto.prodotto.nome}
                        </h4>
                        <div class="text-end"><small>(cod. lotto ${prenot.lotto.id} / prenot. ${prenot.id})</small></div>
                    </div>
                    <div class="card-body d-flex flex-column">
                        <p class="card-text">
                            <small>Disponibile da:</small> <b>${prenot.lotto.get_date}</b>
                        </p>
                        <p class="card-text">
                            <small>Prodotto da:</small> <b>${prenot.lotto.prodotto.produttore.nome}</b>
                        </p>
                        <p class="card-text">
                            <small>Prezzo:</small> <b>${prenot.lotto.prezzo_unitario}</b>
                        </p>
                        <p class="card-text">
                            <small>Q.tà totale lotto:</small> <b>${prenot.lotto.qta_lotto}</b>
                        </p> 
                        <p class="card-text">
                            <small>Q.tà disponibile:</small> <b>${prenot.lotto.get_qta_disponibile}</b>
                        </p>
                        <div class="mt-auto alert alert-primary">
                            <p class="card-text">
                                <small>Q.tà prenotata:</small> <b>${prenot.qta} ${prenot.lotto.qta_unita_misura}</b>
                            </p>
                            <p class="card-text">
                                <small>Prezzo totale:</small> <b>${prenot.get_prezzo_totale_str}</b>
                            </p>
                            ${renderModifica}
                        </div>
                    </div>
                </div>
            </div>
            `;
        }

    });

}