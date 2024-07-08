// Funzione per effettuare chiamate API
async function apiCall(url, method = 'GET', data = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json'
        },
        credentials: 'include'
    };
    if (data) {
        options.body = JSON.stringify(data);
    }
    const response = await fetch(url, options);
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
}

// Funzione per aggiornare la navigazione in base allo stato di login
function updateNavigation(isLoggedIn) {
    document.getElementById('loginLink').style.display = isLoggedIn ? 'none' : 'block';
    document.getElementById('logoutLink').style.display = isLoggedIn ? 'block' : 'none';
    document.getElementById('prenotazioniLink').style.display = isLoggedIn ? 'block' : 'none';
}

// Router
async function router() {
    const routes = {
        'home': renderHome,
        'login': renderLogin,
        'logout': handleLogout,
        'prodotti': renderProdotti,
        'prodotto': renderProdotto,
        'prenotazioni': renderPrenotazioni
    };

    const hash = window.location.hash.slice(1) || 'home';
    const [route, param] = hash.split('/');

    if (routes[route]) {
        await routes[route](param);
    } else {
        renderNotFound();
    }
}

// Funzioni di rendering
function renderHome() {
    const html = `
        <h1>Benvenuto in GAS App</h1>
        <p>Qui puoi trovare i prodotti disponibili e gestire le tue prenotazioni.</p>
        <a href="#prodotti" class="btn btn-primary">Vedi i prodotti disponibili</a>
    `;
    document.getElementById('content').innerHTML = html;
}

function renderLogin() {
    const html = `
        <h1>Login</h1>
        <form id="loginForm">
            <div class="mb-3">
                <label for="email" class="form-label">Email</label>
                <input type="email" class="form-control" id="email" required>
            </div>
            <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input type="password" class="form-control" id="password" required>
            </div>
            <button type="submit" class="btn btn-primary">Login</button>
        </form>
    `;
    document.getElementById('content').innerHTML = html;
    document.getElementById('loginForm').addEventListener('submit', handleLogin);
}

async function handleLogin(event) {
    event.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    try {
        const response = await apiCall('/api/login', 'POST', { email, password });
        updateNavigation(true);
        window.location.hash = '#home';
    } catch (error) {
        console.error('Login failed:', error);
        alert('Login fallito. Riprova.');
    }
}

async function handleLogout() {
    try {
        await apiCall('/api/logout', 'POST');
        updateNavigation(false);
        window.location.hash = '#home';
    } catch (error) {
        console.error('Logout failed:', error);
    }
}

async function renderProdotti() {
    try {
        const lotti = await apiCall('/api/lotti');
        let html = '<h1>Prodotti disponibili</h1><div class="row">';
        lotti.forEach(lotto => {
            html += `
                <div class="col-md-4 mb-4">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">${lotto.prodotto.nome_prodotto}</h5>
                            <p class="card-text">Quantità disponibile: ${lotto.quantita_disponibile} ${lotto.qta_unita_misura}</p>
                            <p class="card-text">Prezzo: €${lotto.prezzo_unitario}/${lotto.qta_unita_misura}</p>
                            <a href="#prodotto/${lotto.id}" class="btn btn-primary">Dettagli</a>
                        </div>
                    </div>
                </div>
            `;
        });
        html += '</div>';
        document.getElementById('content').innerHTML = html;
    } catch (error) {
        console.error('Error:', error);
    }
}

async function renderProdotto(lottoId) {
    try {
        const lotto = await apiCall(`/api/lotti/${lottoId}`);
        const html = `
            <h1>${lotto.prodotto.nome_prodotto}</h1>
            <p>Quantità disponibile: ${lotto.quantita_disponibile} ${lotto.qta_unita_misura}</p>
            <p>Prezzo: €${lotto.prezzo_unitario}/${lotto.qta_unita_misura}</p>
            <form id="prenotaForm">
                <div class="mb-3">
                    <label for="quantita" class="form-label">Quantità</label>
                    <input type="number" class="form-control" id="quantita" min="1" max="${lotto.quantita_disponibile}" required>
                </div>
                <button type="submit" class="btn btn-primary">Prenota</button>
            </form>
        `;
        document.getElementById('content').innerHTML = html;
        document.getElementById('prenotaForm').addEventListener('submit', (event) => handlePrenotazione(event, lottoId));
    } catch (error) {
        console.error('Error:', error);
    }
}

async function renderPrenotazioni() {
    try {
        const prenotazioni = await apiCall('/api/prenotazioni');
        let html = '<h1>Le mie prenotazioni</h1>';
        if (prenotazioni.length === 0) {
            html += '<p>Non hai ancora effettuato prenotazioni.</p>';
        } else {
            html += '<ul class="list-group">';
            prenotazioni.forEach(p => {
                html += `
                    <li class="list-group-item">
                        ${p.lotto.prodotto.nome_prodotto} - Quantità: ${p.qta} ${p.lotto.qta_unita_misura}
                        <button class="btn btn-sm btn-danger float-end" onclick="deletePrenotazione(${p.id})">Elimina</button>
                    </li>
                `;
            });
            html += '</ul>';
        }
        document.getElementById('content').innerHTML = html;
    } catch (error) {
        console.error('Error:', error);
    }
}

async function handlePrenotazione(event, lottoId) {
    event.preventDefault();
    const quantita = document.getElementById('quantita').value;
    try {
        await apiCall('/api/prenotazioni', 'POST', { lotto_id: lottoId, qta: quantita });
        alert('Prenotazione effettuata con successo');
        window.location.hash = '#prenotazioni';
    } catch (error) {
        console.error('Prenotazione failed:', error);
        alert('Prenotazione fallita. Riprova.');
    }
}

async function deletePrenotazione(prenotazioneId) {
    if (confirm('Sei sicuro di voler eliminare questa prenotazione?')) {
        try {
            await apiCall(`/api/prenotazioni/${prenotazioneId}`, 'DELETE');
            renderPrenotazioni();
        } catch (error) {
            console.error('Delete failed:', error);
            alert('Eliminazione fallita. Riprova.');
        }
    }
}

function renderNotFound() {
    document.getElementById('content').innerHTML = '<h1>404 - Pagina non trovata</h1>';
}

// Event listeners
window.addEventListener('hashchange', router);
window.addEventListener('load', router);

// Controlla lo stato di login al caricamento della pagina
window.addEventListener('load', async () => {
    try {
        await apiCall('/api/user');
        updateNavigation(true);
    } catch (error) {
        updateNavigation(false);
    }
});