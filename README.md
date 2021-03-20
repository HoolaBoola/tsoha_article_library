# tsoha-article-library

### What?

A web application which allows users to retrieve textual content from the internet and save it with their own comments.


### Installation and running

Run the following commands in the git repository once you have cloned the project

- Create the virtual environment

  `python3 -m venv venv`

- Enter the virtual environment
  
  `source venv/bin/activate`

- Install the required dependencies

  `pip install -r requirements.txt`

- Create the file `.env` to store environment variables and add the following line

  `DATABASE_URL="postgresql://user"`

  **Note**: depending on the configuration of the PostgreSQL database on the local machine, `DATABASE_URL` might need to be in the following form

  `DATABASE_URL="postgresql://user:password@localhost:5432/db"`

- Create the neccessary database tables

  `psql < schema.sql`

- Launch the application with

  `flask run`
