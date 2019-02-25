# Building a Web App with Flask
Flask is a microframework packed with tools to help build simple, quick web applications. We'll also be using Jinja2, a template engine, to create the bulk of the html content for our application. This tutorial will be split into two parts: creating the application and deploying it. We'll alternate between using the command line, editing code in a text editor (VSCode and Sublime are great options), and interacting with our application in a web browser (Chrome).

## Installating Packages
Luckily, Flask comes prepackaged with Jinja2, so we only have one bulk-package to install. Install Flask via the command line:
`$ pip install flask`

## Bare Bones: Hello World
After installing Flask, we'll start by creating a directory to store all of the files we'll create. Make sure you're in the appropriate working directory first, and then create the folder for your app and set that as your new working directory. Within this new working directory, create another folder called `app` - this will contain the _package_ we'll be creating.
```
$ mkdir my_app
$ cd my_app
$ mkdir app
```
Optionally, connect your application to a GitHub repository. This is not requried, but __strongly__ recommended. It's good to get in the habit of backing up your work, and storing your code on GitHub will make deploying your app easier if you decide to choose a different host. Then, add your first two python files using the `touch` command (if using GitHub, add a few other files, too).

```
$ git init
$ touch routes.py .gitignore README.md requirements.txt
$ cd app
$ touch __init__.py routes.py
```

Now we're ready to work with our python file. Open up `__init__.py` in VSCode and add the following content:
```
from flask import Flask
app = Flask(__name__)

from app import routes
```
We have a few more steps before our package is ready to go - open `routes.py`. This file will eventually define all the different routes (or pages) for your application (more on that later). For now, add the following content:
```
from app import app

@app.route("/")
@app.route("/index")
def hello():
    return("Hello World!")
```
Okay, the basics of our package are set! Now, back to our actual _application_. Set your working directory back to `my_app` and create another python file:
```
$ cd ..
$ touch my_app.py
```
Open that new file, add `from app import app`, and ta-da: your app is ready to go! Jump back over to your terminal and run `export FLASK_APP=my_app.py` to tell Flask how to import your application. Then, run `flask run` - you should see something like this:
```
 * Serving Flask app "app" (lazy loading)
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
In your web browser, navigate to <http://localhost:5000/>. You should see a white page with "Hello World!" in black text in the top right corner.
#### Check Point
Before continuing, make sure that your directory has the following structure:
```
my_app/
    .gitignore
    README.md
    requirements.txt
    my_app.py
    app/
        __init__.py
        routes.py
```
You may also see `__pycache__` in your folder - don't worry about this. If using GitHub, this is a good time to push your updates.

## Routes & Pages
In our code, notice the use of `@app.route("/"):` before our function definition. This is our way of telling the program to run the function we defined below when our URL is followed by just a forward slash. In other words, this is how we define __routes__ to access different __pages__. To see how this works, let's create a few sample routes. Take a few minutes and add two more routes, each with a function returning text. Then, re-run your application and navigate to those new routes!

Now that you have an idea of how routes work, we'll build some together. Initially, we just returned text for our routes. You can also return HTML, which we'll try here. Add a "reasearch" route to your `routes.py` file with the following function definition:
```
@app.route("/research")
def research():
    return '''
<html>
    <head>
        <title>Research Page - My App</title>
    </head>
    <body>
        <h1>Latest Publications will be Listed Below</h1>
    </body>
</html>'''
```

Run `flask run` again and navigate to <localhost:5000/research>. You should see the heading we just wrote.

## Templates
#### Basic Templating 

Now, let's say we had a list of publications that we wanted to display on our site, and that we had that list stored as a Python dictionary. We'd probably design our page like so:
```
@app.route("/research")
def research():
    pubs = ["High Process Computing","NLP","Network Analysis"]
    return '''
<html>
    <head>
        <title>Research Page - My App</title>
    </head>
    <body>
        <h1>Latest Publications will be Listed Below</h1>
        <ul>
            <li>''' + pubs[0]+'''</li>
            <li>''' + pubs[1]+'''</li>
            <li>''' + pubs[2]+'''</li>
        </ul>
    </body>
</html>'''
```
This approach takes constant editing and isn't very user-friendly. Thankfully, Jinja2, a templating tool, links with Flask. This will allow us to create __templates__ for our pages so that they can update easily. We'll start by making a folder for our templates and creating our index template - make sure you're in the `my_app` directory first.
```
$ mkdir app/templates
$ cd app/templates
$ touch research.html
```
Templates allow us to write HTML and use specific placeholders for certain data. Then, when our template is __rendered__, we pass in the data we want to use and it's automatically formatted exactly how we planned. Place the following code in `research.html`:
```
<html>
    <head>
        <title>{{ title }} - My App </title>
    </head>
    <body>
        <h1>{{ heading }}</h1>
        <ul>
        {% for pub in pubs %}
            <li>{{pub}}</li>
        {% endfor %}
        </ul>
    </body>
</html>
```
When we want to display an element from our data, we use double braces `{{ }}`. When we want to use logic, we use a brace paired with a percentage sign, `{% %}`.

Now, in order for this template to be rendered when navigating to the research page, we have to edit our `routes.py` file. Be sure to add `from flask import render_template` at the top, and then update your function definition for `research`:
```
def research():
    title = "Research"
    heading = "Latest Publications will be Listed Below"
    pubs = ["High Process Computing","NLP","Network Analysis"]
    return render_template('research.html', title=title, heading = heading, pubs = pubs)
```
Try re-running your site now - see how each publication is its own element in the list? Jinja took the data we provided and inserted it into the template we created.

#### Template Inheritance