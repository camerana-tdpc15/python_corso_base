from flask import Flask
from settings_esercizio07 import DATABASE




app = Flask(__name__)

app.config.update(
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+DATABASE,
    DEBUG=True
)


# routes da importare
@app.route("/")

def home():
    return "..."


if __name__ == "__main__":
    with app.app_context():
        init_db(app)
    app.run()