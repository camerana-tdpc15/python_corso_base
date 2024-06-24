from flask import Flask, render_template, request

app = Flask(__name__)

# Lista per memorizzare i messaggi del guestbook
guestbook_messages = []

@app.route('/')
def index():
    return render_template('guestbook_ES09.html', messages=guestbook_messages)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    message = request.form.get('message')
    guestbook_messages.append({'name': name, 'message': message})
    return render_template('guestbook_ES09.html', messages=guestbook_messages)

if __name__ == '__main__':
    app.run(debug=True)
