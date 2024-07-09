from flask import Flask, render_template, jsonify,request, session, redirect, url_for
from models import db, init_db,Lotto, Prodotto, Produttore, User, Prenotazione
from settings import DATABASE_PATH

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+DATABASE_PATH
app.config['SECRET_KEY'] = 'mysecretkey'

db.init_app(app)  # Inizializza l'istanza di SQLAlchemy con l'app Flask

@app.route('/')
def home():
    return render_template('home.html')


# @TODO: Qua ci vanno le routes
# ...

@app.route('/api/lotti',methods =['GET'])
def get_lotti():
    # lotti = Lotto.query.all()
    # lotti_data = []

    # for lotto in lotti:
    #     prodotto_id = lotto.prodotto_id
    #     prodotto = db.session.get(Prodotto,prodotto_id)
    #     produttore = db.session.get(Produttore, prodotto.produttore_id)
    #     data = {
    #         'id':lotto.id,
    #         'data_consegna':lotto.data_consegna,
    #         'get_prezzo_str':lotto.get_prezzo_str(),   
    #         ' get_qta_disponibile' : lotto.get_qta_disponibile(),
    #         'get_date':lotto.get_date(),
    #         'qta_unita_misura':lotto.qta_unita_misura, 
    #         'qta_lotto':lotto.qta_lotto,
    #         'prezzo_unitario':lotto.prezzo_unitario,
    #         'sospeso':lotto.sospeso,
    #         'prodotto':{
    #             'nome_prodotto': prodotto.nome_prodotto,
    #             'produttore':{'nome_produttore': produttore.nome_produttore}
    #             }
            
    #    }


    #     lotti_data.append(data)

    # return jsonify(lotti_data)
    lotti_data = []
    for lotto in lotti:
        dict_lotto = lotto.to_dict()
        lotti_data.append(dict_lotto)

    return jsonify(lotti_data)

@app.route('/lotto/<int:id_lotto>')
def mostra_lotto(id_lotto):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    lotto = db.session.get(Lotto, id_lotto)
    if not lotto:
        return'Lotto non trovato!', 404
    
    # user = db,session.get(User, session['user_id'])
    # prenotazioni = user.rel_prenotazioni

    prenot_utente = Prenotazione.query.filter_by(user_id = session['user_id'],
                                                 lotto_id = id_lotto)
    
    if prenot_utente: 
        return redirect('modifica_prenotazione.html')
    else:
        return render_template('nuova_prnotazione.html')


    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(email= email, password=password).first()
        if user:
            session['user_id'] = user.id
            # flash('Login riuscito!')
            return redirect(url_for('home.html'))
        else:
            # flash('Credenziali non valide!')
            return redirect(url_for('login'))
        
    elif request.method == 'GET':
        return redirect(url_for('login'))
    

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    # flash('Logout effettuato con successo!')
    return redirect(url_for('home'))


@app.route('/api/prenotazioni', method=['GET'])
def get_prenotazioni():
            # @TODO: controlare cho l'utente sia loggato
            # Ottengo il record del lotto a partire dal suo ID
     lotto = db.session.get(Lotto, id_lotto)


if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)