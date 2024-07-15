from flask import Flask
from models import   db, init_db

from settings import DATABASE_PATH



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DATABASE_PATH
app.config['SECRET_KEY'] = 'my_very_secret_key123'

db.init_app(app)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)