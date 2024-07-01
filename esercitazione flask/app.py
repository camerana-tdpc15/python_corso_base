from flask import Flask
from setting import DATABASE
from models import init_db
app = Flask (__name__) 

app.config.update(
    SQLALCHEMY_DATABASE_URI = "sqllite:///" +DATABASE
    DEBUG=True
)


if __name__ == "__main__":
    with app.app_context():
        init_db(app)
    app.run()