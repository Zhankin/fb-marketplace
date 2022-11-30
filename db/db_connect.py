import os
from sqlalchemy import create_engine
import pandas as pd


def get_connection():
    return create_engine(
        url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
            os.environ['DB_USER'], os.environ['DB_PASSWORD'], os.environ['DB_HOST'], os.environ['DB_PORT'],
            os.environ['DB']
        )
    )


def create_table(db, table):
    db.execute("""
    CREATE TABLE IF NOT EXISTS {} (
        ad_price varchar(255),
        ad_name varchar(255),
        ad_image_link text,
        ad_link text
    );
    """.format(table))


def db_connect(table_name):
    sql_engine = get_connection()
    db_connection = sql_engine.connect()
    create_table(sql_engine, table_name)
    return db_connection


def close_db(db):
    db.close()


def save_df(df, db, table_name):
    df.to_sql(table_name, db, if_exists='append', index=False)


def read_from_db(db, table_name):
    return pd.read_sql("select * from {}".format(table_name), db)
