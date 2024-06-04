from flask import Flask, request, render_template, flash, session

app = Flask(__name__)

# creo una lista di dizionari con nome utente e password
users = {
    'mrossi' : 'osoejfj3',
    'ggangi' : 'odoeooeee'
}


# route per home
@app.route('/')
def home():
    return render_template('home.html')

# route per login
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Se il metodo è POST:
    if request.method == 'POST':

        # leggiamo il nome utente (rx_username)
        # si usa 'request.form' perchè abbiamo i dati provenienti 
        # da un form quindi 'FormData'
        rx_username = request.form.get('tx_user')
        # leggiamo la password
        rx_password = request.form.get('tx_password')

        #print('user ',rx_username)
        #print('password ', rx_password)
            # per controllare se un utente è presente
        if rx_username in users:
            
            if rx_password == users[rx_username]:
                
                return render_template('film.html')
        
    return render_template('login.html')

# route per film 
@app.route('/film')
def film():
    return render_template('film.html')

# questo si mette cosi sempre
if __name__== '__main__':
    app.run(debug=True)
