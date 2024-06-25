from flask import Flask,render_template,request,jsonify
import os


BASE_DIR_PATH = os.path.abspath(os.path.dirname(__file__))
MIO_FILE_PATH = os.path.join(BASE_DIR_PATH, 'guestbook.txt')

app = Flask(__name__)

@app.route('/')

def home():

    return render_template('guestbook.html')



@app.route('/api/guestbook',method=['POST'])

def guestbook():
    if request.method == 'POST':
        # Lettura di nome e messagio
        nome = request.json.get('nome')
        messagio = request.json.get('messagio')


       


        if not nome or not messagio:
            response = {'error':'Nome e messagio sono obbligatori'}
            return jsonify(response)
        
        response = {'success!': 'ok'}
        return jsonify(response)
        # Scritura su file
        #with open('guestbook.txt', mode='a') as file:
         #   file.write(f'Success\n')
    with open('guestbook.txt','a') as file:
           file.write()
       

   # else: #richiesta GET
       
       

           # Lettura del file
            #Restituzioe delle righe delle file in formato JSON
        
    #   with open('datos.txt', 'r') as file:
     #      file = file.readlines
   








if __name__ == '__main__':
    app.run(debug=True)


 