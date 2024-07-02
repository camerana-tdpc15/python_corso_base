from flask import Flask, render_template
from models import db, init_db
from settings import DATABASE_PATH

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+DATABASE_PATH

db.init_app(app)  # Inizializza l'istanza di SQLAlchemy con l'app Flask

@app.route('/')
def home():
    return render_template('home.html')


# @TODO: Qua ci vanno le routes
# ...

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)