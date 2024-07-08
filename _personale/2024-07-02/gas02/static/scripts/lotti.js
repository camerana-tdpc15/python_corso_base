const rowLotti= document.querySelector('#row-lotti')


fetch("/api/lotti")
.then(response => response.json())
.then(data => {
    for(lotto of data){

    let displayButton = '';
    if(lotto.sospeso){
       displayButton = "<button class='btn btn-danger w-100'>Non disponibile</button>" 
    }
    else{
        if(lotto.get_qta_disponibile == 0)
        {displayButton = "<button class='btn btn-warning w-100'>Esaurito</button> }"}
            else{displayButton = `<a class='btn btn-success w-100' href='/lotto/${lotto.id}'>Prenota ora</a> `
    }}

    {rowLotti.innerHTML+= `
    <div class='col-lg-3 my-2'>
        <div class="card">
            <div class='card-header bg-warning'>
            <h4>${lotto.rel_prodotto.nome_prodotto}</h4>
            <p class= 'text-end'><small>Cod prodotto: ${lotto.id}</small></p>
            </div>
            <div class="card-body">Produttore: <b>${lotto.rel_prodotto.rel_produttore.nome_produttore}</b></div>
            <div class="card-body">Data consegna:  <b>${lotto.get_date}</b></div>
            <div class="card-body">Q.Tà Tot:  <b>${lotto.qta_lotto}${lotto.qta_unita_misura}</b></div>
            <div class="card-body">Q.Tà Disp:  <b>${lotto.get_qta_disponibile}${lotto.qta_unita_misura}</b></div>
            <div class="card-body">Prezzo:  <b>${lotto.prezzo_unitario}</b></div>
            ${displayButton}
            
        </div>
    </div>` };
}
}

)
