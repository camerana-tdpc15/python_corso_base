const form = document.getElementById('guestbook-form');
        const messageList = document.getElementById('message-list');

        form.addEventListener('submit', async (event) => {
            event.preventDefault();

            const name = form.querySelector('#name').value;
            const message = form.querySelector('#message').value;

            try {
                const response = await fetch('/submit', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ name, message })
                });

                if (response.ok) {
                    const newMessage = document.createElement('li');
                    newMessage.textContent = `${name} ha scritto: ${message}`;
                    messageList.appendChild(newMessage);

                    // Pulisci i campi del form
                    form.reset();
                } else {
                    console.error('Errore durante l\'invio del messaggio');
                }
            } catch (error) {
                console.error('Errore di rete:', error);
            }
        });