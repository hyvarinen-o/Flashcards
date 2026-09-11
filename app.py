from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Alrighti roo lets get the show going"
