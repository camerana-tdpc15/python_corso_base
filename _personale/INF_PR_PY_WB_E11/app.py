from flask import Flask

# qui importo il db da models
from settings import DATABASE_PATH
from models import db, init_db


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+DATABASE_PATH

# qui inizializzo il db importato da models
db.init_app(app)



    

if __name__ == '__main__':
    # con il contesto dell'app esistente
    with app.app_context():

        # avvio la funzione per inizializzare l'app
        init_db(app)

    app.run(debug=True)