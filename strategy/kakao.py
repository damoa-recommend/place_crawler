import requests as rq
from urllib import parse
from models.place import Place

class Kakao():
  platform = 'Kakao'

  def __init__(self):
    pass

  async def start(self, store_name):
    print('platform: %s, store_name: %s'%(self.platform, store_name))
    store_infos = self.get_id(store_name)[0]
    
    place = Place(store_infos['confirmid'], store_infos['name'], store_infos['tel'], store_infos['address'], store_infos['img'])
    place.show()
    commends = self.get_commends(place.id)
    print(len(commends), commends)

  def get_id(self, store_name):
  
    url = 'https://search.map.daum.net/mapsearch/map.daum?q=%s&msFlag=A&sort=0'
    res = rq.get(url%(store_name), headers={
      # 'Referer': url%(store_name),
      "Referer": "https://map.kakao.com/?q=%s"%(parse.quote(store_name)),
      "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
    })
    return  res.json().get('place', [])

  def get_commends(self, store_id):
    url ='https://place.map.kakao.com/commentlist/v/%s/%d?platform='
    start_page = 1
    end_page = 3
    commends = []

    for page in range(start_page, end_page):
      res = rq.get(url%(store_id, page))
      data = res.json()

      for item in data.get('comment', {'list': []}).get('list', []):
        msg = item.get('contents', '').replace('\n', '').replace('\t', '').replace('\r', '').strip()
        commend_id = item.get('commentid', 0)

        msg and commends.append({'msg': msg, 'id': commend_id})

    return commends

def get_id(store_name):
  
  url = 'https://search.map.daum.net/mapsearch/map.daum?q=%s&msFlag=A&sort=0'
  res = rq.get(url%(store_name), headers={
    # 'Referer': url%(store_name),
    "Referer": "https://map.kakao.com/?q=%s"%(parse.quote(store_name)),
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
  })
  return res.json().get('place', [])

def get_commends(store_id):
  commends = []
  start_page = 1
  end_page = 6

  for page in range(start_page, end_page):
    url ='https://place.map.kakao.com/commentlist/v/%s/%d?platform='
    res = rq.get(url%(store_id, page))

    data = res.json()
    print('[PAEG] %d page'%(page))
    for item in data['comment']['list']:
      commend = item.get('contents', '').replace('\n', '').replace('\t', '').replace('\r', '').strip()

      commend and commends.append(commend)

  return commends

if __name__ == "__main__":
  ids = [item['confirmid'] for item in get_id('연남서식당')]
  commends = get_commends(ids[0])

  print(commends)