from flask import Flask, request, jsonify, render_template
from models import db, User, Prodotto, Produttore, Lotto, Prenotazione
from settings import SQLALCHEMY_DATABASE_URI, DATABASE_PATH

app = Flask(__name__)
app.config.from_object('settings')
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/api/carrello', methods=['POST'])
def manage_cart():
    data = request.get_json()
    action = data.get('action')
    cart_item_id = data.get('cart_item_id')
    lotto_id = data.get('lotto_id')
    quantity = data.get('quantity')

    if action == 'add':
        # Retrieve the lotto and the user (this is a simple example, in a real app you would get the actual logged in user)
        lotto = Lotto.query.get(lotto_id)
        user = User.query.get(1)  # Example user ID

        if not lotto or lotto.get_qta_disponibile == 0:
            return jsonify({'error': 'Lotto non disponibile'}), 400

        # Add the lotto to the user's cart
        cart_item = Prenotazione(user_id=user.id, lotto_id=lotto.id, quantity=1)
        db.session.add(cart_item)
        db.session.commit()

        return jsonify({'message': 'Lotto aggiunto al carrello!'})

    elif action == 'update':
        cart_item = Prenotazione.query.get(cart_item_id)
        if not cart_item:
            return jsonify({'error': 'Elemento del carrello non trovato'}), 404

        cart_item.quantity = quantity
        db.session.commit()

        return jsonify({'message': 'Quantità aggiornata'})

    elif action == 'delete':
        cart_item = Prenotazione.query.get(cart_item_id)
        if not cart_item:
            return jsonify({'error': 'Elemento del carrello non trovato'}), 404

        db.session.delete(cart_item)
        db.session.commit()

        return jsonify({'message': 'Elemento del carrello rimosso'})

@app.route('/api/carrello', methods=['GET'])
def get_cart():
    user = User.query.get(1)  # Example user ID
    cart_items = Prenotazione.query.filter_by(user_id=user.id).all()
    cart_data = [{
        'id': item.id,
        'lotto': item.lotto.to_dict(),  # Using the serialization
        'quantity': item.quantity
    } for item in cart_items]

    return jsonify(cart_data)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/carrello')
def carrello():
    return render_template('cart.html')

if __name__ == '__main__':
    app.run(debug=True)