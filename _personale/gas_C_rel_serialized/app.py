from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
from models import User, Lotto, Prenotazione, Prodotto, Produttore, db
from populate_db import init_db
from settings import DATABASE_PATH

app = Flask(__name__)

app.config.update(
    SECRET_KEY='my_very_secret_key123',
    SQLALCHEMY_DATABASE_URI='sqlite:///'+DATABASE_PATH,
    # SQLALCHEMY_TRACK_MODIFICATIONS=False,
    # DEBUG=True
)

db.init_app(app)

# Mostra la pagina che deve elencare i lotti disponibili
@app.route('/')
def home():
    return render_template('index.html')

# Mostra la pagina che deve elencare le prenotazioni dell'utente
@app.route('/prenotazioni')
def prenotazioni():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    else:
        return render_template('prenotazioni.html')

# Restituisce i dati dei lotti
@app.route('/api/dati_lotti')
def get_dati_lotti():
    # Esegui la query per ottenere tutti i lotti in ordine di data
    lotti = Lotto.query.order_by(Lotto.data_consegna).all()
    lotti_data = []
    for lotto in lotti:  # Model objects
        lotti_data.append(lotto.to_dict())
    
    return jsonify(lotti_data)


# Restituisce i dati delle prenotazioni degli utenti
@app.route('/api/dati_prenotazioni')
def get_dati_prenotazioni():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    else:
        pass
    
    # Così è semplice, ma non sono ordinati per data del lotto:
    # prenot_user = Prenotazione.query.filter_by(user_id=session['user_id']).all()

    # Se facciamo una query semplice e diretta, non possiamo ordinare per
    # data_consegna del lotto, perché non abbiamo il campo 'data_consegna'
    # del lotto!
    # prenot_user_ord = Prenotazione.query \
    #     .filter_by(user_id=session['user_id']) \
    #     .order_by('???') \
    #     .all()

    # Dobbiamo quindi fare un join con la tabella Lotto per poter
    # ordinare per data_consegna:
    prenot_user_ord = (Prenotazione.query
        .filter_by(user_id=session['user_id'])
        .join(Lotto, Prenotazione.lotto_id == Lotto.id)
        .order_by(Lotto.data_consegna)
        .all()
    )

    # Se preferite, potete dividere la query in due passaggi:
    # prenotazioni_user = Prenotazione.query.filter_by(user_id=session['user_id'])
    # prenot_user_ord = prenotazioni_user.join(Lotto).order_by(Lotto.data_consegna).all()

    # Oppure, possiamo evitare applicare il filtraro, sfruttando la relationship
    # tra Utente e Prenotazione a cui però va impostato l'argomento lazy='dynamic':
    # utente = db.session.get(User, session['user_id'])
    # prenot_user_ord = utente.prenotazioni.join(Lotto).order_by(Lotto.data_consegna).all()

    print(prenot_user_ord)

    prenotazioni_data = []
    for prenot in prenot_user_ord:
        prenotazioni_data.append(prenot.to_dict())

    return jsonify(prenotazioni_data)


# Mostra il lotto
@app.route('/lotto/<int:lotto_id>', methods=['GET'])
def mostra_lotto(lotto_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    else:
        pass

    lotto = db.session.get(Lotto, lotto_id)
    prenotazione_esistente = Prenotazione.query.filter_by(lotto_id=lotto_id, user_id=session['user_id']).first()
    if prenotazione_esistente:
        flash('Hai già una prenotazione per questo lotto. Se vuoi, puoi modificare '
              'la prenotazione esistente.', 'primary'
        )
        return redirect(url_for('mostra_prenotazione', prenotazione_id=prenotazione_esistente.id))
    else:
        return render_template('lotto.html', lotto=lotto)


# Crea una nuova prenotazione a partire da un lotto
@app.route('/lotto/<int:lotto_id>', methods=['POST'])
def prenota_lotto(lotto_id):
    if 'user_id' not in session:
        flash('Devi fare il login per effettuare una prenotazione.', 'warning')
        return redirect(url_for('login'))
    else:
        pass

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

    quantita = int(request.form.get('quantita'))  # ATTENZIONE: sarebbe da gestire meglio
                                                  # con un try/except per evitare errori
    lotto = db.session.get(Lotto, lotto_id)

    if quantita <= 0:
        flash('Quantità non valida. Inserire un numero maggiore di 0.', 'danger')
        return redirect(url_for('mostra_lotto', lotto_id=lotto_id))
    else:
        pass

    qta_disponibile = lotto.get_qta_disponibile()

    if quantita > qta_disponibile:
        flash('La quantità richiesta supera quella disponibile.', 'danger')
        return redirect(url_for('mostra_lotto', lotto_id=lotto_id))
    else:
        pass

    prenotazione = Prenotazione(user_id=session['user_id'], lotto_id=lotto_id, qta=quantita)
    db.session.add(prenotazione)
    db.session.commit()
    flash(f'Prenotazione di {quantita} {lotto.qta_unita_misura} di '
          f'"{lotto.prodotto.nome}" effettuata con successo!', 'success')

    return redirect(url_for('prenotazioni', lotto_id=lotto_id))


# Mostra prenotazione esistente
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

    if prenotazione.user_id != session['user_id']:
        flash('Non sei autorizzato a visualizzare questa prenotazione.', 'danger')
        return redirect(url_for('prenotazioni'))

    return render_template('prenotazione.html', prenotazione=prenotazione)

# Modifica prenotazione esistente
@app.route('/prenotazione/<int:prenotazione_id>', methods=['POST'])
def modifica_prenotazione(prenotazione_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    prenotazione = db.session.get(Prenotazione, prenotazione_id)

    if not prenotazione:
        flash('Prenotazione non trovata.', 'danger')
        return redirect(url_for('prenotazioni'))
    else:
        pass

    if prenotazione.user_id != session['user_id']:
        flash('Non sei autorizzato a modificare questa prenotazione.', 'danger')
        return redirect(url_for('prenotazioni'))
    else:
        pass

    azione = request.form.get('azione')

    if azione == 'aggiorna':
        quantita = int(request.form.get('quantita'))  # ATTENZIONE: sarebbe da gestire meglio
                                                      # con un try/except per evitare errori
        lotto = prenotazione.lotto

        if quantita <= 0:
            flash('Quantità non valida. Inserire un numero maggiore di 0.', 'danger')
            return redirect(url_for('mostra_prenotazione', prenotazione_id=prenotazione_id))

        qta_disponibile = lotto.get_qta_disponibile()

        if quantita > qta_disponibile + prenotazione.qta:
            flash('La quantità richiesta supera quella disponibile.', 'danger')
            return redirect(url_for('mostra_prenotazione', prenotazione_id=prenotazione_id))

        prenotazione.qta = quantita
        db.session.commit()
        flash(f'Prenotazione di "{lotto.prodotto.nome}" aggiornata a {quantita} {lotto.qta_unita_misura}.', 'success')

    elif azione == 'elimina':
        db.session.delete(prenotazione)
        db.session.commit()
        flash('Prenotazione eliminata con successo.', 'warning')

    else:
        flash('Azione non implementata.', 'danger')

    return redirect(url_for('prenotazioni'))


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


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)
