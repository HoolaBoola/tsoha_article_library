# tsoha-article-library

### What?

A web application which allows users to retrieve textual content from the internet and save it with their own comments.

  The end user can create an entry, whereupon the user is presented with a view that allows entering the usual metadata (author name, content, date...).

  Alternatively, the user can enter a link to an article, which the application will use to retrieve said article and do its best at extracting the contents.

  In addition to the article entries, a user is allowed to write their own comments and share their posts with other users. Other users will also be able to comment on the text.

### Current status

  At the moment, the following is possible:
  - Registering a new user
  - Logging in as an existing user
  - Creating a post
    - WYSIWYG (What You See Is What You Get) editor to edit HTML
    - Functionality to automatically load contents from a URL
  - Viewing a post
  - Viewing all posts
  - Logging out
  - Visual improvements
  - Editing + deleting posts
  - HTML sanitization
  - Posts listed newest-first and pagination works

### Todo

  - ~~Visual improvements~~
  - Noscript versions of JavaScript functionality
  - Refactoring
  - ~~Editing posts~~
  - Commenting on posts (we'll see)
  - Refactoring
  - ~~HTML sanitization fine tuning~~
  - ~~Posts listed newest-first and only a handful per page~~

### Testing in Heroku

  A running version of the project can be found at https://tsoha-article-library.herokuapp.com.

  On the initial page, you are presented with the option to register a user or to login. For registering in, you need a username and a password. Registering will also automatically log you in with the created account.

  When logged in, the user is presented with the option to post a new post ("Post a new article"). By entering the needed information and then submitting the form, you can send the post to the server.

  Existing posts can be found by going to "/articles" (this ~~will also later be possible~~ is now possible to view from the main page as well, or "/")

  Once there are more than 20 posts, "Next page" etc. links will appear at the bottom of the page.

  Creating a post can be done as follows:

  - Click "Post a new article". Several fields are now visible.
  - If you have an URL from which you wish to load textual content, write the address into the "URL" field. Then click "load article"
  - After a while, the application fills the fields with its best attempts at gathering the information.
  - Missing or incorrect information can then be edited
  - Once the post is in good shape, click "Send"

  You can delete or edit your own posts while logged in from the buttons visible beside the posts. Before deletion, the app will ask for your confirmation.

  You may view your own posts from the "My posts" button at the top row.

  Another user's posts can be viewed by clicking their username from a post (it's a link)

### Installation and running

Run the following commands in the git repository once you have cloned the project

- Create the virtual environment

  `python3 -m venv venv`

- Enter the virtual environment
  
  `source venv/bin/activate`

- Install the required dependencies

  `pip install -r requirements.txt`

- Add database information to environment file

  `echo 'DATABASE_URL="postgresql://user"' >> .env`

  **Note**: depending on the configuration of the PostgreSQL database on the local machine, `DATABASE_URL` might need to be in the following form

  `DATABASE_URL="postgresql://user:password@localhost:5432/db"`

- Create the neccessary database tables

  `psql < schema.sql`

- Create a secret key to use for storing sessions

  `echo "SECRET_KEY=$(openssl rand -base64 64)" >> .env`
  
  **Note**: secret keys can be created in many ways, [here](https://www.tecmint.com/generate-pre-shared-key-in-linux/) are some should the provided example not suffice

- Launch the application with

  `flask run`
