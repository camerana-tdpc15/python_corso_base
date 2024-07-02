
from flask import Flask
from settings import DATABASE_PATH
from models import db, init_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DATABASE_PATH

# Inizializzo il database dal modulo models
db.init_app(app)

if __name__ == '__main__':
    with app.app_context():
        init_db(app)
    app.run(debug=True)