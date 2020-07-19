import requests as rq
from bs4 import BeautifulSoup
import pandas as pd

class Google():
  platform = 'Google'

  def __init__(self):
    self.headers = {
      "x-client-data": "CIe2yQEIorbJAQjEtskBCKmdygEImbXKAQjnxsoBCOfIygEY/LfKARibvsoB"  
    }
    self.base_url = "https://www.google.com/search?sxsrf=ALeKk01COuuenXKUCw4AJH63_gPCN68zoQ:1593908289542&q=%s&stick=H4sIAAAAAAAAAONgFuLWT9c3LCssSSmsSFNC5mipZSdb6ZcUJZal5uiX5JcWZRaXxCeWAAWSSzLz86yKM1NSyxMrixex8rydOuN114xXm7e-mT1hBysjAOkzRqtWAAAA&sa=X&ved=2ahUKEwib_5uL67TqAhXG7GEKHR9zChYQzTooATAnegQIERAC&biw=1496&bih=859&dpr=1"

  async def start(self, store_name):
    print('platform: %s, store_name: %s'%(self.platform, store_name))

if __name__ == "__main__":
  df = pd.read_csv('../data/places.csv')
  for i, row in df.iterrows():
    url = "https://www.google.com/search?sxsrf=ALeKk01COuuenXKUCw4AJH63_gPCN68zoQ:1593908289542&q=%s&stick=H4sIAAAAAAAAAONgFuLWT9c3LCssSSmsSFNC5mipZSdb6ZcUJZal5uiX5JcWZRaXxCeWAAWSSzLz86yKM1NSyxMrixex8rydOuN114xXm7e-mT1hBysjAOkzRqtWAAAA&sa=X&ved=2ahUKEwib_5uL67TqAhXG7GEKHR9zChYQzTooATAnegQIERAC&biw=1496&bih=859&dpr=1"
    headers = {
      # "x-client-data": "CIe2yQEIorbJAQjEtskBCKmdygEImbXKAQjnxsoBCOfIygEY/LfKARibvsoB"
    }

    res = rq.get(url%(row['name']), headers=headers)
    soup = BeautifulSoup(res.content, 'lxml')

    name = row['name']
    tel = soup.select('.vbShOe span')[-1].text
    address = soup.select('.vbShOe span')[2].text
    img =  soup.select('g-img')
    print(img)
    print('장소이름: %s, 전화번호: %s, 주소: %s, 이미지: %s'%(row['name'], tel, address, img))
