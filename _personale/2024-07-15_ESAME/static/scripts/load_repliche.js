// alert('OK');
const rowLotti = document.querySelector('#row-eventi');


// Fa fetch di un file JSON e lo stampa in console
// (abbiamo aggiunto un esempio di query string per modificare l'ordinamento)
fetch("/api/repliche?order=asc")
    // ......... QUI FLASK STA LAVORANDO PER PREPARARCI LA RISPOSTA
    // ......... E ALLA FINE CE LA INVIA
    .then(response => response.json())
    .then(data => {
        for (replica of data) {
            console.log(replica);

          

            

            rowLotti.innerHTML += `
                <div class="col-lg-3 my-2">
                    <div class="card h-100">
                        <div class="card-header">
                            <h4 class="card-title">${replica.rel_evento.nome_evento}</h4>
                            <p class="text-end"><small>(cod. evento: ${replica.id})</small><p>
                        </div>
                        <div class="card-body d-flex flex-column">
                            <p>Locale: <b>${replica.rel_evento.rel_locale.nome_locale}</b></p>
                            <p>Luogo: <b>${replica.rel_evento.rel_locale.luogo}</b></p>
                            <p>Data e ora: <b>${replica.data_ora}</b></p>
                            <p>Posti totali: <b>${replica.rel_evento.rel_locale.posti}</b></p>
                            
                            

                            <div class="mt-auto">
                                
                            </div>
                        </div>
                    </div>
                <div>
            `;   
        }
    });

   


    const rowLottiData = document.querySelector('#row-eventi-data');


// Fa fetch di un file JSON e lo stampa in console
// (abbiamo aggiunto un esempio di query string per modificare l'ordinamento)
fetch("/api/repliche?order=asc")
    // ......... QUI FLASK STA LAVORANDO PER PREPARARCI LA RISPOSTA
    // ......... E ALLA FINE CE LA INVIA
    .then(response => response.json())
    .then(data => {
        for (replica of data) {
            console.log(replica);



            if (replica.rel_prenotazioni.length > 0) {

                var cont = 0;

                rowLottiData.innerHTML += `
                    <div class="col-lg-3 my-2">
                        <div class="card h-100">
                            
                            <div class="card-body d-flex flex-column">
                                
                                <p>Posti prenotati: <b>${replica.rel_prenotazioni[cont].quantita}</b></p>
                                
    
                                <div class="mt-auto">
                                    
                                </div>
                            </div>
                        </div>
                    <div>
                `; 
                
                cont += 1;

            }
               

         
            

        }
    });

  