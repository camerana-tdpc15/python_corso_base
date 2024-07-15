// Seleziona l'elemento con id 'row-repliche' e lo assegna alla variabile rowRepliche
const rowRepliche = document.querySelector('#row-repliche');

// Fa una fetch di un file JSON dall'API e lo stampa in console
fetch("/api/repliche?order=desc")
    // Qui Flask sta lavorando per prepararci la risposta
    // E alla fine ce la invia
    .then(response => response.json()) // Converte la risposta in formato JSON
    .then(data => { // Elabora i dati ricevuti
        for (replica of data) { // Itera su ogni lotto ricevuto
            console.log(replica); // Stampa la replica in console (debugging)

            // Variabile per il pulsante da visualizzare
            let displayButton = '';
            if(replica.annullato) {
                // Se la replica è annullata, crea un pulsante rosso disabilitato
                displayButton = '<button class="btn btn-danger w-100" disabled>Annullato</button>';
            }
            else if (replica.get_posti_disponibili == 0) {
                // Se i posti sono esauriti, crea un pulsante giallo disabilitato
                displayButton = '<button class="btn btn-warning w-100" disabled>Posti esauriti</button>';
            } 
            else {
                // Altrimenti, crea un pulsante blu per prenotare i posti
                displayButton = `<a class="btn btn-primary w-100" href="/lotto/${replica.id}">Prenota</a>`;
            }

            // Aggiunge un nuovo elemento HTML per ogni lotto nella variabile rowLotti
            rowRepliche.innerHTML += `
               <div class="col-lg-4 col-md-4 col-sm-6 my-2 d-flex align-items-stretch">
                    <div class="card h-100 d-flex flex-column">
                        <div class="card-header bg-gas-primary">
                            <h4 class="card-title text-gas-primary">${replica.rel_evento.nome_evento}</h4>
                            <p class="text-end"><small>(cod. lotto: ${evento.id})</small></p>
                        </div>
                        <div class="card-body flex-grow-1">
                            <p>Luogo: <b>${replica.rel_evento.rel_locale.nome_locale}</b></p>
                            <p>Data replica: <b>${replica.get_date}</b></p>
                            <p>Posti totali: <b>${replica.qta_replica}</b></p>
                            <p>Posti disponibili: <b>${replica.get_posti_disponibili}</b></p>
                </div>
            `;   
        }
    });

