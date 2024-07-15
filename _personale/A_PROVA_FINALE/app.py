from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
from models import User, Lotto, Prenotazione, Prodotto, Produttore, db
from populate_db import init_db
from settings import DATABASE_PATH

