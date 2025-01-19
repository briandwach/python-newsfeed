import pymysql
pymysql.install_as_MySQLdb()

from os import getenv
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import g
from dotenv import load_dotenv


load_dotenv()

# Fetch the CA certificate from the environment variable
ssl_args = {
    'ssl_ca': getenv('DB_SSL_CA')  # Fetch the certificate from environment variable
}

# Connect to the database using the environment variable for the URL
engine = create_engine(
    getenv('DB_URL'),
    echo=True,
    pool_size=20,
    max_overflow=0,
    connect_args={'ssl': ssl_args}
)
Session = sessionmaker(bind=engine)
Base = declarative_base()

def init_db(app):
    Base.metadata.create_all(engine)
    app.teardown_appcontext(close_db)

def get_db():
    if 'db' not in g:
        # store db connection in app context
        g.db = Session()

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
