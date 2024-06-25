from flask import Flask
app = Flask(__name__)

app.config.update(
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+DATABASE,
    DEBUG=True)

if __name__ == "_main_":
    app.run()