from flask import Flask

from models import int_db
from settings import DATABASE

app = Flask(__name__)

app.config.update(
    SQLALCHEMY_DATABASE_URI ="sqlite:///"+DATABASE,
    DEBUG=True  
)

# routes da importare
@app.route("/")
def home():
    return ""

if __name__ == "__main__":
    with app.app._contex():
        int_db(app)
    app.run()