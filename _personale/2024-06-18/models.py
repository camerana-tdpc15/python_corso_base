from flask_sqlalchemy import SQLALchemy

db = SQLALchemy()

def init_db(app)
    db.creare_all()
