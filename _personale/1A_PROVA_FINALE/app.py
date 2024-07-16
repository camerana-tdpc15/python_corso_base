from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
from models import   db, init_db, Evento, User, Replica, Prenotazione

from settings import DATABASE_PATH



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DATABASE_PATH
app.config['SECRET_KEY'] = 'my_very_secret_key123'

db.init_app(app)


@app.route('/prova')
def prova():

    posti_disponibili = Replica.query.get(4).get_posti_disponibili()

    #evento = Evento.query.get(1)
    
    print (posti_disponibili)
    return('1')

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            session['user_id'] = user.id
            flash(f'Login riuscito. Benvenuto {user.nome}!', 'success')
            return redirect(url_for('prenotazioni'))
        else:
            flash('Login non riuscito. Controlla email e password.', 'danger')

    return render_template('login.html')

@app.route('/prenotazioni')
def prenotazioni():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    else:
        return render_template('prenotazioni.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/api/dati_eventi')
def get_dati_eventi():
    # Esegui la query per ottenere tutti i lotti in ordine di data
    eventi = Evento.query.all()
    dati_eventi = []
    for evento in eventi:  # Model objects
        dati_eventi.append()
        dati_eventi.append(evento.to_dict())

    
    return jsonify(dati_eventi)


@app.route('/api/dati_repliche')
def get_dati_repliche():
    # Esegui la query per ottenere tutti i lotti in ordine di data
    eventi = Replica.query.all()
    dati_eventi = []
    for evento in eventi:  # Model objects
        dati_eventi.append(evento.to_dict())
    
    return jsonify(dati_eventi)

@app.route('/replica/<int:replica_id>', methods=['GET'])
def mostra_replica(replica_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    else:
        pass

    replica = db.session.get(Replica, replica_id)
    prenotazione_esistente = Prenotazione.query.filter_by(replica_id=replica_id, utente_id=session['user_id']).first()
    if prenotazione_esistente:
        flash('Hai già una prenotazione per questo replica. Se vuoi, puoi modificare '
              'la prenotazione esistente.', 'primary'
        )
        return redirect(url_for('mostra_prenotazione', prenotazione_id=prenotazione_esistente.id))
    else:
        return render_template('replica.html', replica=replica)
    



@app.route('/prenotazione/<int:prenotazione_id>', methods=['GET'])
def mostra_prenotazione(prenotazione_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    else:
        pass

    prenotazione = db.session.get(Prenotazione, prenotazione_id)

    if not prenotazione:
        flash('Prenotazione non trovata.', 'danger')
        return redirect(url_for('prenotazioni'))
    else:
        pass

    if prenotazione.utente_id != session['user_id']:
        flash('Non sei autorizzato a visualizzare questa prenotazione.', 'danger')
        return redirect(url_for('prenotazioni'))

    return render_template('prenotazione.html', prenotazione=prenotazione)


# Crea una nuova prenotazione a partire da un lotto
@app.route('/replica/<int:replica_id>', methods=['POST'])
def prenota_replica(replica_id):
    if 'user_id' not in session:
        flash('Devi fare il login per effettuare una prenotazione.', 'warning')
        return redirect(url_for('login'))
    else:
        pass

    # Controllo di sicurezza per evitare di duplicare prenotazioni il che solleverebbe
    # un errore dato che abbiamo impostato un constraint univoco su (lotto_id, user_id)
    # a livello di DBMS.
    #TODO se c'è tempo inserire un unique constraints
    # prenotazione_esistente = Prenotazione.query.filter_by(lotto_id=lotto_id, user_id=session['user_id']).first()
    # if prenotazione_esistente:
    #     flash('Hai già una prenotazione per questo lotto. Se vuoi, puoi modificare '
    #           'la prenotazione esistente.', 'primary'
    #     )
    #     return redirect(url_for('mostra_prenotazione', prenotazione_id=prenotazione_esistente.id))
    # else:
    #     pass

    quantita = int(request.form.get('quantita'))  # ATTENZIONE: sarebbe da gestire meglio
                                                  # con un try/except per evitare errori
    replica = db.session.get(Replica, replica_id)

    if quantita <= 0:
        flash('Quantità non valida. Inserire un numero maggiore di 0.', 'danger')
        return redirect(url_for('mostra_lotto', replica_id=replica_id))
    else:
        pass

    qta_disponibile = replica.get_posti_disponibili()

    if quantita > qta_disponibile:
        flash('La quantità richiesta supera quella disponibile.', 'danger')
        return redirect(url_for('mostra_lotto', replica_id=replica_id))
    else:
        pass

    prenotazione = Prenotazione(utente_id=session['user_id'], replica_id=replica_id, quantita=quantita)
    db.session.add(prenotazione)
    db.session.commit()
    flash(f'Prenotazione di {quantita} per lo spettacolo '
          f'"{replica.evento.nome_evento}" effettuata con successo!', 'success')

    return redirect(url_for('prenotazioni', replica_id=replica_id))

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)