from flask import Flask,request, render_template, redirect, url_for, session
app = Flask (__name__)



UserLogin ={
    'mrossi': '12345',
    'ggangi': '67890'
}
    # route  home
@app.route('/')
def home():
    return render_template('home_login0.html')


    # route login
@app.route('/login0', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        rx_username = request.form.get('tx_user')
        rx_password = request.form.get('tx_password')
    if rx_username in UserLogin:
        if rx_password == UserLogin[rx_username]:
            session ['username'] = rx_username
            return redirect (url_for('/film_login0'))
    return render_template('/login0.html')  
        #       PERCHE LOGIN0.HTML HA L'ESTENSIONE E FILM_LOGIN NO ???????????

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home_login0'))

    # route film
app.route('/film_login0')
def  film_loginn0():
    if 'username' in session:
        films =[
            {'title':'AKIRA', 'image':url_for('static'filename='AKIRA.jpg')},
        ]
    return render_template('film_login0.html', films=film_loginn0.html)
else:
    return redirect(url_for('film_login0'))
         



if __name__ == '__main__':
    app.run(debug = True)
