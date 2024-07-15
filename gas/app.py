from flask import Flask
from models import db, int_db
from settings import DATABASE_PATH

app = Flask(__name__)

db.init_app(app) #inizializza l'istanza

if __name__ == '__main__':
    app.run(debug=True)