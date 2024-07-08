
from flask import Flask, redirect, render_template,jsonify, request, session, url_for
from models import Lotto, Prenotazione, Prodotto, Produttore, User, db, init_db
from settings import DATABASE_PATH
import locale

locale.setlocale(locale.LC_TIME, 'it_IT')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+DATABASE_PATH

db.init_app(app)  # Inizializza l'istanza di SQLAlchemy con l'app Flask

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/lotto/<int:id_lotto>')
def mostra_lotto (id_lotto):
    #    controllare che l utente sia loggato
    if 'user_id' not in session:
           return redirect(url_for('login'))

   
    #ottengo il record del lotto a partire dal suo id
    lotto= db.session.get(Lotto,id_lotto)

    if not lotto:
        return 'Lotto non trovato!', 404
    
    #user = db.session.get(User,session['user_id'])
    #prenotazioni= user.rel_prenotazioni


    prenot_utente = Prenotazione.query.filter_by(
        user_id = session ['user_id'],
        lotto_id = id_lotto
        )

    # se l'utente ha delle prenotazioni su un lotto specifico
    if prenot_utente:
        return render_template('modifica_prenotazione.html')

    # se l'utente non ha delle prenotazioni su un lotto specifico
    else:
        return render_template('nuova_prenotazione.html') 

#restituisce i dati dei lotti disponibili in formato json
@app.route('/api/lotti', methods= ['GET'])
def get_lotti():
    lotti = Lotto.query.all()
    lotti_data = []
    for lotto in lotti :
        dict_lotto=lotto.to_dict()
        lotti_data.append(dict_lotto)
        
     #   prodotto_id = lotto.prodotto_id
     #   prodotto = db.session.get(Prodotto, prodotto_id)
#
     #   produttore= db.session.get(Produttore, prodotto.produttore_id)
     #   data = {              
     #       'id':lotto.id,
     #       'data_consegna':lotto.data_consegna,
     #       'get_date':lotto.get_date(),
     #       'get_qta_disponibile':lotto.get_qta_disponibile(),
     #       'qta_unita_misura':lotto.qta_unita_misura,
     #       'qta_lotto':lotto.qta_lotto,
     #       'prezzo_unitario':lotto.get_prezzo_str(),
     #       'sospeso':lotto.sospeso,
     #       'prodotto':{
     #           'prodotto_nome':prodotto.nome_prodotto,               
     #           'produttore':{
     #               'produttore':produttore.nome_produttore               
     #           }
     #       }
     #   }
     #   lotti_data.append(data)

    return jsonify(lotti_data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session['user_id'] = user.id
            #flash('Login riuscito!')
            return redirect(url_for('guestbook'))
        else:
           # flash('Credenziali non valide!')
            return redirect(url_for('login'))
        
    elif request.method == 'GET':
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    #flash('Logout effettuato con successo!')
    return redirect(url_for('home'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

# @TODO: Qua ci vanno le routes
# ...

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)