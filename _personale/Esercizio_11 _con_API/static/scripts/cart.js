document.addEventListener('DOMContentLoaded', () => {
    fetch('/api/carrello')
        .then(response => response.json())
        .then(data => {
            let totalCost = 0;
            const cartItemsContainer = document.getElementById('cart-items');

            data.forEach(item => {
                totalCost += item.lotto.prezzo_unitario * item.quantity;

                cartItemsContainer.innerHTML += `
                    <div class="col-lg-3 my-2">
                        <div class="card h-100">
                            <div class="card-header">
                                <h4 class="card-title">${item.lotto.prodotto.nome_prodotto}</h4>
                                <p class="text-end"><small>(cod. lotto: ${item.lotto.id})</small><p>
                            </div>
                            <div class="card-body">
                                <p>Produttore: <b>${item.lotto.prodotto.produttore.nome_produttore}</b></p>
                                <p>Data consegna: <b>${item.lotto.get_date}</b></p>
                                <p>Prezzo: <b>${item.lotto.prezzo_unitario} €/${item.lotto.qta_unita_misura}</b></p>
                                <p>Quantità: 
                                    <input type="number" value="${item.quantity}" min="1" class="form-control" 
                                    onchange="updateQuantity(${item.id}, this.value)">
                                </p>
                                <button class="btn btn-danger w-100" onclick="removeFromCart(${item.id})">Rimuovi</button>
                            </div>
                        </div>
                    </div>
                `;
            });

            document.getElementById('total-cost').innerText = `Costo totale: ${totalCost} €`;
        });
});

function updateQuantity(cartItemId, newQuantity) {
    fetch('/api/carrello', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ action: 'update', cart_item_id: cartItemId, quantity: newQuantity })
    })
    .then(response => response.json())
    .then(data => {
        location.reload();
    })
    .catch(error => console.error('Errore:', error));
}

function removeFromCart(cartItemId) {
    fetch('/api/carrello', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ action: 'delete', cart_item_id: cartItemId })
    })
    .then(response => response.json())
    .then(data => {
        location.reload();
    })
    .catch(error => console.error('Errore:', error));
}
