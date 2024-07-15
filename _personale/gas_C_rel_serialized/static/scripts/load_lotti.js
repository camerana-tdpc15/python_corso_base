// elementi pagina
const rowLotti = document.querySelector('#row-lotti');

onLoad();

function onLoad() {

    // eseguo la chiamata per ottenere i Lotti
    // select dei Lotti con in join Prodotti e join con Produttori 

    const urlLotti = '/api/dati_lotti';

    fetch(urlLotti).then(res => res.json()).then(data => {
        console.log(data);

        for(lotto of data) {

            let renderPrenota = '';
            if (lotto.sospeso) {
                renderPrenota = '<a href="#" class="btn btn-danger disabled w-100">Sospeso</a>';                
            } else if (lotto.get_qta_disponibile == 0) {
                renderPrenota = '<a href="#" class="btn btn-danger disabled w-100">Esaurito</a>';                
            } else {
                renderPrenota = `<a href="/lotto/${lotto.id}" class="btn btn-primary w-100">Prenota</a>`;
            }

            rowLotti.innerHTML += `
            <div class="col-lg-3 mb-3">
                <div class="card mb-3 w-100 h-100">
                    <div class="card-header">
                        <h4 class="card-title">
                            ${lotto.prodotto.nome}
                        </h4>
                        <div class="text-end"><small>(cod. lotto ${lotto.id})</small></div>
                    </div>
                    <div class="card-body d-flex flex-column">
                        <img class="card-img-top" src="${lotto.prodotto.immagine}" alt="Card image" style="width:100%">
                        <p class="card-text">
                            <small>Disponibile da:</small> <b>${lotto.get_date}</b>
                        </p>
                        <p class="card-text">
                            <small>Prodotto da:</small> <b>${lotto.prodotto.produttore.nome}</b>
                        </p>
                        <p class="card-text">
                            <small>Prezzo:</small> <b>${lotto.get_prezzo_str}</b>
                        </p>   
                        <p class="card-text">
                            <small>Q.tà totale lotto:</small> <b>${lotto.qta_lotto}</b>
                        </p>
                        <p class="card-text">
                            <small>Q.tà disponibile:</small> <b>${lotto.get_qta_disponibile}</b>
                        </p>
                        <div class="mt-auto">
                            ${renderPrenota}
                        </div>
                    </div>
                </div>
            </div>
            `;
        }

    });

}