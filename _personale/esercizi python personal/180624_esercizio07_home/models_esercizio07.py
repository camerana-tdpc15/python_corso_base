import os
# consente di interagire con il sistema
import csv
# Questo modulo ti permette di leggere e scrivere file CSV
import sys
# Questo modulo fornisce funzionalità e variabili specifiche del sistema, 
# come l’accesso agli argomenti della riga di comando, la gestione delle eccezioni e altre operazioni legate al sistema.
from datetime import datetime
# Questo modulo ti permette di lavorare con date e orari,
#  e offre funzionalità per ottenere la data corrente, formattare date, calcolare differenze tra date e altro ancora.

from flask_sqlalchemy import SQLAlchemy
from settings_esercizio07 import USER_TABLE_CSV, FILM_TABLE_CSV, USER_TABLE_NAME, FILM_TABLE_NAME


db = SQLAlchemy()
class User (db.Model):
    __tablename__ = USER_TABLE_NAME
# creato una classe User che eredita dalla classe db.Model di SQLAlchemy. La variabile 
# __tablename__ è stata impostata con il valore della variabile USER_TABLE_NAME, che rappresenta il nome della tabella nel database.
    id = db.Column()


class Film (db.Model):
    __tablename__ = FILM_TABLE_NAME
    