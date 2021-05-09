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

from html_sanitizer import Sanitizer
sanitizer = Sanitizer({
    "tags": {
        "a", "h1", "h2", "h3", "strong", "em", "p", "ul", "ol",
        "li", "br", "sub", "sup", "hr",
        },
    "attributes": {"a": ("href", "name", "target", "title", "id", "rel")},
    "empty": {"hr", "a", "br"},
    "separate": {"a", "p", "li"},
    "whitespace": {"br"},
    "keep_typographic_whitespace": True,
    "add_nofollow": True,
    "autolink": False,
    "element_postprocessors": [],
    "is_mergeable": lambda e1, e2: True,
    }) 

def new_post(post):
    post["content"] = sanitizer.sanitize(post["content"])
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
        SELECT
            articles.id,
            title, 
            author, 
            written, 
            url, 
            content, 
            created_at, 
            creator, 
            username

        FROM Articles
        JOIN Users ON
            Users.id = Articles.creator
        WHERE articles.id = :id AND hidden = false
        """
    result = db.session.execute(sql, {"id": id})
    result = result.fetchone()
    result = result_to_article(result)
    result["content"] = sanitizer.sanitize(result["content"])
    return result

def get_articles_by_user(user_id):
    sql = """
        SELECT username FROM Users
        WHERE id=:id
        """
    result = db.session.execute(sql, {"id": user_id})
    username = result.fetchone()[0]
    if not username:
        return ("No such user", False)

    sql = """
        SELECT 
            articles.id,
            title,
            author,
            written,
            url,
            content,
            created_at,
            creator
        FROM Articles
        WHERE 
            creator = :user_id
            AND
            hidden = false
        ORDER BY created_at DESC
        """
    result = db.session.execute(sql, {"user_id": user_id})
    articles = []
    for row in result:
        articles.append(result_to_article(row))

    return (articles, username)

def get_articles(page = 0):
    page_size = 20
    sql = """
        SELECT Count(*) FROM Articles
        """
    result = db.session.execute(sql)
    count = int(result.fetchone()[0])
    
    last_page = (count + page_size) // page_size - 1
    if page_size * page > count + page_size: 
        page = last_page 
    
    sql = """
        SELECT
            articles.id,
            title, 
            author, 
            written, 
            url, 
            content, 
            created_at, 
            creator, 
            username
        FROM articles, users 
        WHERE users.id = articles.creator AND hidden = false
        ORDER BY created_at DESC
        LIMIT :page_size
        OFFSET :articles
        """
    result = db.session.execute(sql, {"page_size": page_size, "articles": page*page_size})
    res = result.fetchall()
    articles = []
    for row in res:
        article = result_to_article(row)
        articles.append(article)
    return (articles, count, last_page, page)

def result_to_article(res):
    article = {}
    article["id"] = res[0]
    article["title"] = res[1]
    article["author"] = res[2]
    article["written"] = res[3]
    article["url"] = res[4]
    article["content"] = res[5]
    article["created_at"] = res[6]
    article["creator"] = int(res[7])

    if len(res) > 8:
        article["username"] = res[8]
    return article

from trafilatura import extract, fetch_url
import xml.etree.ElementTree as ET
def trafilatura_get_contents(url):
    downloaded = fetch_url(url)
    result = extract(downloaded, output_format="xml")

    if not result:
        return None

    root = ET.fromstring(result)
    date = root.get("date")
    excerpt = root.get("excerpt")
    sitename = root.get("sitename")
    title = root.get("title")
    main = root.find("main")

    content = ET.tostring(main, encoding="utf-8").decode("utf-8").replace("<main>", "").replace("</main>", "")
    return {"date": date, "excerpt": excerpt, "sitename": sitename, "title": title, "content": content}

def delete_article(id):
    sql = """
        UPDATE Articles
        SET hidden = true
        WHERE id=:id
        """
    db.session.execute(sql, {"id": id})
    db.session.commit()
