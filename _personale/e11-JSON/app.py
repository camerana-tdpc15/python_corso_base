import locale
from flask import Flask, render_template, jsonify, request,session,flash,redirect,url_for
from models import db, init_db, Lotto, Prodotto, Produttore,User
from settings import DATABASE_PATH

locale.setlocale(locale.LC_TIME, 'it_IT')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+DATABASE_PATH
app.config['SECRET_KEY'] = 'mysecretkey'

db.init_app(app)  # Inizializza l'istanza di SQLAlchemy con l'app Flask

#Mostra l'elenco dei lotti disponibili
@app.route('/')
def home():

    if 'user_id' in session:
        user = db.session.query(User).get(session['user_id'])
        return render_template('home.html', user=user)
    else:
        return render_template('login.html')
    




# restituisce i datti dei lotti disponibili in formato JSON
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


@app.route('/lotto/<id_lotto>')
def mostra_lotto(id_lotto): #possiamo usare show_lotto
    # @TODO:  CONTROLLARE CHE L'UTENTE SIA LOGGATO
   # if 'user_id' in session:
    #    user = db.session.query(User).get(session['user_id'])
     #   return render_template('home.html', user=user)
    #else:
    #    return render_template('login.html')

    lotto = db.session.get(Lotto, id_lotto)

    return lotto.prodotto.nome_prodotto


@app.route('/api/prenotazioni', methods=['GET'])
def get_prenotazioni():
    ...


# @TODO: Implementare il login / logout

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session['user_id'] = user.id
            flash('Login riuscito!')
            return redirect(url_for('home'))
        else:
            flash('Credenziali non valide!')
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logout effettuato con successo!')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)