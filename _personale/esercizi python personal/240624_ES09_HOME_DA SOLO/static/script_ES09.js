
        async function inviaMessaggio() {
            const nome = document.getElementById('nome').value;
            const messaggio = document.getElementById('messaggio').value;

            try {
                const response = await fetch('/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    body: `nome=${nome}&messaggio=${messaggio}`
                });

                if (response.ok) {
                    // Aggiorna la lista dei messaggi
                    const messageList = document.getElementById('message-list');
                    const nuovoMessaggio = document.createElement('li');
                    nuovoMessaggio.textContent = `${nome}: ${messaggio}`;
                    messageList.appendChild(nuovoMessaggio);

                    // Pulisci i campi del form
                    document.getElementById('nome').value = '';
                    document.getElementById('messaggio').value = '';
                } else {
                    console.error('Errore durante l\'invio del messaggio');
                }
            } catch (error) {
                console.error('Errore di rete:', error);
            }
        }
   