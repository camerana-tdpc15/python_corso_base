from flask import Flask, request, render_template

app = Flask(__name__)

USERS = {
    'mrossi': 'osoejfj3',
    'ggangi': 'odoeooeee'
}



#route per Home
@app.route('/')
def home():
    return render_template('home.html')

#route per Login
@app.route('/login')
def login():
    ...
    #per controllare se un utente c'è
    # if rx_username in USERS:
    #     ...

    # if rx_password == USERS[rx_username]:
    #     ...
    #    return render_template('films.html')

    return render_template('home.html')

#route per Logout
@app.route('/logout')
def logout():
    ...
    return render_template('home.html')


#route per Films
@app.route('/films')
def films():
    return render_template('films.html')

if __name__== '__main__':
    app.run(debug=True)
    
