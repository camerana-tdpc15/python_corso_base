from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    
    # mi collego al db
    connection = sqlite3.connect('C:\TDPC15-12\python_corso_base\_personale\Pitone\database.db')
    
    # setto la connessione al db in righe
    connection.row_factory = sqlite3.Row
    
    # seleziono il comando per fare query di select e 
    # aggiungo 'fetcall()' che farà si che tutte le righe saranno organizzate in una lista python
    # salvo il tutto in una variabile ' posts'
    posts = connection.execute('SELECT * FROM posts').fetchall()
    
    
    connection.close()
    
    return render_template('index.html', posts = posts)

if __name__ == '__main__':
    app.run(debug=True)