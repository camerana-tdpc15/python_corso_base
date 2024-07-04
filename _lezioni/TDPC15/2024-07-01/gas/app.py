from flask import Flask
from models import db, init_db
from settings import DATABASE

app = Flask(__name__)

db.init_app(app)


if __name__ == '__main__':
    with app.app_context():
        init_db(app)
    app.run(debug=True)