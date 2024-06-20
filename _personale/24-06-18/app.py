from models import init_db
from flask import Flask, render_template, request
from settings import DATABASE,User, Film 

app = Flask(__name__)

app.config.update(
        SQLALCHEMY_DATABASE_URI = "sqlite:///"+DATABASE
)


# 4 route

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', Methods = ['GET','POST'] )
def login():
    if request.method  == 'POST':
        rx_username = request.form.get ('tx_user')
        rx_password = request.form.get('tx_password')

        user =

        if user  and user.password = 

    return render_template('login.html')


@app.route('/films')
def films():
    return render_template('films.html')


@app.route('/logout')
def logout():
    return render_template('logout.html')


if __name__ == '__main__':
    with app.app_context():
        init_db(app)
    app.run