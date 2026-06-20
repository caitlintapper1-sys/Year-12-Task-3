from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

#create the web host app (?? seems important don't touch)
app = Flask(__name__)

started = False

#default route
@app.route("/")
def default():
       #redirects to start page
       return redirect(url_for('start'))

#route for starting page
@app.route("/start", methods=['GET', 'POST'])
def start():
        return render_template('start.html')

#route for tutorial/explanation
@app.route("/tutorial")
def tutorial():
      return render_template('tutorial.html')

#route for the first investigation section        
@app.route("/apartment")
def apartment():
       return render_template('apartment.html')


#starts the website IMPORTANT don't touch
app.run(debug=True, port=5000)