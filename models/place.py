class Place:
  
  def __init__(self, id, name, tel, address, img):
    self.id = id
    self.name = name
    self.tel = tel
    self.address = address
    self.img = img

  def show(self):
    print('id: {id}, name: {name}, tel: {tel}, addr: {address}, img: {img}'.format(
      id=self.id,
      name=self.name,
      tel=self.tel,
      address=self.address,
      img=self.img
    ))