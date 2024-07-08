const rowLotti = document.querySelector('#row-lotti');

// Fa fetch di un file JSON e lo stampa in console
fetch("api/lotti")
    .then(response => response.json())
    .then(data => {
        for (lotto of data) {
            let displayButton = '';
            if(lotto.sospeso) {
                displayButton = '<button class="btn btn-danger w-100" disabled>Sospeso</button>';
            }
            else if (lotto.get_qta_disponibile == 0) {
                displayButton = '<button class="btn btn-warning w-100" disabled>Esaurito</button>';
            } 
            else {
                displayButton = `<button class="btn btn-primary w-100" onclick="aggiungiAlCarrello(${lotto.id})">Prenota</button>`;
            }

            rowLotti.innerHTML += `
                <div class="col-lg-3 my-2">
                    <div class="card h-100">
                        <div class="card-header">
                            <h4 class="card-title">${lotto.prodotto.nome_prodotto}</h4>
                            <p class="text-end"><small>(cod. lotto: ${lotto.id})</small><p>
                        </div>
                        <div class="card-body">
                            <p>Produttore: <b>${lotto.prodotto.produttore.nome_produttore}</b></p>
                            <p>Data consegna: <b>${lotto.get_date}</b></p>
                            <p>Q.tà TOT: <b>${lotto.qta_lotto} ${lotto.qta_unita_misura}</b></p>
                            <p>Q.tà Disp: <b>${lotto.get_qta_disponibile} ${lotto.qta_unita_misura}</b></p>
                            <p>Prezzo: <b>${lotto.prezzo_unitario} €/${lotto.qta_unita_misura}</b></p>

                            ${displayButton}
                        </div>
                    </div>
                <div>
            `;   
        }
    });

function aggiungiAlCarrello(lottoId) {
    fetch("/api/carrello", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ action: 'add', lotto_id: lottoId })
    })
    .then(response => response.json())
    .then(data => {
        alert("Lotto aggiunto al carrello!");
    })
    .catch(error => console.error("Errore:", error));
}
