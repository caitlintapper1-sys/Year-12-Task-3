from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response, send_from_directory, jsonify
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime

#create the web host app 
app = Flask(__name__)

def get_db():
    db = sqlite3.connect('database/task3.db', timeout = 15)
    db.row_factory = sqlite3.Row
    return db

#default route
@app.route("/")
def default():
       #redirects to start page
       return redirect(url_for('start'))

#route for starting page
@app.route("/start", methods=['GET', 'POST'])
def start():
        db = get_db()
        db.execute(f'''UPDATE clues SET obtained = "F" WHERE id > 1''',)
        db.commit()
        return render_template('start.html')

#route for tutorial/explanation
@app.route("/tutorial")
def tutorial():
      return render_template('tutorial.html')

#route for the first investigation section        
@app.route("/apartment", methods=['GET','POST'])
def apartment():
        db = get_db()
        #gets all clues the user has unlocked
        clues = db.execute(f'''SELECT * FROM clues 
                                WHERE obtained == 'T'
                                ORDER BY id ASC''',).fetchall()
        #gets all items the user has unlocked
        items = db.execute(f'''SELECT * FROM items 
                                WHERE obtained == 'T'
                                ORDER BY id ASC''',).fetchall()
        #checks if one of 2 clues is found
        clue1, = db.execute(f'''SELECT obtained FROM clues
                                WHERE id == 7''',).fetchone()
        clue2, = db.execute(f'''SELECT obtained FROM clues
                                WHERE id == 8''',).fetchone()
        #shows the associated button if one of the clues is found
        if clue1 == 'T' or clue2 == 'T':
            showbutton = True
        else:
            showbutton = False
        #gets the users answer for the puzzle 
        safeCode = 'unsolved'
        targetCode = 'unsolved'
        if request.method == 'POST':
            #prevents issues if the puzzle hasn't been answered
            try:
                safeCodeGuess = request.form['safe']
            except:
                safeCodeGuess = 0
            try:
                targetNameGuess = request.form['target']
            except:
                targetNameGuess = ''
            #checks if the answer is correct
            if safeCodeGuess == 2947:
                safeCode = 'solved'
            if targetNameGuess.lower() == 'the commissioner':
                targetCode = 'solved'

        return render_template('apartment.html', clues=clues, items=items, showbutton=showbutton, safeCode=safeCode, targetCode=targetCode)

#updates SQL to say a clue is obtained when the user clicks it
@app.route('/processClue', methods=['POST'])
def processClue():
    db = get_db()
    #gets id from javascript
    id = request.form.get('data')
    #updates SQL
    db.execute(f'''UPDATE clues SET obtained = "T" WHERE id = {int(id)}''',)
    db.commit()
    redirect(render_template('apartment.html'))
    return id

#updates SQL to say an item is obtained when the user clicks/obtains it
@app.route('/processItem', methods=['POST'])
def processItem():
    db = get_db()
    #gets id from javascript
    id = request.form.get('data')
    #updates SQL
    db.execute(f'''UPDATE items SET obtained = "T" WHERE id = {int(id)}''',)
    db.commit()
    #
    #if id == 1: 
        #redirect(render_template('apartment.html'))
    #else:
         #return(render_template('station.html'))
    return id
    
#route for the 2nd investigation section
@app.route('/station')
def station():
        db = get_db()
        #gets all clues the user has unlocked
        clues = db.execute(f'''SELECT * FROM clues 
                                WHERE obtained == 'T'
                                ORDER BY id ASC''',).fetchall()
        #gets all items the user has unlocked
        items = db.execute(f'''SELECT * FROM items 
                                WHERE obtained == 'T'
                                ORDER BY id ASC''',).fetchall()
        #checks if one of 2 clues is found
        clue1, = db.execute(f'''SELECT obtained FROM clues
                                WHERE id == 7''',).fetchone()
        clue2, = db.execute(f'''SELECT obtained FROM clues
                                WHERE id == 8''',).fetchone()
        #shows the associated button if one of the clues is found
        if clue1 == 'T' or clue2 == 'T':
            showbutton = True
        else:
            showbutton = False

        return render_template('station.html', clues=clues, items=items, showbutton=showbutton)

#route for the 3rd investigation section
@app.route('/alleyway')
def alleyway():
        db = get_db()
        #gets all clues the user has unlocked
        clues = db.execute(f'''SELECT * FROM clues 
                                WHERE obtained == 'T'
                                ORDER BY id ASC''',).fetchall()
        #gets all items the user has unlocked
        items = db.execute(f'''SELECT * FROM items 
                                WHERE obtained == 'T'
                                ORDER BY id ASC''',).fetchall()
        #checks if one of 2 clues is found
        clue1, = db.execute(f'''SELECT obtained FROM clues
                                WHERE id == 7''',).fetchone()
        clue2, = db.execute(f'''SELECT obtained FROM clues
                                WHERE id == 8''',).fetchone()
        #shows the associated button if one of the clues is found
        if clue1 == 'T' or clue2 == 'T':
            showbutton = True
        else:
            showbutton = False

        return render_template('alleyway.html', clues=clues, items=items, showbutton=showbutton)



#XMLHttp request!! something with that and Javascript and JSON(?) 
#look at the cat movie thingy's code trust


#starts the website IMPORTANT don't touch
app.run(debug=True, port=5000)