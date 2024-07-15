from flask import Flask, session
from models import   db, init_db

# Lotto, Prenotazione, Prodotto, Produttore, User,

from settings import DATABASE_PATH



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DATABASE_PATH

db.init_app(app)

@app.route('/')
def home():
    return ('CIAO')

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)