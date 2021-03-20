from flask import Flask
from flask import redirect, render_template, request
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/articles")
def get_articles():
    result = db.session.execute("SELECT name, author, written, url, source, created_at, creator, username FROM articles, users WHERE users.id = articles.creator")
    print(result.fetchall())
    return render_template("index.html")

@app.route("/articles/new", methods=["POST"])
def new_article_send():
    form = request.form
    new = {}
    new["name"] = "test article"
    new["author"] = form["author"]
    new["written"] = form["written"]
    new["url"] = form["url"]
    new["source"] = form["content"]
    new["created_at"] = datetime.utcnow()
    new["creator"] = 2
    new["hidden"] = False

    sql = """
        INSERT INTO articles (name, author, written, url, source, created_at, creator, hidden) 
            VALUES (:name, :author, :written, :url, :source, :created_at, :creator, :hidden)    
          """
    db.session.execute(sql, new)
    db.session.commit()
    print(request.form)
    return redirect("/articles/new")

@app.route("/articles/new")
def new_article():
    return render_template("form_new_article.html")
