from flask import Flask
from models import db, init_db
from settings import DATABASE_PATH

app = Flask(__name__)

app.confi

db.init_app(app) # Inizializzare l'istanza di SQLAlchemy con l'app

if __name__=='__main__':
    with app.app_context():
        init_db(app)
    app.run(debug=True)