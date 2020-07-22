import requests as rq
from urllib import parse

from models.place import Place
from models.comment import Comment

from utils.crypto import encode_sha2


class Kakao():
  platform = 'Kakao'

  def __init__(self):
    pass

  async def start(self, store_name):
    print('platform: %s, store_name: %s'%(self.platform, store_name))
    store_infos = self.get_id(store_name)[0]
    place = Place(store_infos.get('confirmid', None), store_infos.get('name', None), store_infos.get('tel', ''), store_infos.get('address', ''), store_infos.get('img', ''))
    place.show()
    placeId = 0
    
    if store_infos.get('confirmid', None):
      print('[SAVE PLACE] store_name: %s'%(store_name))
      placeId = place.save()
    else:
      print('[UN SAVE] store_name: %s'%(store_name))
      return 

    comments = self.get_comments(placeId, store_name, place.siteId)
    for c in comments:
      c.save()

    print('[SAVE COMMENT] count: %d'%(len(comments)))

  def get_id(self, store_name):
  
    url = 'https://search.map.daum.net/mapsearch/map.daum?q=%s&msFlag=A&sort=0'
    res = rq.get(url%(store_name), headers={
      # 'Referer': url%(store_name),
      "Referer": "https://map.kakao.com/?q=%s"%(parse.quote(store_name)),
      "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
    })

    return  res.json().get('place', [])

  def get_comments(self, placeId, store_name, siteId):
    url ='https://place.map.kakao.com/commentlist/v/%s/%d?platform='
    page = 1
    
    comments = []

    while True:
      res = rq.get(url%(siteId, page), headers={
        # 'Referer': url%(store_name),
        "Referer": "https://map.kakao.com/?q=%s"%(parse.quote(store_name)),
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
      })
      data = res.json()
      is_exist = False
      res_comments = data.get('comment', {'list': []}).get('list', [])
      for item in res_comments:
        msg = item.get('contents', '').replace('\n', '').replace('\t', '').replace('\r', '').strip()
        commend_id = item.get('commentid', 0)
        if msg:
          C = Comment(
            placeId, siteId, self.platform,
            item.get('username', ''), encode_sha2(item.get('msg', '')), 
            item.get('msg', ''), item.get('point', 0)
          )

          is_exist = C.is_exist_comment()
          
          if not is_exist:
            comments.append(C)
          if is_exist:
            break
      
      if not len(res_comments) or is_exist:
        break
      
      page += 1

    return comments

def get_id(store_name):
  
  url = 'https://search.map.daum.net/mapsearch/map.daum?q=%s&msFlag=A&sort=0'
  res = rq.get(url%(store_name), headers={
    # 'Referer': url%(store_name),
    "Referer": "https://map.kakao.com/?q=%s"%(parse.quote(store_name)),
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
  })
  return res.json().get('place', [])

def get_comments(siteId):
  comments = []
  start_page = 1
  end_page = 6

  for page in range(start_page, end_page):
    url ='https://place.map.kakao.com/commentlist/v/%s/%d?platform='
    res = rq.get(url%(siteId, page), headers={})

    data = res.json()
    print('[PAEG] %d page'%(page))
    for item in data['comment']['list']:
      commend = item.get('contents', '').replace('\n', '').replace('\t', '').replace('\r', '').strip()

      commend and comments.append(commend)

  return comments

if __name__ == "__main__":
  ids = [item['confirmid'] for item in get_id('연남서식당')]
  comments = get_comments(ids[0])

  print(comments)