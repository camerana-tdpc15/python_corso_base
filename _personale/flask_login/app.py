from flask import Flask, render_template, request

app = Flask(__name__)


USERS = {
    'mrossi': 'osoejfj3',
    'ggangi': 'odoeooeee'
}

# route per home

@app.route('/home')
def home():
    return render_template('home.html')

# route per film

@app.route('/movies')
def movies():
    return render_template('movies.html')




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
# se il metodo è post   
    # CONTROLLARE SE UN UTENTE è PRESENTE
    #    if rx_mrossi in USERS:
    #     ...

    #     if rx_utente == USERS[rx_username]:
    #         ....
    #   return render_template('movies.html')



    
        rx_username = (request.form.get('tx_user'))
        rx_password = (request.form.get('tx_password'))

        print('User', rx_username)
        print('Password', rx_password)
        ...
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
