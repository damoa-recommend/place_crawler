class Comment:

  def __init__(self, placeId, siteId, platform,  author, contextHash, content, grade):
    self.hash = hash
    self.placeId = placeId # Places 테이블의 id
    self.id = siteId       # 사이트에 표시된 장소 id
    self.platform = platform
    self.author = author
    self.contextHash = contextHash

    self.content = content
    self.grade = grade

  def show(self):
    pass