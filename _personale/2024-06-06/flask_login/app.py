from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

USER = {"mrossi": "osoejfj3", "ggangi": "odoeooeee"}


# route per home


@app.route("/")
def home():
    # Lista di dizionari contenenti titolo e URL
    contenitore = [{"title": "Login", "url": "/login"}]
    # Passiamo la lista al template

    return render_template("home.html", contenitore=contenitore)


# route per login


@app.route("/login", methods=["GET", "POST"])
def login():

    # se il metodo è POST
    if request.method == "POST":
        # leggiamo il nome utente
        rx_username = request.form.get("tx_user")
        # leggiamo la password
        rx_password = request.form.get("tx_password")
        # per controllare se un utente e' presente

        print("user:", rx_username)
        print("password:", rx_password)

        if rx_username in USER:
            if rx_password == USER[rx_username]:

                return redirect(url_for("films"))
            else:
                return "PASSWORD ERRATA"

        else:
            return "USER NON VALIDO"

    return render_template("login.html")


# route per film


@app.route("/films")
def films():

    return render_template("films.html")


if __name__ == "__main__":
    app.run(debug=True)
