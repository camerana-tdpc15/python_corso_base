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
                            <h4 class="card-title">${locale.nome_locale}</h4>
                            <p class="text-end"><small>(codice: ${locale.id})</small><p>
                        </div>
                        <div class="card-body">
                            <p>Nome locale: <b>${locale.nome_locale}</b></p>
                            <p>Luogo: <b>${locale.luogo}</b></p>
                            <p>Posti: <b>${locale.posti}</b></p>
                            
                            

                           
                        </div>
                    </div>
                <div>
            `;   
        }
    });

  

    