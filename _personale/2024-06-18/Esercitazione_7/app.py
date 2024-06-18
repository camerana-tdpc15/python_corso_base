from flask import Flask, flash, redirect, render_template, request, session, url_for
from settings import DATABASE
from models import init_db, db, User, Film

app = Flask(__name__)

app.config.update(
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE,
    DEBUG = True
)

db.init_app(app)
#4 route da impostare
@app.route('/')
def home():
    return (render_template.template('home.html'))
    #return ('ciao')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        rx_username = request.form.get('tx_user')
        rx_password = request.form.get('tx_password')

        user = User.query.filter_by(login=rx_username).first()

        if user and user.password == rx_password:
            session['username'] = rx_username
            flash('Benvenuto!', 'success')        
            app.logger.info(f"L'utente {rx_username} ha effettuato l'accesso.")
            return redirect(url_for('films'))
        
        else:
            flash('Username o password errati.', 'danger')
            app.logger.warning(f"Accesso fallito {rx_username}.")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Arrivederci.', 'warning')
    return redirect(url_for('home'))


@app.route('/films')
def films():
    if 'username' in session:
        films = Film.query.all()
        return render_template('films.html', films=films)
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        init_db(app)
    app.run()

