from flask import Flask
from flask import redirect, render_template, request, session
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash
from psycopg2 import errors

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register_form.html")

@app.route("/register", methods=["POST"])
def register_send():
    username = request.form["username"]

    sql = "SELECT password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    

    if user:
        return redirect("/register")

    password = request.form["password"]

    hash_value = generate_password_hash(password)
    sql = "INSERT INTO users (username,password) VALUES (:username,:password)"
    db.session.execute(sql, {"username":username,"password":hash_value})
    db.session.commit()
    
    sql = "SELECT id ROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    

    session["username"] = username
    session["userid"] = user[0]
    return redirect("/")

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

    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    

    print(user)
    if user == None:
        # TODO: invalid username
        return redirect("login")
    else:
        hash_value = user[1]
        if check_password_hash(hash_value,password):
            session["username"] = username
            session["userid"] = user[0]
        else:
            # TODO: invalid password
            return redirect("/login")

    return redirect("/")


@app.route("/articles/<int:id>")
def get_article(id):
    if not "username" in session:
        return "not logged in"
    sql = """
        SELECT * FROM Users
        WHERE Users.id = :id
        """
    result = db.session.execute(sql, {"id": id})
    return str(result.fetchone())

@app.route("/articles")
def get_articles():
    result = db.session.execute("""
        SELECT 
            title, 
            author, 
            written, 
            url, 
            source, 
            created_at, 
            creator, 
            username 

        FROM articles, users 
        WHERE users.id = articles.creator
        """)
    print(result)
    res = result.fetchall()
    return render_template("index.html", entries=res)

@app.route("/articles/new", methods=["POST"])
def new_article_send():
    if not "username" in session:
        return redirect("/login")

    print("session:", session)
    form = request.form
    new = {}
    new["title"] = form["title"] 
    new["author"] = form["author"]
    new["written"] = form["written"]
    new["creator"] = session["userid"]
    print(new)
    if not new["written"]:
        new["written"] = None
    new["url"] = form["url"]
    new["source"] = form["content"]
    new["created_at"] = datetime.utcnow()
    new["hidden"] = False

    sql = """
        INSERT INTO articles (
            title, 
            author, 
            written, 
            url,
            source, 
            created_at, 
            creator, 
            hidden
        ) 
        VALUES (
            :title, 
            :author, 
            :written, 
            :url, 
            :source, 
            :created_at, 
            :creator, 
            :hidden
        )    
          """
    db.session.execute(sql, new)
    db.session.commit()
    print(request.form)
    return redirect("/articles")

@app.route("/articles/new")
def new_article():
    if not "username" in session:
        return redirect("/login")   
    return render_template("form_new_article.html")
