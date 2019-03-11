from flask import render_template
from app import app
from bokeh.embed import components
from bokeh_vbar import create_bar_chart

@app.route("/")
@app.route("/home")
def home():
    data = {"title":"Home Page", "heading": "Home"}
    return render_template('home.html', data=data)

@app.route("/workshop")
def workshop():
    pubs = [{"title":"NLP", "link":"https://github.com/epmarie/IntroNLP"},
            {"title":"Network Analysis", "link":"https://github.com/epmarie/network_workshop"},
            {"title":"Flask", "link":"https://github.com/epmarie/flask_example_app"}]
    data = {"title": "Workshops", "heading": "Latest Workshops", "pubs":pubs}
    return render_template('workshop.html', data=data)

@app.route("/vbar", defaults={'days': 13})
@app.route("/vbar/<int:days>/")
def graphics(days):
    days = 13 if days < 1 else days
    plot = create_bar_chart(days=days)
    script, div = components(plot)
    data = {"title":"Graphics", "heading":"Chart", "days":days, "div":div, "script":script}
    return render_template("graphics.html", data=data)

# todo:
# add url param display bokeh chart
# graphic / page for python anywhere
# make PA account
# updating site once deployed