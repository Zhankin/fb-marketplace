import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

ssl_args = {'ssl_ca': '/etc/ssl/cert.pem'}
url = url = "mysql+pymysql://{0}:{1}@{2}/{3}".format(
    os.environ['USERNAME'], os.environ['PASSWORD'], os.environ['HOST'], os.environ['DATABASE']
)
engine = create_engine(url, connect_args=ssl_args)
# create a configured "Session" class
Session = sessionmaker(bind=engine)

Base = declarative_base()
