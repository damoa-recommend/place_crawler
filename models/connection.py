from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from config.config import get_config 

import sys, traceback

c = get_config()
c = c['database']

DATABASE_TYPE = c['DATABASE_TYPE']
USER = c['USER']
PASSWORD = c['PASSWORD']
HOST = c['HOST']
PORT = c['PORT']
DATABASE = c['DATABASE']

engine = create_engine(
  '%s://%s:%s@%s:%s/%s'%(DATABASE_TYPE, USER, PASSWORD, HOST, PORT, DATABASE),
  # echo=True, 
  pool_recycle=20,
  pool_size=30
)

db_session = scoped_session(
  sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

Base = declarative_base()
Base.query = db_session.query_property()

@contextmanager
def session_scope(noti_push, noti_error):
  # session = scoped_session(
  #   sessionmaker(autocommit=False, autoflush=False, bind=engine)
  # )
  session = db_session
  # session = get_session()
  
  try:
    yield session
    session.commit()
    print('commit')
  except Exception as err:
    session.rollback()
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print("*** print_tb:")
    traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
    print("*** print_exception:")
    # exc_type below is ignored on 3.5 and later
    traceback.print_exception(exc_type, exc_value, exc_traceback,
                              limit=2, file=sys.stdout)
    print('rollback')
    raise
  finally:
    session.close()
    print('close')