from flask import Flask, request, render_template

app = Flask(__name__)

USERS = {
    'mrossi': 'osoejfj3',
    'ggangi': 'odoeooeee'
}


# route per Home
@app.route('/')
def home():
    return render_template('home.html')

# route per Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Se il metodo è POST
    if request.method == 'POST':
        # Leggiamo il nome utente (rx_username)
        rx_username = request.form.get('tx_user')
        # Leggiamo la password (rx_password)
        rx_password = request.form.get('tx_password')

        print('User:', rx_username)
        print('Password:', rx_password)

        # Per copntrollare se un utente è presente
        if rx_username in USERS:
            if rx_password == USERS[rx_username]:
                ...
        #       return render_template('films.html')

    return render_template('login.html')


# route per Films

@app.route('/films')
def films():
    return render_template('films.html')


if __name__ == '__main__':
    app.run(debug=True)