// Main JavaScript file (main.js)

// Helper function to make API calls
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

// Function to update navigation based on login status
function updateNavigation(isLoggedIn) {
    document.getElementById('loginLink').style.display = isLoggedIn ? 'none' : 'block';
    document.getElementById('registrazioneLink').style.display = isLoggedIn ? 'none' : 'block';
    document.getElementById('logoutLink').style.display = isLoggedIn ? 'block' : 'none';
}

// Router function
async function router() {
    const routes = {
        'home': renderHome,
        'login': renderLogin,
        'logout': handleLogout,
        'registrazione': renderRegistrazione,
        'prodotto': renderProdotto,
        'carrello': renderCarrello,
        'nuovo_produttore': renderNuovoProduttore,
        'nuovo_prodotto': renderNuovoProdotto,
        'nuovo_lotto': renderNuovoLotto,
        'gestisci_utenti': renderGestisciUtenti
    };

    const path = window.location.hash.slice(1) || 'home';
    const [route, param] = path.split('/');
    
    if (routes[route]) {
        await routes[route](param);
    } else {
        renderNotFound();
    }
}

// Render functions for each page
async function renderHome() {
    try {
        const data = await apiCall('/');
        let html = '<h1>Prodotti disponibili</h1><div class="row">';
        data.forEach(item => {
            html += `
                <div class="col-md-4 mb-4">
                    <div class="card">
                        <img src="${item.prodotto.image_url}" class="card-img-top" alt="${item.prodotto.nome_prodotto}">
                        <div class="card-body">
                            <h5 class="card-title">${item.prodotto.nome_prodotto}</h5>
                            <p class="card-text">Disponibile: ${item.disponibile ? 'Sì' : 'No'}</p>
                            <a href="#prodotto/${item.prodotto.id}" class="btn btn-primary">Dettagli</a>
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

async function renderLogin() {
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
        const response = await apiCall('/login', 'POST', { email, password });
        updateNavigation(true);
        window.location.hash = '#home';
    } catch (error) {
        console.error('Login failed:', error);
        alert('Login failed. Please try again.');
    }
}

async function handleLogout() {
    try {
        await apiCall('/logout');
        updateNavigation(false);
        window.location.hash = '#home';
    } catch (error) {
        console.error('Logout failed:', error);
    }
}

async function renderRegistrazione() {
    const html = `
        <h1>Registrazione</h1>
        <form id="registrationForm">
            <div class="mb-3">
                <label for="nome" class="form-label">Nome</label>
                <input type="text" class="form-control" id="nome" required>
            </div>
            <div class="mb-3">
                <label for="cognome" class="form-label">Cognome</label>
                <input type="text" class="form-control" id="cognome" required>
            </div>
            <div class="mb-3">
                <label for="telefono" class="form-label">Telefono</label>
                <input type="tel" class="form-control" id="telefono">
            </div>
            <div class="mb-3">
                <label for="email" class="form-label">Email</label>
                <input type="email" class="form-control" id="email" required>
            </div>
            <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input type="password" class="form-control" id="password" required>
            </div>
            <button type="submit" class="btn btn-primary">Registrati</button>
        </form>
    `;
    document.getElementById('content').innerHTML = html;
    document.getElementById('registrationForm').addEventListener('submit', handleRegistration);
}

async function handleRegistration(event) {
    event.preventDefault();
    const formData = {
        nome: document.getElementById('nome').value,
        cognome: document.getElementById('cognome').value,
        telefono: document.getElementById('telefono').value,
        email: document.getElementById('email').value,
        password: document.getElementById('password').value
    };
    try {
        await apiCall('/registrazione', 'POST', formData);
        alert('Registrazione effettuata con successo. Effettua il login.');
        window.location.hash = '#login';
    } catch (error) {
        console.error('Registration failed:', error);
        alert('Registrazione fallita. Riprova.');
    }
}

async function renderProdotto(id) {
    try {
        const data = await apiCall(`/prodotto/${id}`);
        const html = `
            <h1>${data.prodotto.nome_prodotto}</h1>
            <img src="${data.prodotto.image_url}" alt="${data.prodotto.nome_prodotto}" class="img-fluid mb-3">
            <p>Quantità disponibile: ${data.quantita_disponibile} ${data.unita_misura}</p>
            <p>Prezzo: €${data.prezzo}</p>
            <form id="prenotaForm">
                <div class="mb-3">
                    <label for="quantita" class="form-label">Quantità</label>
                    <input type="number" class="form-control" id="quantita" min="1" max="${data.quantita_disponibile}" required>
                </div>
                <button type="submit" class="btn btn-primary">Prenota</button>
            </form>
        `;
        document.getElementById('content').innerHTML = html;
        document.getElementById('prenotaForm').addEventListener('submit', (event) => handlePrenotazione(event, id));
    } catch (error) {
        console.error('Error:', error);
    }
}

async function handlePrenotazione(event, prodottoId) {
    event.preventDefault();
    const quantita = document.getElementById('quantita').value;
    try {
        await apiCall(`/prodotto/${prodottoId}`, 'POST', { quantita });
        alert('Prenotazione effettuata con successo');
        window.location.hash = '#carrello';
    } catch (error) {
        console.error('Prenotazione failed:', error);
        alert('Prenotazione fallita. Riprova.');
    }
}

async function renderCarrello() {
    try {
        const data = await apiCall('/carrello');
        let html = '<h1>Carrello</h1>';
        if (data.prenotazioni.length === 0) {
            html += '<p>Il tuo carrello è vuoto.</p>';
        } else {
            html += '<ul class="list-group">';
            data.prenotazioni.forEach(prenotazione => {
                html += `
                    <li class="list-group-item d-flex justify-content-between align-items-center">
                        ${prenotazione.lotto.prodotto.nome_prodotto} - Quantità: ${prenotazione.qta}
                        <div>
                            <button class="btn btn-sm btn-danger" onclick="rimuoviPrenotazione(${prenotazione.id})">Rimuovi</button>
                        </div>
                    </li>
                `;
            });
            html += '</ul>';
            html += `<p class="mt-3">Totale: €${data.totale}</p>`;
        }
        document.getElementById('content').innerHTML = html;
    } catch (error) {
        console.error('Error:', error);
    }
}

async function rimuoviPrenotazione(prenotazioneId) {
    try {
        await apiCall('/carrello', 'POST', { prenotazione_id: prenotazioneId, delete: true });
        renderCarrello();
    } catch (error) {
        console.error('Error removing prenotazione:', error);
        alert('Errore durante la rimozione della prenotazione. Riprova.');
    }
}

// Add other render functions (renderNuovoProduttore, renderNuovoProdotto, renderNuovoLotto, renderGestisciUtenti) here...

function renderNotFound() {
    document.getElementById('content').innerHTML = '<h1>404 - Page Not Found</h1>';
}

// Event listeners
window.addEventListener('hashchange', router);
window.addEventListener('load', router);

// Check login status on page load
window.addEventListener('load', async () => {
    try {
        await apiCall('/');
        updateNavigation(true);
    } catch (error) {
        updateNavigation(false);
    }
});