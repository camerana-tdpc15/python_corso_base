import os
import json
from datetime import date
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from settings import BASE_DIR, DATA_PATH, DATABASE_PATH

db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    cognome = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False) 

    serialize_rules = ('-password',  '-pronotazioni.user')









