import logging
from soupsieve import escape
from sqlalchemy import create_engine
import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import DropTable
from sqlalchemy.ext.compiler import compiles

# LOGGING
logger = logging.getLogger()

logger.setLevel(logging.ERROR)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.disabled = True

def create_database(database_name):
    try:
        e = create_engine("postgresql://postgres:secret@localhost:5432/")
        conn = e.connect()
        conn.execute("commit")
        conn.execute(f'CREATE DATABASE {database_name}')
        conn.close()
    except Exception as e:
        logger.error(e)
        logger.error("|-| Error creating database...")
        pass

try:
    DB_NAME = "formshunterdb"
    Base = declarative_base()
    create_database(DB_NAME)
    engine = create_engine("postgresql://postgres:secret@localhost:5432/" + DB_NAME)
    
    Session = sessionmaker(bind=engine)
except Exception as e:
    print("|-| Error connecting to database... 🕯️")
    logger.error(e)
    pass

def add_item_to_items_table(sess, item):
    with engine.connect() as conn:
        sess.add(item)
        try:
            sess.commit()
            return True
        
        except Exception as e:
            pass

def check_if_row_exists(sess, table):
    with engine.connect() as conn:
        q = f"SELECT {table.id} AS id FROM {table.__tablename__} WHERE url = '{table.url}' AND "
        print(f'{table.url}')
        r = conn.execute(q)
        sess.commit()
        return r.all()

