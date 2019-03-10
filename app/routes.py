from flask import render_template
from app import app

@app.route("/")
@app.route("/home")
def home():
    return("Hello, World! Welcome home.")

@app.route("/workshop")
def workshop():
    pubs = [{"title":"NLP", "link":"https://github.com/epmarie/IntroNLP"},
            {"title":"Network Analysis", "link":"https://github.com/epmarie/network_workshop"},
            {"title":"Flask", "link":"https://github.com/epmarie/flask_example_app"}]
    data = {"title": "Workshops", "heading": "Latest Workshops", "pubs":pubs}
    return render_template('workshop.html', data=data)

# todo:
# add url param display bokeh chart
# graphic / page for python anywhere
# make PA account
# cut github part
# template inheritance & linking
# updating site once deployed