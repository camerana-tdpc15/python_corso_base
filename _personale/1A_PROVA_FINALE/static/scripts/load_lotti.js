// elementi pagina
const rowLotti = document.querySelector('#row-lotti');

onLoad();

function onLoad() {

    // eseguo la chiamata per ottenere i Lotti
    // select dei Lotti con in join Prodotti e join con Produttori 

    const urlLotti = '/api/dati_repliche';

    fetch(urlLotti).then(res => res.json()).then(data => {
        console.log(data);

        for(replica of data) {

            let renderPrenota = '';
            if (replica.annullato) {
                renderPrenota = '<a href="#" class="btn btn-danger disabled w-100">Sospeso</a>';                
             } else if (replica.get_posti_disponibili == 0) {
                 renderPrenota = '<a href="#" class="btn btn-danger disabled w-100">Esaurito</a>';                
            } else {
                renderPrenota = `<a href="/replica/${replica.id}" class="btn btn-primary w-100">Prenota</a>`;
            }

            rowLotti.innerHTML += `
            <div class="col-lg-3 mb-3">
                <div class="card mb-3 w-100 h-100">
                    <div class="card-header">
                        <h4 class="card-title">
                            ${replica.evento.nome_evento}
                        </h4>
                        <div class="text-end"><small>(cod. lotto ${replica.id})</small></div>
                    </div>
                    <div class="card-body d-flex flex-column">
                        <p class="card-text">
                            <small>Data Evento:</small> <b>${replica.data_ora}</b>
                        </p>
                        <p class="card-text">
                            <small>Locale Evento:</small> <b>${replica.evento.locale.nome_locale}</b>
                        </p>
                        <p class="card-text">
                            <small>Posti in sala:</small> <b>${replica.evento.locale.posti}</b>
                        </p>   
                        <p class="card-text">
                            <small>Posti disponibili:</small> <b>${replica.get_posti_disponibili}</b>
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