from flask import Flask
from flask_bcrypt import Bcrypt
from models import db, User
from settings import DATABASE_PATH

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+DATABASE_PATH
app.config['SECRET_KEY'] = 'mysecretkey'

db.init_app(app)  # Inizializza l'istanza di SQLAlchemy con l'app Flask

def rehash_passwords():
    with app.app_context():
        users = User.query.all()
        for user in users:
            # Verifica se la password è già hashata (ad esempio, la lunghezza dell'hash bcrypt è 60 caratteri)
            if len(user.password) != 60 or not user.password.startswith('$2b$'):
                # Hash la password con bcrypt
                hashed_password = bcrypt.generate_password_hash(user.password).decode('utf-8')
                user.password = hashed_password
                print(f"Password re-hashata per l'utente: {user.email}")
        db.session.commit()
        print("Re-hashing completato.")

if __name__ == '__main__':
    rehash_passwords()
