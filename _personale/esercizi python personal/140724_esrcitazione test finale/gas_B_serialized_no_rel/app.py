from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
from models import User, Lotto, Prenotazione, Prodotto, Produttore, db
from populate_db import init_db
from settings import DATABASE_PATH

app = Flask(__name__)   #creando un’istanza dell’app Flask 

app.config.update(      ##Configuri l’URI del database SQLAlchemy 
        # per utilizzare un database SQLite situato nel percorso specificato
    SECRET_KEY='my_very_secret_key123', #  viene utilizzata per la gestione delle sessioni 
        #e altre funzionalità legate alla sicurezza.
    SQLALCHEMY_DATABASE_URI='sqlite:///'+DATABASE_PATH,     #Configuri l’URI del database SQLAlchemy 
        # per utilizzare un database SQLite situato nel percorso specificato

    
)

db.init_app(app)
    #è una riga di codice comune utilizzata nelle applicazioni Flask per inizializzare 
    # un’estensione del database (come SQLAlchemy) con l’istanza dell’app Flask

# Mostra la pagina che deve elencare i lotti disponibili
@app.route('/') #Quando un utente visita l’URL principale (la radice /), 
    # l’app risponderà con il contenuto definito nella funzione associata.
def home(): #Quando un utente visita la homepage, questa funzione verrà eseguita
    return render_template('index.html')    #Questa riga restituisce il contenuto della pagina HTML definita nel file index.html. 
    #La funzione render_template() carica il template HTML associato alla route.

# Mostra la pagina che deve elencare le prenotazioni dell'utente
@app.route('/prenotazioni') #Questa riga di codice crea una route per l’URL /prenotazioni. Quando un utente visita questo URL, 
    # l’app risponderà con il contenuto definito nella funzione associata.
def prenotazioni(): #Questa è la definizione della funzione prenotazioni().
        # Quando un utente visita l’URL /prenotazioni, questa funzione verrà eseguita.
    if 'user_id' not in session:    
        return redirect(url_for('login'))   #Questa riga verifica se la chiave 'user_id' è presente nella sessione dell’utente. Se non è presente (cioè l’utente non è autenticato),
            # reindirizza l’utente alla pagina di login utilizzando redirect(url_for('login')).

    else:   
        return render_template('prenotazioni.html') # Se la chiave 'user_id' è presente nella sessione (cioè l’utente è autenticato), viene restituito il contenuto 
            #della pagina HTML definita nel file prenotazioni.html utilizzando render_template().

# Restituisce i dati dei lotti
@app.route('/api/dati_lotti')
def get_dati_lotti():
    # Esegui la query per ottenere tutti i lotti in ordine di data
    # lotti = Lotto.query.order_by(Lotto.data_consegna).all()

    lotti = db.session.query(Lotto, Prodotto, Produttore) \
        .join(Prodotto, Lotto.prodotto_id == Prodotto.id) \
        .join(Produttore, Prodotto.produttore_id == Produttore.id) \
        .order_by(Lotto.data_consegna) \
        .all()
    
        # db.session.query(Lotto, Prodotto, Produttore): Questa parte del codice crea una query che seleziona dati da tre tabelle: Lotto, Prodotto e Produttore. Stiamo cercando di ottenere informazioni da queste tabelle.
    # .join(Prodotto, Lotto.prodotto_id == Prodotto.id): Qui stiamo eseguendo una join tra la tabella Lotto e la tabella Prodotto. La condizione di join è che l’ID del prodotto nel lotto (Lotto.prodotto_id) corrisponda all’ID del prodotto (Prodotto.id).
    # .join(Produttore, Prodotto.produttore_id == Produttore.id): Stiamo eseguendo un’altra join, questa volta tra la tabella Prodotto e la tabella Produttore. La condizione di join è che l’ID del produttore nel prodotto (Prodotto.produttore_id) corrisponda all’ID del produttore (Produttore.id).
    # .order_by(Lotto.data_consegna): Ordiniamo i risultati in base alla colonna data_consegna nella tabella Lotto. In altre parole, vogliamo i lotti ordinati per data di consegna.
    # .all(): Infine, otteniamo tutti i risultati della query come una lista di oggetti. Ogni oggetto rappresenta una combinazione di dati da tutte e tre le tabelle (lotto, prodotto e produttore).

    lotti_data = []
    for lotto in lotti:  # Model objects
        dict_lotto = lotto[0].to_dict()
        dict_lotto['prodotto'] = lotto[1].to_dict()
        dict_lotto['prodotto']['produttore'] = lotto[2].to_dict()   
        lotti_data.append(dict_lotto)
    return jsonify(lotti_data)

        #lotti_data = []: Questa riga inizializza una lista vuota chiamata lotti_data. Verrà utilizzata per memorizzare dizionari contenenti informazioni sui lotti.
    # for lotto in lotti:: Questo ciclo itera su ciascun elemento nella collezione lotti. Ogni lotto rappresenta una combinazione di dati dalle tabelle Lotto, Prodotto e Produttore.
    # dict_lotto = lotto[0].to_dict(): Qui estraiamo il primo elemento dal lotto (che corrisponde all’oggetto modello Lotto) e lo convertiamo in un dizionario utilizzando il metodo .to_dict(). Questo dizionario contiene informazioni sul lotto.
    # dict_lotto['prodotto'] = lotto[1].to_dict(): Aggiungiamo al dizionario dict_lotto un altro dizionario chiamato 'prodotto', ottenuto dal secondo elemento del lotto (che rappresenta il modello Prodotto).
    # dict_lotto['prodotto']['produttore'] = lotto[2].to_dict(): Infine, aggiungiamo al dizionario del prodotto un altro dizionario chiamato 'produttore', ottenuto dal terzo elemento del lotto (che rappresenta il modello Produttore).
    # lotti_data.append(dict_lotto): Aggiungiamo il dizionario dict_lotto alla lista lotti_data.
    # return jsonify(lotti_data): Infine, restituiamo i dati dei lotti come risposta in formato JSON utilizzando la funzione jsonify().


# Restituisce i dati delle prenotazioni degli utenti
@app.route('/api/dati_prenotazioni')
def get_dati_prenotazioni():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    else:
        pass
    
    prenotazioni = db.session.query(Prenotazione, Lotto, Prodotto, Produttore) \
        .join(Lotto, Prenotazione.lotto_id == Lotto.id) \
        .join(Prodotto, Lotto.prodotto_id == Prodotto.id) \
        .join(Produttore, Prodotto.produttore_id == Produttore.id) \
        .filter(Prenotazione.user_id == session['user_id']) \
        .order_by(Lotto.data_consegna) \
        .all()
            # Nel corpo della funzione, stai eseguendo una query al database utilizzando SQLAlchemy.
        #  La query recupera i dati relativi alle prenotazioni, lotti, prodotti e produttori, unendoli in base alle relazioni
        #  specificate. I risultati vengono filtrati per l’ID dell’utente attualmente autenticato (session['user_id']) e ordinati per data di consegna del lotto.
    print(prenotazioni)

    prenotazioni_data = []
    for prenot in prenotazioni:
        # prenotazioni_data.append(prenot.to_dict())
        dict_prenot = prenot[0].to_dict()   # Qui stiamo estrarre il primo elemento dal prenot 
            # (che rappresenta l’oggetto modello Prenotazione) e convertirlo in un dizionario utilizzando il metodo .to_dict().
            # Questo dizionario conterrà informazioni sulla prenotazione.
        dict_prenot['lotto'] = prenot[1].to_dict()# Aggiungiamo al dizionario dict_prenot un altro dizionario chiamato 'lotto',
            # ottenuto dal secondo elemento del prenot (che rappresenta il modello Lotto)
        dict_prenot['lotto']['prodotto'] = prenot[2].to_dict()  # Continuiamo ad aggiungere informazioni al dizionario del lotto. Qui stiamo includendo un altro
            # dizionario chiamato 'prodotto', ottenuto dal terzo elemento del prenot (che rappresenta il modello Prodotto).
        dict_prenot['lotto']['prodotto']['produttore'] = prenot[3].to_dict()    # Infine, aggiungiamo al dizionario del prodotto un altro dizionario chiamato 
            # 'produttore', ottenuto dal quarto elemento del prenot (che rappresenta il modello Produttore).
        prenotazioni_data.append(dict_prenot)   # Aggiungiamo il dizionario dict_prenot alla lista prenotazioni_data.


    return jsonify(prenotazioni_data)   #  I dati delle prenotazioni sono stati convertiti in formato JSON e restituiti come risposta. 


# Mostra il lotto
@app.route('/lotto/<int:lotto_id>', methods=['GET'])    # Questa riga di codice crea una route dinamica per l’URL /lotto/<lotto_id>
    # L’ID del lotto viene passato come parametro nell’URL. Quando un utente visita un URL come /lotto/123, 
    # l’app risponderà con il contenuto definito nella funzione associata.
def mostra_lotto(lotto_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))   # Se la chiave 'user_id' non è presente nella sessione (cioè l’utente non è loggato), 
            # l’app reindirizza l’utente alla pagina di login utilizzando redirect(url_for('login')).
    else:
        pass

    lotto = db.session.get(Lotto, lotto_id) # Qui stiamo cercando di ottenere il lotto con l’ID specificato. db.session.get() 
            # restituisce l’oggetto modello Lotto corrispondente all’ID fornito.
    prenotazione_esistente = Prenotazione.query.filter_by(lotto_id=lotto_id, user_id=session['user_id']).first()    # Qui stiamo cercando 
            # una prenotazione con l’ID del lotto e l’ID dell’utente corrispondenti. 
    if prenotazione_esistente:
        flash('Hai già una prenotazione per questo lotto. Se vuoi, puoi modificare '
              'la prenotazione esistente.', 'primary'
        )
        return redirect(url_for('mostra_prenotazione', prenotazione_id=prenotazione_esistente.id))  # Se esiste una prenotazione, 
            # mostriamo un messaggio di avviso e reindirizziamo l’utente alla pagina di visualizzazione della prenotazione esistente.
    else:
        return render_template('lotto.html', lotto=lotto)   # In caso contrario, mostriamo 
            # la pagina del lotto utilizzando render_template('lotto.html', lotto=lotto).


# Crea una nuova prenotazione a partire da un lotto
@app.route('/lotto/<int:lotto_id>', methods=['POST'])
def prenota_lotto(lotto_id):
    if 'user_id' not in session:
        flash('Devi fare il login per effettuare una prenotazione.', 'warning')
        return redirect(url_for('login'))
    else:
        pass
        # Se l’utente non è loggato (cioè 'user_id' non è presente nella sessione),
        #  viene mostrato un messaggio di avviso con la classe 'warning' e l’utente viene reindirizzato alla pagina di login.
        # Altrimenti, il codice prosegue.

    # Controllo di sicurezza per evitare di duplicare prenotazioni il che solleverebbe
    # un errore dato che abbiamo impostato un constraint univoco su (lotto_id, user_id)
    # a livello di DBMS.
    prenotazione_esistente = Prenotazione.query.filter_by(lotto_id=lotto_id, user_id=session['user_id']).first()
    if prenotazione_esistente:
        flash('Hai già una prenotazione per questo lotto. Se vuoi, puoi modificare '
              'la prenotazione esistente.', 'primary'
        )
        return redirect(url_for('mostra_prenotazione', prenotazione_id=prenotazione_esistente.id))
    else:
        pass
            # Viene verificato se l’utente ha già una prenotazione per il lotto specificato.
                # Se esiste una prenotazione, viene mostrato un messaggio con la classe 'primary' indicando che l’utente 
                # ha già una prenotazione per quel lotto e viene reindirizzato alla pagina di visualizzazione della prenotazione esistente.

    quantita = int(request.form.get('quantita'))  # ATTENZIONE: sarebbe da gestire meglio
                                                  # con un try/except per evitare errori
            # La quantità richiesta viene estratta dalla richiesta POST (request.form.get('quantita')).
    lotto = db.session.get(Lotto, lotto_id)

    if quantita <= 0:
        flash('Quantità non valida. Inserire un numero maggiore di 0.', 'danger')
        return redirect(url_for('mostra_lotto', lotto_id=lotto_id))
    else:
        pass

            # Si verifica se la quantità è un numero positivo (maggiore di 0). In caso contrario,
            #  viene mostrato un messaggio di errore con la classe 'danger' e l’utente viene reindirizzato alla pagina del lotto.
            # Se la quantità è valida, il codice prosegue.

    qta_disponibile = lotto.get_qta_disponibile()   # Si ottiene la quantità disponibile per il 
            # lotto specificato (qta_disponibile = lotto.get_qta_disponibile()).

    if quantita > qta_disponibile:
        flash('La quantità richiesta supera quella disponibile.', 'danger')
        return redirect(url_for('mostra_lotto', lotto_id=lotto_id))
    else:
        pass
            # Se la quantità richiesta supera quella disponibile, viene mostrato un messaggio di errore con la classe 'danger' e l’utente viene reindirizzato alla pagina del lotto.
            # Altrimenti, il codice prosegue.
            
    prenotazione = Prenotazione(user_id=session['user_id'], lotto_id=lotto_id, qta=quantita)
            # Viene creata una nuova istanza di Prenotazione con l’ID dell’utente e l’ID del lotto.
    db.session.add(prenotazione)
    db.session.commit()
    flash(f'Prenotazione di {quantita} {lotto.qta_unita_misura} di '
          f'"{lotto.prodotto.nome}" effettuata con successo!', 'success')
            # La prenotazione viene aggiunta alla sessione e il commit viene effettuato nel database.

    return redirect(url_for('prenotazioni', lotto_id=lotto_id))
        # Viene mostrato un messaggio di successo con la classe 'success' indicando che 
        # la prenotazione è stata effettuata correttamente.


# Mostra prenotazione esistente
@app.route('/prenotazione/<int:prenotazione_id>', methods=['GET']) 
        # codice definisce una route in Flask per visualizzare i dettagli di una prenotazione.
def mostra_prenotazione(prenotazione_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))   # Verifica se l’utente è autenticato (cioè se 'user_id' è presente nella sessione).
    else:
        pass
            # Se l’utente non è autenticato, viene reindirizzato alla pagina di login.
                # Altrimenti, il codice prosegue.

    prenotazione = db.session.get(Prenotazione, prenotazione_id)
            # Ottiene l’oggetto Prenotazione corrispondente all’ID specificato (prenotazione_id).
    if not prenotazione:
        flash('Prenotazione non trovata.', 'danger')
        return redirect(url_for('prenotazioni'))
    else:
        pass
            # Se la prenotazione non esiste, viene mostrato un messaggio di errore con la classe 
            # 'danger' e l’utente viene reindirizzato alla pagina delle prenotazioni.
            # Altrimenti, il codice prosegue.


    if prenotazione.user_id != session['user_id']:      #Verifica se l’utente è autorizzato a visualizzare questa prenotazione.
        flash('Non sei autorizzato a visualizzare questa prenotazione.', 'danger')
        return redirect(url_for('prenotazioni'))

    return render_template('prenotazione.html', prenotazione=prenotazione)      
        # Se l’utente non è l’autore della prenotazione, viene mostrato un messaggio di errore con la classe 'danger' 
        # e l’utente viene reindirizzato alla pagina delle prenotazioni.
        # Altrimenti, il codice prosegue.

# Modifica prenotazione esistente
@app.route('/prenotazione/<int:prenotazione_id>', methods=['POST']) 
        # codice definisce una route in Flask per modificare una prenotazione esistente
def modifica_prenotazione(prenotazione_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
        # La prima riga verifica se l’ID dell’utente ('user_id') è presente nella sessione.
        # Se l’utente non è autenticato (cioè l’ID non è presente), viene reindirizzato alla 
        # pagina di login utilizzando redirect(url_for('login')).
        # In caso contrario, il codice prosegue.
    
    prenotazione = db.session.get(Prenotazione, prenotazione_id)

    if not prenotazione:
        flash('Prenotazione non trovata.', 'danger')
        return redirect(url_for('prenotazioni'))
            # La riga successiva utilizza il metodo get() della sessione del database 
            # (db.session.get(Prenotazione, prenotazione_id)) per cercare un oggetto Prenotazione con l’ID specificato 
            # (prenotazione_id).
            # Se la prenotazione non esiste (ovvero prenotazione è None), viene mostrato 
            # un messaggio di errore con la classe 'danger' e l’utente viene reindirizzato alla pagina delle prenotazioni.
            # Altrimenti, il codice prosegue.
    else:
        pass
            # Verifica se l’utente è autenticato (cioè se 'user_id' è presente nella sessione).
            # Se l’utente non è autenticato, viene reindirizzato alla pagina di login.
            # Altrimenti, il codice prosegue.

    if prenotazione.user_id != session['user_id']:
        flash('Non sei autorizzato a modificare questa prenotazione.', 'danger')
        return redirect(url_for('prenotazioni'))
    else:
        pass

            # Ottiene l’oggetto Prenotazione corrispondente all’ID specificato (prenotazione_id).            
            # Se la prenotazione non esiste, viene mostrato un messaggio di errore con la classe 
            # 'danger' e l’utente viene reindirizzato alla pagina delle prenotazioni.
            # Altrimenti, il codice prosegue.

    azione = request.form.get('azione') # La riga azione = request.form.get('azione') recupera l’azione specificata dall’utente 
            # (sia “aggiorna” per l’aggiornamento che “elimina” per la cancellazione).

    if azione == 'aggiorna':    # Se l’azione è “aggiorna”:
        quantita = int(request.form.get('quantita'))  # ATTENZIONE: sarebbe da gestire meglio
                                                      # con un try/except per evitare errori
                # # Estrae la quantità richiesta dai dati del modulo.
        lotto = prenotazione.lotto

        if quantita <= 0:    # Verifica che la quantità sia valida (maggiore di 0).
            flash('Quantità non valida. Inserire un numero maggiore di 0.', 'danger')
            return redirect(url_for('mostra_prenotazione', prenotazione_id=prenotazione_id))

        qta_disponibile = lotto.get_qta_disponibile()

        if quantita > qta_disponibile + prenotazione.qta:
            flash('La quantità richiesta supera quella disponibile.', 'danger')
            return redirect(url_for('mostra_prenotazione', prenotazione_id=prenotazione_id))
            
            
            # Recupera il lotto associato.
            # Calcola la quantità disponibile (qta_disponibile).
            # Assicura che la quantità richiesta non superi la quantità disponibile più la quantità prenotata esistente.
            # Aggiorna la quantità della prenotazione nel database.
            
        prenotazione.qta = quantita
        db.session.commit()
        flash(f'Prenotazione di "{lotto.prodotto.nome}" aggiornata a {quantita} {lotto.qta_unita_misura}.', 'success')
            # # Mostra un messaggio di successo indicando la quantità aggiornata.
    elif azione == 'elimina':
        db.session.delete(prenotazione)
        db.session.commit()
        flash('Prenotazione eliminata con successo.', 'warning')

        # Se l’azione è “elimina”:
        # Elimina la prenotazione dal database.
        # Mostra un messaggio di avviso confermando l’eliminazione.

    else:
        flash('Azione non implementata.', 'danger')
            # Se l’azione non è né “aggiorna” né “elimina”, viene mostrato un 
            # messaggio di errore indicando che l’azione non è implementata.

    return redirect(url_for('prenotazioni'))
            # Infine, l’utente viene reindirizzato alla pagina delle prenotazioni.


@app.route('/login', methods=['GET', 'POST'])    # definisce una route in Flask per la pagina di login
         # La route gestisce sia richieste GET che POST.
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            session['user_id'] = user.id
            flash(f'Login riuscito. Benvenuto {user.nome}!', 'success')
            return redirect(url_for('prenotazioni'))
            # Se la richiesta è di tipo POST (ovvero l’utente ha inviato il modulo di login), 
            # il codice procede con il controllo delle credenziali.
        else:
            flash('Login non riuscito. Controlla email e password.', 'danger')

    return render_template('login.html')
    # Altrimenti, viene visualizzata la pagina di login.


@app.route('/logout')
def logout():
    session.pop('user_id', None)    # La riga session.pop('user_id', None) rimuove l’ID dell’utente dalla sessione.
    return redirect(url_for('login'))   # Dopo aver eseguito il logout, l’utente viene reindirizzato 
            # alla pagina di login utilizzando redirect(url_for('login')).


if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)
