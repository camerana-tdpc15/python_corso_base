from flask import Flask,request, render_template

app= Flask(__name__)

USERS= {
# Nome : password 
    'mrossi':'osoejfj3',
    'ggangi':'odoeooeee',
}


@app.route("/home")
def home():
   return render_template('home.html')




@app.route("/films")
def films():
   return render_template('films.html')




@app.route("/login" , methods=['GET', 'POST'])
def login():
    # SE IL METODO E' POST
    if request.method == 'POST':  
        rx_username = request.form.get ('tx_user')  #  leggiamo nome utente
        rx_password = request.form.get ('tx_password')  #  leggiamo password
 
        # PER CONTROLLARE SE L'UTENTE E' PRESENTE 
        if rx_username in USERS:          

            if rx_password == USERS[rx_username]:
                
               return render_template('films.html')
               
    return render_template('login.html')



if __name__ == '__main__':
    app.run(debug=True)