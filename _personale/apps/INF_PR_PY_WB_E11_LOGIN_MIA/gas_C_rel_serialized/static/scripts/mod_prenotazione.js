// elementi pagina
const rowModPrenotazione = document.querySelector('#row-mod-prenotazione');

onLoad();

function onLoad() {

    // eseguo la chiamata per ottenere le prenotazioni
    // select delle Prenotazioni con in join Lotti, join con Prodotti e join con Produttori 

    const urlModPrenotazione = '/prenotazione/<int:prenotazione_id>';

    fetch(urlModPrenotazione).then(res => res.json()).then(data => {
        console.log(data);

        rowModPrenotazione.innerHTML = `
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h4 class="card-title">
                                {{ prenotazione.lotto.prodotto.nome }}
                            </h4>
                            <div class="text-end"><small>(cod. lotto {{ prenotazione.lotto.id }} / prenot. {{ prenotazione.id }})</small></div>
                        </div>
                        <div class="card-body">
                            <p class="card-text">
                                <small>Disponibile da:</small> <b>{{ prenotazione.lotto.get_date() }}</b>
                            </p>
                            <p class="card-text">
                                <small>Prodotto da:</small> <b>{{ prenotazione.lotto.prodotto.produttore.nome }}</b>
                            </p>
                            <p class="card-text">
                                <small>Q.tà totale lotto:</small> <b>{{ prenotazione.lotto.qta_lotto }} {{ prenotazione.lotto.qta_unita_misura }}</b>
                            </p>
                            <p class="card-text">
                                <small>Q.tà disponibile:</small> <b>{{ prenotazione.lotto.get_qta_disponibile() }} {{ prenotazione.lotto.qta_unita_misura }}</b>
                            </p>
                            <p class="card-text">
                                <small>Prezzo:</small> <b>{{ prenotazione.lotto.get_prezzo_str() }}</b>
                            </p>
                            <div class="row alert alert-primary text-center">
                                <div class="col card-text">
                                    <small>Q.tà già prenotata:</small> <b>{{ prenotazione.qta }} {{ prenotazione.lotto.qta_unita_misura }}</b>
                                </div>
                                <div class="col card-text">
                                    <small>Prezzo totale:</small> <b>{{ prenotazione.get_prezzo_totale_str() }}</b>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
          
            `;

    });

}



