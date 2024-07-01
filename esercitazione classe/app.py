import os

from flask import Flask, request, 

def render_home():
    return render_template('home.html')
    
@app.route('api/guestbook', methods=['GET', 'POST'])
def guestbook