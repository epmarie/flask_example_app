from app import app

@app.route("/")
def hello():
    return("Hello World!")

@app.route("/home")
def home():
    return("Welcome home!")

@app.route("/research")
def research():
    return("Here's some of my latest research:")