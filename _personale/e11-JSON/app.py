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


db.init_app(app)  # Inizializza l'istanza di SQLAlchemy con l'app Flask

if __name__ == '__main__':
    with app.app_context():
        init_db(app)
    app.run(debug=True)
