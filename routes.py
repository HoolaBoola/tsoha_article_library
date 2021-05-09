import trafilatura
from app import app

from flask import redirect, render_template, request, session
from flask import render_template
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from psycopg2 import errors

import user

@app.route("/")
def index():
    result = user.get_articles()
    articles = result[0]
    last_page = result[2]
    return render_template("index.html", entries=articles, page=0, last_page=last_page)

@app.route("/register")
def register():
    return render_template("register_form.html")

@app.route("/register", methods=["POST"])
def register_send():
    username = request.form["username"]
    password = request.form["password"]

    result = user.new_user(username, password)
    if result[0]:
        session["username"] = username
        session["userid"] = result[2]
        return redirect("/")
    print(result[1])
    return render_template("register_form.html", error_msg=result[1])

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/login")
def login():
    return render_template("login_form.html")

@app.route("/login", methods=["POST"])
def login_send():
    username = request.form["username"]
    password = request.form["password"]

    result = user.login(username, password)

    if result[0]:
        session["username"] = username
        session["userid"] = result[2]
        return redirect("/")

    return render_template("login_form.html", error_msg=result[1])


@app.route("/user/<int:id>")
def get_articles_by_user(id):
    result = user.get_articles_by_user(id)
    if result[1] == False:
        return render_template("error.html", msg="User not found")

    return render_template("user.html", articles=result[0], username=result[1])


@app.route("/articles")
def get_articles():
    page = int(request.args.get("page"))
    if not page:
        return redirect("/")
    result = user.get_articles(page)
    articles = result[0]
    last_page = result[2]
    page = result[3]
    return render_template("index.html", entries=articles, page=page, last_page=last_page)

@app.route("/articles/new", methods=["POST"])
def new_article_send():
    if not "username" in session:
        return redirect("/login")

    form = request.form
    new = {}
    new["title"] = form["title"] 
    new["author"] = form["author"]
    new["written"] = form["written"]
    new["creator"] = session["userid"]
    if not new["written"]:
        new["written"] = None
    new["url"] = form["url"]
    new["content"] = form["content"]
    new["created_at"] = datetime.utcnow()
    new["hidden"] = False

    if user.new_post(new):
        return redirect("/")

    return render_template("error.html", msg="Something strange happened. Please try again.")

@app.route("/articles/new")
def new_article():
    if not "username" in session:
        return redirect("/login")   

    return render_template("form_new_article.html")

@app.route("/articles/new/get_contents_from_url", methods=["POST", "GET"])
def get_contents_from_url():

    url = request.args.get("url")
    if not url:
        return ""

    result = user.trafilatura_get_contents(url)
    if not result:
        return ""

    return result

@app.route("/articles/post/<int:id>")
def get_article(id):
    res = user.get_article(id)
    return render_template("post.html", entry=res)

@app.route("/articles/delete/<int:id>")
def delete_article(id):
    article = user.get_article(id)
    if article["creator"] != session["userid"]:
        return render_template("error.html", msg="You are not authorized to do this!")
    return render_template("delete_confirmation.html", post_id=id)

@app.route("/articles/delete/<int:id>", methods=["POST"])
def delete_after_confirmation(id):
    article = user.get_article(id)
    if article["creator"] != session["userid"]:
        return render_template("error.html", msg="You are not authorized to do this!")

    if request.form["delete"]:
        user.delete_article(id)

    return redirect("/") 

@app.route("/articles/edit/<int:id>")
def edit_article(id):
    article = user.get_article(id)
    if article["creator"] != session["userid"]:
        return render_template("error.html", msg="You are not authorized to do this!")
    return redirect("/")
