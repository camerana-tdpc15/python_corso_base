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
            if(!prenot.replica.annullato) {
                renderModifica = `<a href="/prenotazione/${prenot.id}" class="btn btn-primary w-100">Modifica prenotazione</a>`;
            } else {
                renderModifica = '<a href="#" class="btn btn-danger disabled">Annullato</a>';                
            }

            rowPrenotazioni.innerHTML += `
            <div class="col-lg-3 mb-3">
                <div class="card mb-3 w-100 h-100">
                    <div class="card-header">
                        <h4 class="card-title">
                            ${prenot.replica.evento.nome_evento}
                        </h4>
                    
                            ${renderModifica}
                        </div>
                    </div>
                </div>
            </div>
            `;
        }

    });

}