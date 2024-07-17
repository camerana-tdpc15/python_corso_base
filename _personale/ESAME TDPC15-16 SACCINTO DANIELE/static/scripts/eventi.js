document.addEventListener('DOMContentLoaded', function () {
    fetch('/api/eventi?order=asc')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('eventi-container');
            data.forEach(evento => {
                const card = document.createElement('div');
                card.className = 'col-md-4';
                const isAnnullato = evento.annullato;
                card.innerHTML = `
                    <div class="card mb-4 shadow-sm">
                        <div class="card-body">
                            <h5 class="card-title">${evento.rel_eventi.nome_evento}</h5>
                            <p class="card-text">Data: ${evento.get_date}</p>
                            <p class="card-text">Disponibili: ${evento.get_qta_disponibile}</p>
                            <a href="/replica/${evento.id}" class="btn ${isAnnullato ? 'btn-danger' : 'btn-primary'}" ${isAnnullato ? 'disabled' : ''}>Prenota</a>                          
                        </div>
                    </div>
                `;
                container.appendChild(card);
            });
        })
        .catch(error => console.error('Errore:', error));
});
