# tsoha-article-library

### What?

A web application which allows users to retrieve textual content from the internet and save it with their own comments.

  The end user can create an entry, whereupon the user is presented with a view that allows entering the usual metadata (author name, content, date...).

  Alternatively, the user can enter a link to an article, which the application will use to retrieve said article and do its best at extracting the contents.

  In addition to the article entries, a user is allowed to write their own comments and share their posts with other users. Other users will also be able to comment on the text.


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
