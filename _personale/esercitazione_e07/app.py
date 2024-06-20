from flask import Flask
from _personale.esercitazione_e07.models import init_db
from settings import DATABASE

app = Flask(__name__)

app.config.update(
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+DATABASE,
    DEBUG=True
)

@app.route('/')
def home():
    return ""

if __name__ == "__main__":
    with app.app_context():
        init_db(app)
    app.run()
