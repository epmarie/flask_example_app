from flask import render_template
from app import app
from bokeh.embed import components
from bokeh_vbar import create_bar_chart
from bokeh_calendar import create_calendar

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
    heading = f'Bokeh Chart Using {days} Days'
    data = {"title":"Graphics", "heading":heading, "days":days, "div":div, "script":script}
    return render_template("graphics.html", data=data)

@app.route("/calendar")
def calendar():
    cal = create_calendar()
    script, div = components(cal)
    data = {"title":"Graphics", "heading":"Bokeh Calendar", "div":div, "script":script}
    return render_template("graphics.html", data=data)