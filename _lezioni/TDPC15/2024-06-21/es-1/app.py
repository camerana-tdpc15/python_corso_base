
from flask import Flask, jsonify
from settings import DATABASE
from models import Concerto,Sala,Orchestra, db, init_db
app = Flask(__name__)

app.config.update(
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + DATABASE,
    DEBUG=True,
)

db.init_app(app)

@app.route("/")
def query():
    subquery_torino = db.session.query(Concerto.cod_o).join(Sala).filter(
        Sala.citta=="Torino"
    ).subquery()
    
    subquery_milano = db.session.query(Concerto.cod_o).join(Sala).filter(
        Sala.citta=="Milano"
    ).subquery()
    
    subquery_bologna = db.session.query(Concerto.cod_o).join(Sala).filter(
        Sala.citta=="Bologna"
    ).subquery()
    
    result = db.session.query(Orchestra.cod_o, Orchestra.nome_o).filter(
        Orchestra.num_elementi > 30,
        Orchestra.cod_o.in_(subquery_torino),
        Orchestra.cod_o.in_(subquery_milano),
        Orchestra.cod_o.notin_(subquery_bologna),
        #~Orchestra.cod_o.in_(subquery_bologna)  
    ).all()
    return jsonify([{"CodO":r[0],"NomeO":r[1]} for r in result])

if __name__ == "__main__":
    with app.app_context():
        init_db(app)
    app.run()    
        