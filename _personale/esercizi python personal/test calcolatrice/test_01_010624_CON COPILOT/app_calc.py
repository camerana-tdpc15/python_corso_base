# CREAMO L'APP

# from flask import Flask
# app = Flask(__name__)

#_________________PERCHE (__name__)???_________________
# UTILISANO __name__L'APPLICAZIONE  OTTIENE AUTOMATICAMENTE IL NOME DEL MODULO  CORRENTE
# IN FAZE DI SVILUPPO SI CHIAMERA "app_calc.py"
# IN FAZE DI PROGETTAZIONE SI CHIAMDERA "my_flask_app_calc"



# OGGETTO DI  CONFIGURAZIONE PER GESTIRE L'APP

# app.config ['TESTING'] = True
# app.config ['SECRET_KEY'] = 'The secretr key'


# TESTING - IMPOSTA LA MODALITA TEST - se attivo le eccezioni vengono propagate 
# inivece di essere gestite dagli error handlers dell'app

 # SECRET_KEY - imposta una chiave secreta per l'app, importante per la sicurezza e mantenuta secreta

# flask run --deburg    ?????


from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# SINTASI jsonify() -   imposta automaticamente gli header di risposta corretti e di tipo di contenuto 
#                       per le risposte JSON
#                   -   semplifica la creazione di API che restituiscono dati in formato JSON
#                   -   ACCETA UNO O PIU ARGOMENTI POSIZIONALI, CHE RAPPRESENTANO I DATI DA CONVERTIRE IN UN OGGETTO
#                       DI RISPOSTA JSON, E QUALSEASI NUMERO DI ARGOMENT CON NOME, UTILISATI PER
#                       PERSONALISARE L'OGGETTO DI RISPOSTA JSON 



@app.route("/")
def home():
    return render_template("index_010624.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    num1 = float(request.form.get("num1"))
    num2 = float(request.form.get("num2"))
    operator = request.form.get("operator")

    if operator == "add":
        result = num1 + num2
    elif operator == "subtract":
        result = num1 - num2
    elif operator == "multiply":
        result = num1 * num2
    elif operator == "divide":
        if num2 != 0:
            result = num1 / num2
        else:
            result = "Errore: divisione per zero"
    else:
        result = "Operatore non valido"

    return render_template("result.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)







