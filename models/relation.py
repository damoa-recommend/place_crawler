# 장소 검색후 비슷한 여행지 정보
from sqlalchemy import Column, Integer, String, Numeric, DateTime, DateTime, Time, DECIMAL, Text, Float

from models.connection import Base
from models.connection import session_scope
from models.connection import db_session

class Relation(Base):
  __tablename__ = "Relations"
  id = Column(Integer, primary_key=True)

  placeId = Column(Integer)
  name = Column(String)
  link = Column(Text)
  siteId = Column(String)

  def __init__(self, placeId, name, link, siteId):
    self.placeId = placeId
    self.name = name
    self.link = link
    self.siteId = siteId

  def show(self):
    print('placeId: {placeId}, name: {name}, link: {link}'.format(
      placeId=self.placeId,
      name=self.name,
      link=self.link
    ))

  def save(self):
    is_exist_relation = self.is_exist_relation()
    is_exist_place = self.is_exist_place()

    if (not is_exist_relation) and (not is_exist_place):
      with session_scope('push', 'error') as session:
        session.add(self)

  def is_exist_relation(self):
    sql = '''
      SELECT 
        id 
      FROM 
        Relations
      WHERE
        siteId='{siteId}'
    '''

    return db_session.execute(sql.format(
      siteId=self.siteId
    )).fetchone()

  def is_exist_place(self):
    sql = '''
      SELECT 
        id 
      FROM 
        Places
      WHERE
        name='{name}'
    '''

    return db_session.execute(sql.format(
      name=self.name
    )).fetchone()