from db import db
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

def new_user(username: str, password: str):
    sql = """
        SELECT password
        FROM Users
        WHERE username=:username
        """
    result = db.session.execute(sql, {"username": username})

    # username already taken
    if result.fetchone():
        return (False, "Username already taken")

    hash_value = generate_password_hash(password)
    sql = """
        INSERT INTO Users (username, password)
        VALUES(:username, :password)
        RETURNING id
        """

    result = db.session.execute(sql, {"username": username, "password":hash_value})
    identity = result.fetchone()[0]
    result = db.session.commit()
    return (True, "ok", identity)


def login(username: str, password: str):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    

    if user != None:

        hash_value = user[1]
        if check_password_hash(hash_value, password):
            # correct credentials
            return (True, "Logged in", user[0])

    return (False, "Wrong username or password")

def new_post(title, author, written, creator, url, created_at, hidden, content):
    post = {}
    post["title"] = title
    post["author"] = author
    post["written"] = written
    post["creator"] = creator
    post["url"] = url
    post["source"] = source
    post["created_at"] = created_at
    post["hidden"] = hidden
    post["content"] = content
    return new_post(post)

def new_post(post):
    print(post)
    sql = """
        INSERT INTO articles (
            title, 
            author, 
            written, 
            url,
            content,
            created_at, 
            creator, 
            hidden
        ) 
        VALUES (
            :title, 
            :author, 
            :written, 
            :url, 
            :content,
            :created_at, 
            :creator, 
            :hidden
        )    
          """
    db.session.execute(sql, post)
    db.session.commit()

    return True

def get_article(id: int):
    sql = """
        SELECT * FROM Articles, Users
        WHERE Articles.id=:id
        """
    result = db.session.execute(sql)
    result = result.fetchone()
    print(result)
    

def get_articles():
    result = db.session.execute("""
        SELECT
            articles.id,
            title, 
            author, 
            written, 
            url, 
            content, 
            created_at, 
            creator, 
            username,
            users.id

        FROM articles, users 
        WHERE users.id = articles.creator
        """)
    res = result.fetchall()
    articles = []
    for row in res:
        article = result_to_article(row)
        articles.append(article)
    print(articles[0])
    return articles

def result_to_article(res):
    article = {}
    article["id"] = res[0]
    article["title"] = res[1]
    article["author"] = res[2]
    article["written"] = res[3]
    article["url"] = res[4]
    article["content"] = res[5]
    article["created_at"] = res[6]
    article["creator"] = res[7]
    article["username"] = res[8]
    article["posterid"] = res[9]
    return article

