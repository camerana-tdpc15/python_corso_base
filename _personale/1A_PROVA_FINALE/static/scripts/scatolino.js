<div class="text-end"><small>(cod. lotto ${prenot.id} )</small></div>
</div>
<div class="card-body d-flex flex-column">
    <p class="card-text">
        <small>Disponibile da:</small> <b>${prenot.replica.data_ora}</b>
    </p>
    <p class="card-text">
        <small>Locale Evento:</small> <b>${prenot.lotto.prodotto.produttore.nome}</b>
    </p>
    <p class="card-text">
        <small>Prezzo:</small> <b>${prenot.lotto.prezzo_unitario}</b>
    </p>
    <p class="card-text">
        <small>Q.tà totale lotto:</small> <b>${prenot.lotto.qta_lotto}</b>
    </p> 
    <p class="card-text">
        <small>Q.tà disponibile:</small> <b>${prenot.lotto.get_qta_disponibile}</b>
    </p>
    <div class="mt-auto alert alert-primary">
        <p class="card-text">
            <small>Q.tà prenotata:</small> <b>${prenot.qta} ${prenot.lotto.qta_unita_misura}</b>
        </p>
        <p class="card-text">
            <small>Prezzo totale:</small> <b>${prenot.get_prezzo_totale_str}</b>
        </p>