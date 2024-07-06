from flask import Flask
from  models import db, init_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DATABASE_PATH


db.init_app(app) 

if __name__ =='__name__':
    with app.app_context():
        init_db()
    app.run(deburg=True)