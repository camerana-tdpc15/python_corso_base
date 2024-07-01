from flask import Flask, render_template, request
app = Flask(__name__)




USERS = {
    'mrrossi' : 'dofogklh'
    'ggangi' : 'akldlflgf'

}

#route per home
@app.route('/')
def home():
    return render_template('home.html')


#route per login

@app.route('/login', methods=['GET', 'POST'])
def login():
    #Se il metodo è POST
    if request.method == 'POST':
        #Leggiamo il nome utente (rx_username)
        rx_username = request.form.get('tx_user')
    #Leggiamo la password (rx_password)
        rx_password =  request.form.get('tx_password')


        print('User', rx_username)
        print('Password', rx_password)
    #controllare se  UTENTE è presente
    ...

    # Per controllare se un utente è presente 
    if rx_username in USERS:
    #  ...
     if rx_password == USERS[rx_username]:
         #ATTENZIONE: Notare che se restituisce il template
         #l'URL rimane il medesimo
         #return render_template('films.html')
         #Bisogna inmvece fare una redirect :
         return redirect(url_for('films'))
     
     #che equivale a scriveredirettamente 
     #return redirect('/films)
     #...ma questa scrittura è meno manutenibile
     #in caso di ridenominazione della route
    

    # ...
    #return render_template('films.html')
    
    return render_template('login.html')

#route per Films
@app.route('/films')
def films():
    return render_template('home.html')




if __name__ == '__main__':
    app.run(debug=True)


