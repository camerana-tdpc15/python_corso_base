from flask import Flask, request, render_template,redirect, url_for

app = Flask(__name__)

USERS = {
 'mrossi': 'osoejfj3',
 'ggangi' : 'odoeooeee',
 'ebambace': '123asd'
}



# Home per la route

@app.route('/')
def home():
    return render_template('index.html')


# Route per Login

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        rx_username = request.form.get('tx_user')
        rx_password = request.form.get('tx_password')

        print('User', rx_username)
        print('Password', rx_password)
    
        if rx_username in USERS:
            if rx_password == USERS[rx_username]:

             return redirect(url_for('films'))
            
    return render_template('login.html')



@app.route('/films')
def films():
   return render_template('films.html')

if __name__ == '__main__':
   app.run(debug=True)