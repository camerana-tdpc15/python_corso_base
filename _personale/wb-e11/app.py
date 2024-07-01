from flask import Flask,request,session, render_template, flash, redirect, url_for
from settings import DATABASE
from models import init_db,db,lotti,users,prodotti,produttori,prenotazioni

# Inizializiamo la app
app = Flask(__name__)
# impostiamo tutto lo necsario per lavorare con  il database, il modo debug
#e anche creamo la chiave secreta per firmare i cookies dall'usuario
app.config.update(
    SECRET_KEY='my_very_secret_key_321',
    SQLALCHEMY_DATABASE_URI='sqlite:///'+DATABASE,
    DEBUG=True
)

# inizializiamo SQL ALCHEMY con l'app flask
db.init_app(app)

# Creamo la nostra route base
@app.route('/')
def index():
    return render_template('index.html')



 # Creamo la nostra route di login
@app.route('/login', methods=['GET','POST'])
def login():

    #Controliamo se il metodo ricevuto e post
    if request.method =='POST':
        
        # prend i datti ottenuti dal formData (dall form html) 
        rx_username = request.form.get('username')
        rx_password = request.form.get('contraseña')


        # Si fa una query per filtrare tra tutti utenti e scoprire se l'utente essite
        
        user =  users.query.filter_by(login=rx_username).firts()

        # Controlliamo se l'utente e la contraseña e correteta
        if user and user.password == rx_password:
            session['username'] = rx_username
            flash('Login avvenuto correttamente!','success')
            app.logger.info(f"L'utente{rx_username}  ha effettuato l'accesso.")
            return redirect(url_for('ecomerce'))

        else:
            #diversamente se nome utente e password non vengono riconosciuti mostriamo un msj
            flash('Username o Password nonm validi.', 'danger')
            # Loggiamo il tentativo di accesso fallito
            app.logger.warning(f"tentativo di accesso fallito per l'utente{rx_username}.")

    return render_template('login.html')



@app.route('/logout')
def logout():
    session.pop('Username', None)  # Implementiamo SESSION per togliere la variabile "utente" e chiudere la sesione
    flash('Logout effettuato correttamente,','warning')
    return redirect(url_for('home'))



@app.route('/lotti_prenotabili')
def lotti_prenotabili():
    if 'username' in session:
        ...



@app.route('/prenotazioni')
def prenotazioni():
    
    if 'username' in session:
        ...


@app.route('/prenotazioni_efetuatte')
def prenotazioni_efetuatte():
   
   if 'username' in session:
       ...





if __name__=='__main__':
    with app.app_context():
        init_db(app)
    app.run()