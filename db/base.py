import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

url = url = "mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
    os.environ['DB_USER'], os.environ['DB_PASSWORD'], os.environ['DB_HOST'], os.environ['DB_PORT'],
    os.environ['DB']
)
engine = create_engine(url)
# create a configured "Session" class
Session = sessionmaker(bind=engine)

Base = declarative_base()
