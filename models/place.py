from sqlalchemy import Column, Integer, String, Numeric, DateTime, DateTime, Time, DECIMAL, Text

from models.connection import Base
from models.connection import session_scope
from models.connection import db_session

class Place(Base):
  __tablename__ = "Places"
  id       = Column(Integer, primary_key=True, autoincrement=True)
  name     = Column(String)
  tel      = Column(String)
  address  = Column(String)
  img      = Column(Text)

  def __init__(self, placeId, name, tel, address, img):
    self.placeId = placeId
    self.name = name
    self.tel = tel
    self.address = address
    self.img = img

  def show(self):
    print('placeId: {placeId}, name: {name}, tel: {tel}, addr: {address}, img: {img}'.format(
        placeId=self.placeId,
        name=self.name,
        tel=self.tel,
        address=self.address,
        img=self.img
    ))

  def save(self):
    is_exist = self.is_exist_place()
    
    if not is_exist:
      with session_scope('push', 'error') as session:
        session.add(self)

  def is_exist_place(self):
    sql = '''
      SELECT 
        id 
      FROM 
        Places
      WHERE
        name='{place_name}'
    '''
    return db_session.execute(sql.format(place_name=self.name)).fetchone()
