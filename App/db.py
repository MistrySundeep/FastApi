import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DB_URL = 'postgresql://postgres:ipr1smData@localhost:5432/AddressData'
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

conn_str = "host='localhost' dbname='AddressData' user='postgres' password='ipr1smData'"
conn = psycopg2.connect(conn_str)
