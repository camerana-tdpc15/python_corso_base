
import locale
from flask import Flask,flash, redirect, render_template, jsonify, request, session, url_for
from models import Prenotazione, User, db, init_db, Lotto, Prodotto, Produttore
from settings import DATABASE_PATH

locale.setlocale(locale.LC_TIME, 'it_IT')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+DATABASE_PATH
app.config['SECRET_KEY'] = 'mysecretkey'

db.init_app(app)  # Inizializza l'istanza di SQLAlchemy con l'app Flask

# questo  mostra l'elenco dei lotti
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/prenotazioni')
def mostra_prenotazioni():
    return render_template('prenotazioni.html')



# restituisce i dati dei lotti disponibili in json
@app.route('/api/lotti', methods=['GET'])
def get_lotti():

    # Leggo i parametri passati in query string
    order = request.args.get('order', 'asc')

    if order == 'asc':
        lotti = Lotto.query.order_by(Lotto.data_consegna).all()
    elif order == 'desc':
        lotti = Lotto.query.order_by(Lotto.data_consegna.desc()).all()
    else:
        return 'Parametro order non valido. Utilizzare "asc" o "desc".'

    lotti_data = []
    for lotto in lotti:
        dict_lotto = lotto.to_dict()
        lotti_data.append(dict_lotto)

    return jsonify(lotti_data)


@app.route('/lotto/<int:id_lotto>', methods=["GET"])
def mostra_lotto(id_lotto):

    # @TODO: controllare che l'utente sia loggato
    # se l'utente non è loggato
    if 'user_id' not in session:

        # mi rindirizzi alla login
        return redirect(url_for('login'))

    else:
        # ottengo il record del lotto a partire dal suo id
        lotto = db.session.get(Lotto, id_lotto)

        if not lotto:
            return 'Lotto non trovato', 404
        
        # user = db.session.get(User,session['user_id'])
        # prenotazioni = user.rel_prenotazioni

        prenot_utente = Prenotazione.query.filter_by(
            user_id=session['user_id'],
            lotto_id=id_lotto
        ).first()

        # se l'utente ha delle prenotazioni SU QUESTO SPECIFICO LOTTO
        if prenot_utente:
            return redirect(url_for('aggiorna_prenotazione.html', id_prenotazione=prenot_utente.id))

        # se l'utente NON ha delle prenotazioni  SU QUESTO SPECIFICO LOTTO
        else:
            return render_template('lotto.html', lotto=lotto)
    return lotto.rel_prodotto.nome_prodotto


@app.route('/lotto/<int:id_lotto>', methods=["POST"])
def nuova_prenotazione(id_lotto):
     # se l'utente non è loggato
    if 'user_id' not in session:

        # mi rindirizzi alla login
        return 'Non sei loggato, 401'
    else:
        pass
    quantita = int(request.form.get('quantita'))
    

    #TODO Verifica che la quantità sia:
    
    # maggiore o uguale a 1
    if quantita < 1 :
        flash("La quantità dev'essere maggiore di 0", "warning")
        return redirect(url_for('mostra_lotto', id_lotto=id_lotto))
    
    # minore o uguale alla qta_disponibile
    lotto=db.session.get(Lotto,id_lotto)

    if quantita > lotto.get_qta_disponibile():        
        flash("Hai prenotato di più della quantità disponibile", "warning")
        return redirect(url_for('mostra_lotto', id_lotto=id_lotto))

      

    new_prenotazione = Prenotazione(qta=quantita, lotto_id=id_lotto, user_id=session['user_id'])

    db.session.add(new_prenotazione)

    db.session.commit()

    flash('Prenotazione effettuata con successo', 'success')

    return redirect(url_for(mostra_prenotazioni))

@app.route('/prenotazione/<int:id_prenotazione>', methods=['GET'])
def aggiorna_prenotazione(id_prenotazione):
    ...

    return render_template('prenotazione.html')

@app.route('/api/prenotazioni', methods=['GET'])
def get_prenotazioni():
    prenotazioni = Prenotazione.query \
        .filter_by(user_id=session['user_id']) \
        .order_by(Prenotazione.data_consegna) \
            .all()
    
    # converto in dizionario 
    prenot_data = []
    for prenot in prenotazioni:
        dict_prenot = prenot.to_dict()
        prenot_data.append(dict_prenot)

    return jsonify(prenot_data)
   


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session['user_id'] = user.id
            # flash('Login riuscito!')
            return redirect(url_for('home'))
        else:
            # flash('Credenziali non valide!')
            return redirect(url_for('login'))
        
    elif request.method == 'GET':
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logout effettuato con successo!')
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)