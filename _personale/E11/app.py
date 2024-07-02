from flask import Flask, request, render_template, redirect, url_for, session, flash
from settings import DATABASE_PATH
from models import init_db, db,User
app = Flask(__name__)

app.config.update(
    SECRET_KEY='my_very_secret_key123',
    SQLALCHEMY_DATABASE_URI='sqlite:///'+DATABASE_PATH,  # Il path al database
    DEBUG=True  # Imposto qua la modalità debug
                # Vedi app.run() alla fine del file
)



PRODOTTI = [
    {'title': 'Farina di grano tenero', 'image': 'fgt.jpeg'},
    {'title': 'Formaggio toma', 'image': 'ft.jpg'},
    {'title': 'Mele Golden', 'image': 'mg.jpeg'},
    {'title': 'Miele di acacia Bio', 'image': 'mda.jpeg'},
    {'title': 'Olio Extravergine di oliva Bio', 'image': 'odo.jpeg'},
    {'title': 'Riso Integrale', 'image': 'ri.jpeg'},
    {'title': 'Zucchine novelle ', 'image': 'zn.jpeg'},
]


@app.route('/')
def index():
    
    return render_template('index.html', prodotti = PRODOTTI)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['username'] = user
            flash('Login exitoso!', 'success')
            return redirect(url_for('product_list'))
        else:
            flash('Nombre o contraseña incorrectos.', 'danger')
    return render_template('login.html')


@app.route('/home')
def home():
    if 'user_id' in session:
        user = db.session.query(user).get(session['user_id'])
        return render_template('home.html', utente=user)
    return render_template('home.html')


db.init_app(app)  # Inizializza l'istanza di SQLAlchemy con l'app Flask

if __name__ == '__main__':
    with app.app_context():
        init_db(app)
    app.run(debug=True)
