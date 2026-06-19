from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

#create the web host app (?? seems important don't touch)
app = Flask(__name__)

#route for test homepage
@app.route("/", methods=['GET', 'POST'])
def home():
    #makes it load the main.html template
    return render_template('main.html')

#route for menu, opens on 'game' tab by default
@app.route("/menu", methods=['GET', 'POST'])
def menu():
    return render_template('menu_game.html')
#route for clues tab in menu
@app.route("/menu_clues", methods=['GET','POST'])
def menu_clues():
    return render_template('menu_clues.html')

#route for inventory tab in menu
@app.route("/menu_inventory", methods=['GET', 'POST'])
def menu_inventory():
    return render_template('menu_inventory.html')


#starts the website IMPORTANT don't touch
app.run(debug=True, port=5000)