import requests as rq 
from bs4 import BeautifulSoup
from urllib import parse
from utils.crypto import encode_sha2

##############################
# store_name= '연남서식당'
# search_url = 'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=%s'
# res = rq.get(search_url%(store_name), headers={
#   'Referer': search_url%(parse.quote(store_name)),
#   "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
# })  

# soup =BeautifulSoup(res.content, 'lxml')
# print(soup.select('.api_more_theme'))
# print()
# print(soup.select('#place_main_ct .biz_name_area .biz_name'))
# print(soup.select('#place_main_ct .list_item_biztel div.txt'))
# print(soup.select('#place_main_ct .list_item_address span.addr'))
# print(soup.select('#place_main_ct .top_photo_area img'))

##########################
# commends = []
# start_page = 1
# end_page = 6
# store_id = 8128910

# for page in range(start_page, end_page):
#   url ='https://place.map.kakao.com/commentlist/v/%s/%d?platform='
#   res = rq.get(url%(store_id, page), headers={})

#   data = res.json()
#   print(data)
#   print('[PAEG] %d page'%(page))
#   for item in data['comment']['list']:
#     commend = item.get('contents', '').replace('\n', '').replace('\t', '').replace('\r', '').strip()

#     commend and commends.append(commend)

#############
import time

store_id = '13513620' 
# 덕수궁돌담길(13513620), 서울중앙시장(13304246), 카페 할아버지공장(1425989301), 비아37(11853181) => 등 json decode 에러
page = 1
display = 10
url = "https://store.naver.com/sogum/api/receiptReviews?businessId=%s&page=%d&display=%d"

while True:
  res = rq.get(url%(store_id, page, display), headers = {
    'Referer': 'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=%EC%97%B0%EB%82%A8%EC%84%9C%EC%8B%9D%EB%8B%B9&',
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
  })
  print(res.text)
  d = res.json()

  res_comments = d.get('items', [])
  print('============== %d page =============='%(page))
  for c in res_comments:
    print('h: %s, author: %s, body: %s'%(encode_sha2(c['body']), c['authorId'], c['body'], ))
  
  time.sleep(0.6)
  page += 1

# print('😪😭')