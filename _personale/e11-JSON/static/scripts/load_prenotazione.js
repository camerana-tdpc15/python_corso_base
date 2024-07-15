// elementi pagina
const rowPrenotazioni = document.querySelector('#row-prenotazioni');

onLoad();

function onLoad() {

    // eseguo la chiamata per ottenere le prenotazioni
    // select delle Prenotazioni con in join Lotti, join con Prodotti e join con Produttori 

    const urlPrenotazioni = '/api/dati_prenotazioni';

    fetch(urlPrenotazioni).then(res => res.json()).then(data => {
        console.log(data);

        if (data.length == 0) {
            rowPrenotazioni.innerHTML = `<p>Non hai ancora effettuato prenotazioni, <a href="/">scopri i prodotti disponibili</a>!</p>`;
        }          

        for(prenot of data) {

            let renderModifica = '';
            if(!prenot.lotto.sospeso) {
                renderModifica = `<a href="/prenotazione/${prenot.id}" class="btn btn-primary w-100">Modifica prenotazione</a>`;
            } else {
                renderModifica = '<a href="#" class="btn btn-danger disabled">Annullato</a>';                
            }

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