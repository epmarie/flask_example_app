from flask import render_template
from app import app

@app.route("/")
def hello():
    return("Hello World!")

@app.route("/home")
def home():
    return("Welcome home!")

@app.route("/research")
def research():
    title = "Research"
    heading = "Lates Publications will be Listed Below"
    pubs = ["High Process Computing","NLP","Network Analysis"]
    return render_template('research.html', title=title, heading = heading, pubs = pubs)