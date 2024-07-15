from flask import Flask, render_template
from model import db, init_db
from setting import DATABASE_PATH

app = Flask(__name__)
db.init_app(app)

app.config.update( 
    SQLALCHEMY_DATABASE_URI='sqlite:///'+ DATABASE_PATH)
# Mostra la pagina che deve elencare gli eventi disponibili



@app.route('/')
def home():
    return render_template('index.html')

# Mostra la pagina che deve elencare le prenotazioni dell'utente
@app.route('/prenotazioni')
def prenotazioni():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    else:
        return render_template('prenotazioni.html')
    

    @bp.route('/events')
@login_required
def events():
    events = Event.query.all()
    return render_template('events.html', events=events)

@bp.route('/reserve', methods=['POST'])
@login_required
def reserve():
    replica_id = request.form['replica_id']
    seats = int(request.form['seats'])
    replica = EventReplica.query.get(replica_id)
    event = replica.event

    if replica and not replica.is_canceled and replica.available_seats >= seats:
        replica.available_seats -= seats
        reservation = Reservation(user_id=current_user.id, event_replica_id=replica_id, seats_reserved=seats)
        db.session.add(reservation)
        db.session.commit()
        flash('Reservation successful', 'success')
    else:
        flash('Not enough seats available or event is canceled', 'danger')
    return redirect(url_for('main.events'))

@bp.route('/modify_reservation/<int:reservation_id>', methods=['POST'])
@login_required
def modify_reservation(reservation_id):
    reservation = Reservation.query.get(reservation_id)
    new_seats = int(request.form['seats'])
    difference = new_seats - reservation.seats_reserved
    replica = reservation.event_replica

    if replica.available_seats >= difference:
        reservation.seats_reserved = new_seats
        replica.available_seats -= difference
        db.session.commit()
        flash('Reservation updated', 'success')
    else:
        flash('Not enough seats available', 'danger')
    return redirect(url_for('main.reservations'))

@bp.route('/cancel_reservation/<int:reservation_id>', methods=['POST'])
@login_required
def cancel_reservation(reservation_id):
    reservation = Reservation.query.get(reservation_id)
    replica = reservation.event_replica
    replica.available_seats += reservation.seats_reserved
    db.session.delete(reservation)
    db.session.commit()
    flash('Reservation canceled', 'success')
    return redirect(url_for('main.reservations'))
