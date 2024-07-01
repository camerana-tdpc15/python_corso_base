from flask import Flask, jsonify
from settings import DATABASE
from models import db, init_db, Studente,Corso,Esame,Docente
from sqlalchemy.sql import func
app = Flask(__name__)

app.config.update(
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + DATABASE,
    DEBUG=True,
)

db.init_app(app)

@app.route("/1")
def query1():
    result = db.session.query(
        Esame.matr_s,
        func.max(Esame.voto).label("VotoMassimo"),
        func.min(Esame.voto).label("VotoMinimo"),
        func.avg(Esame.voto).label("VotoMedia")
    ).group_by(Esame.matr_s).all()
    
    return jsonify([{"matr_s":r[0],"max":r[1],"min":r[2],"avg":r[3]} for r in result])

@app.route("/2")
def query2():
    result = db.session.query(
        Esame.matr_s,
        Studente.nome_s,
        func.max(Esame.voto).label("VotoMassimo"),
        func.min(Esame.voto).label("VotoMinimo"),
        func.avg(Esame.voto).label("VotoMedia")
    ).join(Esame, Studente.matr_s==Esame.matr_s).group_by(Esame.matr_s, Studente.nome_s).all()
    
    return jsonify([{"matr_s":r[0],"nome":r[1],"max":r[2],"min":r[3],"avg":r[4]} for r in result])

@app.route("/3")
def query3():
    result = db.session.query(
        Esame.matr_s,
        Studente.nome_s,
        func.max(Esame.voto).label("VotoMassimo"),
        func.min(Esame.voto).label("VotoMinimo"),
        func.avg(Esame.voto).label("VotoMedia")
    ).join(Esame, Studente.matr_s==Esame.matr_s).group_by(Esame.matr_s, Studente.nome_s).having(func.avg(Esame.voto)>28).all()
    
    return jsonify([{"matr_s":r[0],"nome":r[1],"max":r[2],"min":r[3],"avg":r[4]} for r in result])

@app.route("/4")
def query4():
    result = db.session.query(
        Esame.matr_s,
        Studente.nome_s,
        func.max(Esame.voto).label("VotoMassimo"),
        func.min(Esame.voto).label("VotoMinimo"),
        func.avg(Esame.voto).label("VotoMedia")
    ).join(Esame, Studente.matr_s==Esame.matr_s).filter(Studente.citta=="Torino").group_by(Esame.matr_s, Studente.nome_s).having(func.avg(Esame.voto)>28, func.count(Esame.data.distinct())>=10).all()
    
    return jsonify([{"matr_s":r[0],"nome":r[1],"max":r[2],"min":r[3],"avg":r[4]} for r in result])


if __name__ == "__main__":
    with app.app_context():
        init_db(app)
    app.run()    
        