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
    articles = user.get_articles()
    return render_template("index.html", entries=articles)

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


@app.route("/articles/u/<int:id>")
def get_articles_by_user(id):
    sql = """
        SELECT * FROM Users
        WHERE Users.id = :id
        """
    result = db.session.execute(sql, {"id": id})
    return str(result.fetchone())

@app.route("/articles/post/<int:id>")
def get_article(id):
    return redirect("/")

@app.route("/articles")
def get_articles():
    return redirect("/")

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

    return redirect("/")

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

    downloaded = trafilatura.fetch_url(url)
    result = trafilatura.extract(downloaded, date_extraction_params={"extensive_search": True, "original_date": True}, with_metadata=True, include_formatting=True)
    if not result:
        return ""
    return str(result) 
