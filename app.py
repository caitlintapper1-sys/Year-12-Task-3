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
        db.execute(f'''UPDATE dialogue SET show = "no" WHERE id == 1''',)
        db.commit()
        db.execute(f'''UPDATE items SET obtained = "F"''',)
        db.commit()
        db.execute(f'''UPDATE puzzles SET solved = "unsolved"''',)
        db.commit()
        return render_template('start.html')

#route for tutorial/explanation
@app.route("/tutorial")
def tutorial():
      return render_template('tutorial.html')

#sets variable default so they don't reset everytime the page reloads
safeCode = 'unsolved'
targetCode = 'unsolved'

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

        #checks if the puzzle is solved or not
        safeCode, = db.execute(f'''SELECT solved FROM puzzles
                                WHERE id == 1''',).fetchone()
        targetCode, = db.execute(f'''SELECT solved FROM puzzles
                                WHERE id == 2''',).fetchone()
        #prevents code from running if the puzzle is already solved
        if safeCode != 'solved' or targetCode != 'solved':
            if request.method == 'POST':
                #prevents issues if the puzzle hasn't been answered
                try:
                    #gets the users answer for the puzzle 
                    safeCodeGuess = request.form['safe']
                    #checks if the answer is correct and updates sql
                    if int(safeCodeGuess) == 2947:
                        db.execute(f'''UPDATE puzzles SET solved = 'solved' WHERE id = 1''',)
                        db.commit()
                        safeCode = 'solved'
                except:
                    safeCodeGuess = 0
                try:
                    #gets the users answer for the puzzle 
                    targetNameGuess = request.form['target']
                    #checks if the answer is correct and updates sql
                    if targetNameGuess.lower() == 'the commissioner':
                        db.execute(f'''UPDATE puzzles SET solved = 'solved' WHERE id = 2''',)
                        db.commit()
                        return redirect(url_for('station'))
                except:
                    targetNameGuess = ''

        #checks if dialogue should be shown
        showDialogue, = db.execute(f'''SELECT show FROM dialogue
                                WHERE id == 1''',).fetchone()
        #gets the dialogue that needs to be shown
        dialogueContent, = db.execute(f'''SELECT dialoguecontent FROM dialogue
                                WHERE id == 1''',).fetchone()
        #prevents dialogue from showing again if the page reloads
        db.execute(f'''UPDATE dialogue SET show = "no" WHERE id = 1''',)
        db.commit()

        openSafe, = db.execute(f'''SELECT obtained FROM clues
                                WHERE id == 10''',).fetchone()
        return render_template('apartment.html', clues=clues, items=items, openSafe=openSafe, safeCode=safeCode, showbutton=showbutton, showDialogue=showDialogue, dialogueContent=dialogueContent)

#updates SQL to say a clue is obtained when the user clicks it
@app.route('/processClue', methods=['POST'])
def processClue():
    db = get_db()
    #gets id from javascript
    id = request.form.get('data')
    #updates SQL
    db.execute(f'''UPDATE clues SET obtained = "T" WHERE id = {int(id)}''',)
    db.commit()
    #indicates dialogue needs to be shown
    db.execute(f'''UPDATE dialogue SET show = "yes" WHERE id = 1''',)
    db.commit()
    #gets dialogue from file
    d = open('static/dialogue/apartment-dialogue-clues.txt').read()
    #puts dialogue into sql so the main page can access it
    db.execute(f'''UPDATE dialogue SET dialoguecontent = "{d}" WHERE id = 1''',)
    db.commit()
    
    return d

#updates SQL to say an item is obtained when the user clicks/obtains it
@app.route('/processItem', methods=['POST'])
def processItem():
    db = get_db()
    #gets id from javascript
    id = request.form.get('data')
    #updates SQL
    db.execute(f'''UPDATE items SET obtained = "T" WHERE id = {int(id)}''',)
    db.commit()
     #indicates dialogue needs to be shown
    db.execute(f'''UPDATE dialogue SET show = "yes" WHERE id = 1''',)
    db.commit()

    
    #gets dialogue from file
    d = open('static/dialogue/apartment-dialogue-clues.txt').read()
    #puts dialogue into sql so the main page can access it
    db.execute(f'''UPDATE dialogue SET dialoguecontent = "{d}" WHERE id = 1''',)
    db.commit()
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