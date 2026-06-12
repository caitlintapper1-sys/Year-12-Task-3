from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

#create the web host app (?? seems important don't touch)
app = Flask(__name__)

#route for test homepage
@app.route("/", methods=['GET', 'POST'])
def home():
    #makes it load the base.html template
    return render_template('main.html')

@app.route("/menu", methods=['GET', 'POST'])
def menu():
    return render_template('menu.html')

@app.route("/menu_game", methods=['GET','POST'])
def menu_game():
    return render_template('menu_game.html')

#starts the website IMPORTANT don't touch
app.run(debug=True, port=5000)