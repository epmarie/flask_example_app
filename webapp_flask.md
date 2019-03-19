# Building a Web App with Flask
Flask is a microframework packed with tools to help build simple, quick web applications. We'll also be using Jinja2, a template engine, to create the bulk of the html content for our application. This tutorial will cover creating a site, deploying it, and adding interactive Bokeh graphics. We'll alternate between using the command line, editing code in a text editor (VSCode and Sublime are great options), and interacting with our application in a web browser (Chrome).

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
Next, add your first two python files using the `touch` command.

```
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
@app.route("/home")
def hello():
    return("Hello World! Welcome home.")
```
Okay, the basics of our package are set! Now, back to our actual _application_. Set your working directory back to `my_app` and create another python file:
```
$ cd ..
$ touch flask_app.py
```
Open that new file, add the line `from app import app`, and ta-da: your app is ready to go! Since we'll be running it locally, we'll want to run our application in __debug (development)__ mode. Tell Flask to run your application in a development environment by running `export FLASK_ENV=development` in your terminal. Now run `export FLASK_APP=flask_app.py` to tell Flask how to import your application. Then, run `flask run` - you should see something like this:
```
[* Serving Flask app "app" (lazy loading)
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)]( * Serving Flask app "flask_app.py" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 267-280-087
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
)
```
In your web browser, navigate to <http://localhost:5000/>. You should see a white page with "Hello World! Welcome home." in black text in the top right corner.
#### Check Point
Before continuing, make sure that your directory has the following structure:
```
my_app/
    flask_app.py
    app/
        __init__.py
        routes.py
```
You may also see `__pycache__` in your folder - don't worry about this.

## Routes & Pages
In our code, notice the use of `@app.route("/"):` before our function definition. This is our way of telling the program to run the function we defined below when our URL is followed by just a forward slash. In other words, this is how we define __routes__ to access different __pages__. To see how this works, let's create a few sample routes. Take a few minutes and add two more routes, each with a function returning text. Then, re-run your application and navigate to those new routes!

Now that you have an idea of how routes work, we'll build some together. Initially, we just returned text for our routes. You can also return HTML, which we'll try here. Add a "workshop" route to your `routes.py` file with the following function definition:
```
@app.route("/workshop")
def workshop():
    return '''
<html>
    <head>
        <title>Workshops Page - My App</title>
    </head>
    <body>
        <h1>Latest Workshops will be Listed Below</h1>
    </body>
</html>'''
```

Run `flask run` again and navigate to <http://localhost:5000/workshop>. You should see the heading we just wrote.

## Templates
#### Basic Templating 

Now, let's say we had a list of Workshops that we wanted to display on our site, and that we had that list stored as a Python dictionary. We'd probably design our page like so:
```
@app.route("/workshop")
def workshop():
    pubs = ["NLP","Network Analysis", "Flask"]
    return '''
<html>
    <head>
        <title>Workshops Page - My App</title>
    </head>
    <body>
        <h1>Latest Workshops will be Listed Below</h1>
        <ul>
            <li>''' + pubs[0]+'''</li>
            <li>''' + pubs[1]+'''</li>
            <li>''' + pubs[2]+'''</li>
        </ul>
    </body>
</html>'''
```
This approach takes constant editing and isn't very user-friendly. Thankfully, Jinja2, a templating tool, links with Flask. This will allow us to create __templates__ for our pages so that they can update easily. We'll start by making a folder for our templates and creating our home and workshop templates - make sure you're in the `my_app` directory first.
```
$ mkdir app/templates
$ cd app/templates
$ touch home.html workshop.html
```
Templates allow us to write HTML and use specific placeholders for certain data. Then, when our template is __rendered__, we pass in the data we want to use and it's automatically formatted exactly how we planned. Place the following code in `workshop.html`:
```
<html>
    <head>
        <title>{{ data.title }} - My App </title>
    </head>
    <body>
        <h1>{{ data.heading }}</h1>
        <ul>
        {% for pub in data.pubs %}
            <li><a href="{{pub.link}}">{{ pub.title }}</a></li>
        {% endfor %}
        </ul>
    </body>
</html>
```
When we want to display an element from our data, we use double braces `{{ }}`. When we want to use logic, we use a brace paired with a percentage sign, `{% %}`.

Now, in order for this template to be rendered when navigating to the workshop page, we have to edit our `routes.py` file. Be sure to add `from flask import render_template` at the top, and then update your function definition for `workshop`:
```
def workshop():
    pubs = [{"title":"NLP", "link":"https://github.com/epmarie/IntroNLP"},
            {"title":"Network Analysis", "link":"https://github.com/epmarie/network_workshop"},
            {"title":"Flask", "link":"https://github.com/epmarie/flask_example_app"}]
    data = {"title": "workshop", "heading": "Latest Workshops", "pubs":pubs}
    return render_template('workshop.html', data=data)
```
Try re-running your site now - see how each Workshop is its own element in the list? Jinja took the data we provided and inserted it into the template we created.

#### Template Inheritance

Most websites have some sort of navigation bar and/or header at the top of every page. Instead of having to copy and paste the same HTML code into every single route, Jinja allows us to create one file that contains this code that we can add to every other page. Create a new file in the templates folder (either through your editor or through terminal) called `base.html`. Then, place the following code inside it:
```
<html>
  <head>
    {% if title %}
    <title>{{ title }}</title>
    {% else %}
    <title>Welcome to My App</title>
    {% endif %}
  </head>
  <body>
    <div>My App: <a href="/home">Home</a><a href="/workshop">workshop</a></div>
    <hr>
    {% block content %}{% endblock %}
  </body>
</html>
```

Notice the `{% block content %}{% endclock %}` line? This is where the code for each separate page will end up. To fill this, switch back to `workshop.html`, and replace the current code with the code below:
```
{% extends "base.html" %}
{% block content %}
    <h1>{{ data.heading }}</h1>
    <ul>
    {% for pub in data.pubs %}
        <li><a href="{{ pub.link }}"> {{pub.title}} </a></li>
    {% endfor %}
    </ul>
{% endblock %}
```
By doing this, we're telling our workshop page to _extend_ our base file. Now, if you reload your workshop page, you should see a header at the top with links to the home page and the workshop page.

### Exercise: Home Page
Now that you have some of the basics for creating a template and using template inheritance, create a `home.html` page and use it to extend the `base.html` template and show a page header and a quick welcome/description. Hint: remember to change your function in `routes.py`!

## Deploying to Python Anywhere

We've built a web application, learned how to use templates, and added some interactive graphics. Now it's time to deploy! We'll be using Python Anywhere, but there are many options (AWS, Heroku, etc.) to host your site. Navigate to <http://www.pythonanywhere.com/login> to log in (or create an account, if needed).

On the homepage, navigate to the __Web__ tab and select __"Add a new web app"__. We'll use the Flask setup (and we're running Python 3.6). Once the page loads, scroll down to the __Code__ section and select "Go to directory" for the _source directory_ - we'll come back to add files later.

Since you can only upload files one at a time (unless you're connecting to something like GitHub), we'll zip our entire folder, upload it, and then unzip it. In your Windows file manager, make sure you're in the `my_app` directory, then right-click `flask_app.py` and `app` and select "send to zipped folder" (named `mysite.zip`). Now, upload that zipped file to PythonAnywhere, and then click "Open Bash Console Here" at the top of the page. In _that_ console, run `unzip mysite.zip` (tedious, I know) and all your files should be stored on PythonAnywhere.

Navigate to your web app page once again, reload your site, and then navigate to the url provided (usually <<username>.pythonanywhere.com>). Ta-da! Your site should be up and running, just as it was locally.
	
For further reference on deployment options with flask, visit <http://flask.pocoo.org/docs/1.0/deploying/>.

## Adding Interactive Bokeh Graphics
Since we have our website up and funcitoning, let's take it a step further and add some interactive charts. To keep everything nice and isolated, we'll add a whole new page for this. Back in VSCode, start by adding a new route definition:
```
@app.route("/vbar", defaults={'days': 13})
@app.route("/vbar/<int:days>/")
def graphics(days):
    # TODO
    return("Coming soon!")
```

Before adding the definition, notice the part of the app route that asks for an _int_ value for _days_. This is a parameter passed through the URL to the function. We tell the application that we want an integer value, and we name it _days_ for use in the function. For example, if I wanted 5 days, I would navigate to `localhost:5000/vbar/5`. We set the default number of days to 13, in case someone navigates just to `localhost:5000/vbar`. We'll see how to do this shortly, but first, create a new template called `graphics.html`:
```
<link rel="stylesheet" href="https://cdn.pydata.org/bokeh/release/bokeh-0.13.0.min.css" type="text/css" />
<link rel="stylesheet" href="https://cdn.pydata.org/bokeh/release/bokeh-widgets-0.13.0.min.css" type="text/css" />
<script type="text/javascript" src="https://cdn.pydata.org/bokeh/release/bokeh-0.13.0.min.js"></script>
<script type="text/javascript" src="https://cdn.pydata.org/bokeh/release/bokeh-api-0.13.0min.js"></script>
<script type="text/javascript" src="https://cdn.pydata.org/bokeh/release/bokeh-widgets-0.13.0.min.js"></script>
{% extends 'base.html' %}
{% block content %}
	<h1>Bokeh VBar Chart using {{ data.days }} Days</h1>
    {{ data.div|safe }}
    {{ data.script|safe }}
{% endblock %}
```
Since we're using Bokeh to create the graphics, we need references to the package's javascript and CSS, hence the links at the beginning. Now that we have a template to return, we can update the function definition for our graphics page:
```
def graphics(days):
    days = 13 if days < 1 else days
    plot = create_bar_chart(days=days)
    script, div = components(plot)
    data = {"title":"Graphics", "heading":"Chart", "days":days, "div":div, "script":script}
    return render_template("graphics.html", data=data)
```
Depending on your text editor, you may see errors pop up regarding the `create_bar_chart()` and `components()` functions. Before we can use these functions, we must import them. `Components` comes directly from Bokeh, but `create_bar_chart` is something we (Alex) created. Copy and paste the file information into a new file (make sure it's in the `my_app` folder).

#### Check point
Before continuing, make sure that your directory has the following structure:
```
my_app/
    app/
        templates/
            base.html
            graphics.html
            home.html
            workshop.html
        __init__.py
        routes.py
    flask_app.py
    bokeh_vbar.py
    
```
(as before, you may also see `__pycache__` in your folders)

At the top of your `routes.py` file, add the following lines of code just below your `from app import app` line:
```
from bokeh.embed import components
from bokeh_vbar import create_bar_chart
```
Run your site and navigate to your new page. Try out a few different integer values (and try _not_ passing in a value) to ensure that your function is acting as intended.

## Exercise: Second Bokeh page
Now that you see how the first Bokeh graphics page, download `bokeh_calendar.py`. Using the functions we just wrote as an example, create a new route to display this calendar. Use the same graphics template we used before. Don't forget to update `base.html` - you may want to rename things! 

## Exercise: ReDeploy
Since we've added quite a few new features to our website, it's time to re-deploy. Even though all the changes you made show up when you run your site locally, the PythonAnywhere site has to be updated for those changes to show up. Using what you've learned, update your site! (Hint: instead of zipping everything, it might be easier to upload file by file, since you'll only need to upload what you've added or changed)
