import locale
from flask import Flask, render_template, jsonify
from models import db, init_db, Lotto, Prodotto, Produttore
from settings import DATABASE_PATH

locale.setlocale(locale.LC_TIME, 'it_IT')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+DATABASE_PATH

db.init_app(app)  # Inizializza l'istanza di SQLAlchemy con l'app Flask

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/api/lotti', methods=['GET'])
def get_lotti():
    lotti = Lotto.query.all()
    
    lotti_data = []
    for lotto in lotti:
        dict_lotto = lotto.to_dict()
        lotti_data.append(dict_lotto)

    return jsonify(lotti_data)


if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)