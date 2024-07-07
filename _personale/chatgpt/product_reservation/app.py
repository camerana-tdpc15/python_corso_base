from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User, Produttore, Prodotto, Lotto, Prenotazione, init_db
from forms import LoginForm, ReservationForm
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reservations.db'
db.init_app(app)



login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    lotti = Lotto.query.filter_by(sospeso=False).all()
    return render_template('products.html', lotti=lotti)

@app.route('/my_reservations')
@login_required
def my_reservations():
    reservations = Prenotazione.query.filter_by(utente_id=current_user.id).all()
    return render_template('reservations.html', reservations=reservations)

@app.route('/reserve/<int:lotto_id>', methods=['GET', 'POST'])
@login_required
def reserve(lotto_id):
    lotto = Lotto.query.get(lotto_id)
    form = ReservationForm()
    if form.validate_on_submit():
        if form.qta.data > lotto.qta_lotto:
            flash('Quantity exceeds available amount')
        elif lotto.sospeso:
            flash('Cannot reserve from a suspended lot')
        else:
            reservation = Prenotazione.query.filter_by(utente_id=current_user.id, lotto_id=lotto_id).first()
            if reservation:
                flash('You already have a reservation for this lot')
            else:
                new_reservation = Prenotazione(utente_id=current_user.id, lotto_id=lotto_id, qta=form.qta.data)
                db.session.add(new_reservation)
                db.session.commit()
                return redirect(url_for('my_reservations'))
    return render_template('reserve.html', form=form, lotto=lotto)

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)


