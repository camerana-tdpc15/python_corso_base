from flask import Flask,request, render_template, redirect,url_for,session

app= Flask(__name__)
#impostiamo una chiave segreta
app.secret_key='paolortaldapaolortaldapaolortalda'

USERS= {
# Nome : password 
    'mrossi':'osoejfj3',
    'ggangi':'odoeooeee',
}


@app.route("/")
def home():
   return render_template('home.html')




@app.route("/films")
def films():
    if 'username'in session:
        return render_template('films.html')
    else:
       return redirect(url_for('login')) 



@app.route("/login" , methods=['GET', 'POST'])
def login():
    # SE IL METODO E' POST
    if request.method == 'POST':  
        rx_username = request.form.get ('tx_user')  #  leggiamo nome utente
        rx_password = request.form.get ('tx_password')  #  leggiamo password
 
        # PER CONTROLLARE SE L'UTENTE E' PRESENTE 
        if rx_username in USERS:          

            if rx_password == USERS[rx_username]:
               session['username']= rx_username
                
               return redirect(url_for('films'))
    return render_template('login.html')        

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect (url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)