from flask import Flask
from flask import redirect, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/articles/new", methods=["POST"])
def new_article_send():
    form = request.form
    new = {}
    new["written"] = form["written"]
    new["author"] = form["author"]
    new["url"] = form["url"]
    print(request.form)
    return redirect("/articles/new")

@app.route("/articles/new")
def new_article():
    return render_template("form_new_article.html")
