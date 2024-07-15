#from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
#from models import User, Lotto, Prenotazione, Prodotto, Produttore, db
# from populate_db import init_db
#from settings import DATABASE_PATH

#app = Flask(__name__)  

#app.config.update(      

#    SECRET_KEY='my_very_secret_key123', 

#    SQLALCHEMY_DATABASE_URI='sqlite:///'+DATABASE_PATH,    

#        )
#@app.route('/') 

#def home(): 
#    return render_template('login.html')

#@app.route('/eventi')

#def prenotazioni():
#    if 'utente_id' not in session: 
         
#        flash('Devi efettuare login', 'primary')

#        return redirect(url_for('login')) 
    
#    else:   
#        return render_template('eventi.html')


from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import locale
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_very_secret_key123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db'
db = SQLAlchemy(app)

# Definisci i modelli (Utente, Prenotazione, Replica, Evento, Locale) qui...

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/eventi')
def eventi():
    if 'utente_id' not in session:
        flash('Devi effettuare il login', 'primary')
        return redirect(url_for('login'))
    # Ottieni gli eventi e i posti disponibili dal database
    # Mostra gli eventi utilizzando template Jinja2
    return render_template('eventi.html', eventi=Event.query.all())

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

# Altre route per la gestione delle prenotazioni, login, ecc.

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)