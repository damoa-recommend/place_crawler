# 장소 검색후 비슷한 여행지 정보

class Relation:

  def __init__(self, id, name, link):
    self.id = id
    self.name = name
    self.link = link

  def show(self):
    print('id: {id}, name: {name}, link: {link}'.format(
      id=self.id,
      name=self.name,
      link=self.link
    ))