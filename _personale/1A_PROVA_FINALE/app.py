from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
from models import   db, init_db, Evento, User

from settings import DATABASE_PATH



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DATABASE_PATH
app.config['SECRET_KEY'] = 'my_very_secret_key123'

db.init_app(app)

@app.route('/')
def home():

    evento = Evento.query.get(1)
    
    return (evento.nome_evento)


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

@app.route('/api/dati_eventi')
def get_dati_eventi():
    # Esegui la query per ottenere tutti i lotti in ordine di data
    eventi = Evento.query.all()
    dati_eventi = []
    for evento in eventi:  # Model objects
        dati_eventi.append(evento.to_dict())
    
    return jsonify(dati_eventi)

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)