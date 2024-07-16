import locale
from flask import Flask, flash, render_template, jsonify, request, session, redirect, url_for
from models import db, init_db, prenotazione, utente, replica, evento, locale
from settings import DATABASE_PATH





app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+DATABASE_PATH
app.config['SECRET_KEY'] = 'mysecretkey'

db.init_app(app)  # Inizializza l'istanza di SQLAlchemy con l'app Flask


@app.route('/')
def iniziale():
    return redirect(url_for('login'))

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/prenotazioni')
def pag_prenot():
    return render_template('Prenotazioni.html')

@app.route('/eventi')
def pag_eventi():
    return render_template('eventi.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # ATTENZIONE: Possiamo usare la password come parametro di ricerca
        #             perché l'abbiamo memorizzata in chiaro (e non come "hash")
        user = utente.query.filter_by(email=email, password=password).first()
        if user:
            session['utente_id'] = user.id
            # flash('Login riuscito!')
            return redirect(url_for('home'))
        else:
            # flash('Credenziali non valide!')
            return redirect(url_for('login'))
    
    elif request.method == 'GET':
        return render_template('login.html')
    




@app.route('/logout')
def logout():
    session.pop('utente_id', None)
    # flash('Logout effettuato con successo!')
    return redirect(url_for('home'))


# Restituisce i dati degli eventi disponibili in formato JSON
@app.route('/api/eventi', methods=['GET'])
def get_eventi():

    # Leggo i parametri passati in query string
    order = request.args.get('order', 'asc')

    if order == 'asc':
        repliche = replica.query.order_by(replica.data_ora).all()  
    elif order == 'desc':
        repliche = replica.query.order_by(replica.data_ora.desc()).all()
    else:
        return 'Parametro order non valido. Utilizzare "asc" o "desc".'

    repliche_data = []
    for replica in repliche:
        dict_replica = replica.to_dict()
        repliche_data.append(dict_replica)

    return jsonify(repliche_data) 


#restituisce i dati delle prenotazioni
@app.route('/api/prenotazioni', methods=['GET'])
def get_prenotazioni():
    
    prenotazioni_ = prenotazione.query \
        .filter_by(user_id=session['user_id']) \
        .join(replica, replica.id == prenotazione.replica_id) \
        .order_by(replica.data_ora) \
        .all()  

    prenot_data = []
    for prenot in prenotazioni_:
        dict_prenot = prenot.to_dict()
        prenot_data.append(dict_prenot)

    return jsonify(prenot_data)



# Mostra il form per la nuova prenotazione di un evento (GET)
@app.route('/replica/<int:id_replica>', methods=['GET'])
def mostra_replica(id_replica):
    # Controllare che l'utente sia loggato
    if 'utente_id' not in session:
        return redirect(url_for('login'))


    # Ottengo il record della replica a partire dal suo ID
    replica = db.session.get(replica, id_replica)
    if not replica:
        return 'evento non trovato!', 404

    # user = db.session.get(User, session['user_id'])
    # prenotazioni = user.rel_prenotazioni

    prenot_utente = prenotazione.query.filter_by(
        utente_id=session['utente_id'],
        replica_id=id_replica
    ).first()

    # Se l'utente ha delle prenotazioni su qusto specifico evento
    if prenot_utente:
        return redirect(url_for('mostra_prenotazione', prenotazione_id=prenot_utente.id))
    # Se l'utente non ha delle prenotazioni su qusto specifico evento
    else:
        return render_template('eventi.html', replica=replica)
    


    # Riceve i dati del form per la nuova prenotazione di un evento (POST)
@app.route('/evento/<int:id_>', methods=['POST'])
def nuova_prenotazione(id_prenotazione):
    # Controllare che l'utente sia loggato
    if 'utente_id' not in session:
        return 'Non sei autorizzato', 401

    quantita = int(request.form.get('quantita'))

    # Controllo che sia una quantità >= 1
    if quantita < 1:
        # @TODO: fix flask messages
        flash('La quantità deve essere mggiore di zero!', 'warning')
        return redirect(url_for('mostra_replica', id_prenotazione=id_prenotazione))
    

    # Controllo che la quantità sia minore o uguale alla qta disponibile
    prenotazione = db.session.get(prenotazione, id_prenotazione)
    if quantita > replica.get_qta_disponibile():
        flash('Hai prenotato di più della quantità disponibile.', 'warning')
        return redirect(url_for('mostra_replica', id_replica=id_prenotazione))

    new_prenotazione = prenotazione(qta=quantita, prenotazione_id=id_prenotazione, utente_id=session['utente_id'])
    db.session.add(new_prenotazione)
    db.session.commit()
    flash('Prenotazione effettuata con successo!', 'success')

    return redirect(url_for('mostra_prenotazioni'))


# Mostra il form per la modifica di una prenotazione esistente (GET)
@app.route('/prenotazione/<int:prenotazione_id>', methods=['GET'])
def mostra_prenotazione(prenotazione_id):
    if 'utente_id' not in session:
        return redirect(url_for('login'))
    else:
        pass

    prenotazione = db.session.get(prenotazione, prenotazione_id)

    if not prenotazione:
        flash('Prenotazione non trovata.', 'danger')
        return redirect(url_for('prenotazioni'))
    else:
        pass

    if prenotazione.utente_id != session['utente_id']:
        flash('Non sei autorizzato a visualizzare questa prenotazione.', 'danger')
        return redirect(url_for('prenotazioni'))

    return render_template('Prenotazioni.html', prenotazione=prenotazione)


# Riceve i dati del form per la modifica di una prenotazione esistente (POST)
@app.route('/prenotazione/<int:prenotazione_id>', methods=['POST'])
def modifica_prenotazione(prenotazione_id):
    if 'utente_id' not in session:
        return redirect(url_for('login'))
    
    prenotazione = db.session.get(prenotazione, prenotazione_id)

    if not prenotazione:
        flash('Prenotazione non trovata.', 'danger')
        return redirect(url_for('prenotazioni'))
    else:
        pass

    if prenotazione.utente_id != session['utente_id']:
        flash('Non sei autorizzato a modificare questa prenotazione.', 'danger')
        return redirect(url_for('prenotazioni'))
    else:
        pass

    azione = request.form.get('azione')

    if azione == 'aggiorna':
        quantita = int(request.form.get('quantita'))  # ATTENZIONE: sarebbe da gestire meglio
                                                      # con un try/except per evitare errori
        replica = prenotazione.rel_replica

        if quantita <= 0:
            flash('Quantità non valida. Inserire un numero maggiore di 0.', 'danger')
            return redirect(url_for('mostra_prenotazione', prenotazione_id=prenotazione_id))

        qta_disponibile = replica.get_qta_disponibile()

        if quantita > qta_disponibile + prenotazione.quantita:
            flash('La quantità richiesta supera quella disponibile.', 'danger')
            return redirect(url_for('mostra_prenotazione', prenotazione_id=prenotazione_id))

        prenotazione.quantita = quantita
        db.session.commit()
        flash(f'Prenotazione di "{replica.rel_evento.nome_evento}" aggiornata a {quantita}.', 'success')

    elif azione == 'elimina':
        db.session.delete(prenotazione)
        db.session.commit()
        flash('Prenotazione eliminata con successo.', 'warning')

    else:
        flash('Azione non implementata.', 'danger')

    return redirect(url_for('mostra_prenotazioni'))














if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)

