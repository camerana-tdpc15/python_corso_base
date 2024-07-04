from flask import Flask, render_template
from models import db, init_db
from settings import DATABASE

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+DATABASE

db.init_app(app)

@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    with app.app_context():
        init_db(app)
    app.run(debug=True)