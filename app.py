from flask import Flask

#create the web host app (?? seems important don't touch)
app = Flask(__name__)

#route for test homepage
@app.route("/")
def home():
    return "Hello, World!"

#starts the website IMPORTANT don't touch
app.run(debug=True, port=5000)