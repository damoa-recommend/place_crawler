from sqlalchemy import Column, Integer, String, Numeric, DateTime, DateTime, Time, DECIMAL, Text, Float

from models.connection import Base
from models.connection import session_scope
from models.connection import db_session

class Comment(Base):
  __tablename__ = "Comments"

  placeId = Column(Integer)

  platform = Column(String, primary_key=True)
  siteId = Column(String, primary_key=True)
  author = Column(String, primary_key=True)
  content = Column(String)

  contentHash =Column(String, primary_key=True)
  grade = Column(Float)

  def __init__(self, placeId, siteId, platform,  author, contentHash, content, grade):
    self.placeId = placeId # Places 테이블의 id
    
    self.platform = platform
    self.siteId = siteId       # 사이트에 표시된 장소 id
    self.author = author
    self.content = content
    
    self.contentHash = contentHash

    self.grade = grade


  def show(self):
    pass

  def save(self):
    with session_scope('push', 'error') as session:
      session.add(self)

  def is_exist_comment(self):
    sql = '''
      SELECT 
        platform, siteId, author, contentHash
      FROM 
        Comments
      WHERE
        platform='{platform}'
        AND siteId='{siteId}'
        AND author='{author}'
        AND contentHash='{contentHash}'
    '''
    return db_session.execute(sql.format(
      platform=self.platform,
      siteId=self.siteId,
      author=self.author,
      contentHash=self.contentHash,
    )).fetchone()