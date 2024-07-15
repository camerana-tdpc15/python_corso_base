from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
from models import User, Lotto, Prenotazione, Prodotto, Produttore, db
from populate_db import init_db
from settings import DATABASE_PATH

app = Flask(__name__)   #creando un’istanza dell’app Flask 

app.config.update(      #Configuri l’URI del database SQLAlchemy 
        # per utilizzare un database SQLite situato nel percorso specificato
    SECRET_KEY='my_very_secret_key123', #  viene utilizzata per la gestione delle sessioni 
        #e altre funzionalità legate alla sicurezza.
    SQLALCHEMY_DATABASE_URI='sqlite:///'+DATABASE_PATH,     #Configuri l’URI del database SQLAlchemy 
        # per utilizzare un database SQLite situato nel percorso specificato

        )
