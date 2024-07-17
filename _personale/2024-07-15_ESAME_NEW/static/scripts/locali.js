// alert('OK');
const rowLocali = document.querySelector('#row-locali');


// Fa fetch di un file JSON e lo stampa in console
fetch("/api/locali?order=asc")
    // ......... QUI FLASK STA LAVORANDO PER PREPARARCI LA RISPOSTA
    // ......... E ALLA FINE CE LA INVIA
    .then(response => response.json())
    .then(data => {
        for (locale of data) {
            console.log(locale);

        

            rowLocali.innerHTML += `
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

  

    