from flask import Flask, request, render_template, redirect, url_for, jsonify

app = Flask(__name__)


FILE_JSON = [
    {
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "year": 1960,
        "genre": "Fiction"
    },
    {
        "title": "1984",
        "author": "George Orwell",
        "year": 1949,
        "genre": "Dystopian"
    },
    {
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "year": 1813,
        "genre": "Romance"
    },
    {
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "year": 1925,
        "genre": "Fiction"
    },
    {
        "title": "Moby Dick",
        "author": "Herman Melville",
        "year": 1851,
        "genre": "Adventure"
    },
    {
        "title": "War and Peace",
        "author": "Leo Tolstoy",
        "year": 1869,
        "genre": "Historical Fiction"
    },
    {
        "title": "The Catcher in the Rye",
        "author": "J.D. Salinger",
        "year": 1951,
        "genre": "Fiction"
    },
    {
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "year": 1937,
        "genre": "Fantasy"
    },
    {
        "title": "Ulysses",
        "author": "James Joyce",
        "year": 1922,
        "genre": "Modernist"
    },
    {
        "title": "The Odyssey",
        "author": "Homer",
        "year": -800,
        "genre": "Epic"
    }
]



@app.route('/', methods=['GET'])
def home():
    data_file =  jsonify(FILE_JSON)
    #return render_template('index.html', FILE_JSON=FILE_JSON)
    return data_file



if __name__ == '__main__':
    app.run(debug=True)