from flask import Flask, render_template, request, redirect, url_for

app= Flask(__name__)

registered_user ={
    'mrossi': 'osoejfj3',
    'ggangi': 'odoeooeee',
}
@app.route('/', methods= ['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username in registered_user and registered_user[username] ==password:
        return redirect(url_for('film'))
    else:
        return render_templates('login.html', error=True)
    if __name__== '__main__':
        app.run(debug=True)