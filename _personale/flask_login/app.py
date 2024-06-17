from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)
# impostiamo una chiave segreta ( che vediamo solo noi sviluppatori)
# la chiave servirà per crittografare e firmare i cookies
app.secret_key = 'my_very_secret_key123'

USERS = {
    'mrossi': 'PASSWORD',
    'ggangi': 'PASSWORD'
}


# route per la Home
@app.route('/')
def home():
    return render_template('home.html')

# route per login
@app.route('/login', methods=['GET','POST'])
def login():
    # se il metodo è POST
    if request.method =='POST':
        # leggi il nome utente (rx_username)
        rx_username = request.form.get('tx_user')
        # leggiamo la password 
        rx_password = request.form.get('tx_password')

        # print('user:', rx_username)
        # print('password:', rx_password)
    

        # per controllare se un utente è presente
        if rx_username in USERS:
            if rx_password == USERS[rx_username]:
                session['username'] = rx_username
                # Bisogna invece fare la direct:
                return redirect(url_for('films'))
            return render_template('login.html')

# if rx_username in USERS:
#    ...
# if rx_password == USERS[rx_username]:
#  ...


    return render_template('login.html')
@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('home'))

# route films

@app.route('/films')
def films():

    if 'username' in session:
        return render_template('films.html')
    else:
        return redirect(url_for('login'))
    # return render_template('films.html')



if __name__ == '__main__':
    app.run(debug=True)