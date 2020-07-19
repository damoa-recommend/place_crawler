import requests as rq
from bs4 import BeautifulSoup
from urllib import parse
from urllib.parse import urlparse, parse_qs, parse_qsl
from models.place import Place


class Naver():
  platform = 'Naver'

  def __init__(self):
    pass

  async def start(self, store_name):
    print('platform: %s, store_name: %s'%(self.platform, store_name))
    store_infos = self.get_id(store_name)
    place = Place(store_infos['id'], store_infos['name'], store_infos["tel"], store_infos['address'], store_infos['img'])
    place.show()

  def get_id(self, store_name):
  
    url = "https://store.naver.com/restaurants/detail?entry=plt&id=11708756&query=%s&tab=receiptReview&tabPage=0"
    res = rq.get(url%(store_name), headers={
      'Referer': url%(parse.quote(store_name)),
      "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
    })
    
    soup = BeautifulSoup(res.content, 'lxml')
    
    link = soup.select('a.link')
    query_parsed = urlparse(link[0].get('href'))
    store_id=parse_qs(query_parsed.query)['id'][0]

    return {
      "id": store_id,
      "name": soup.select('#content .biz_name_area strong.name')[0].text,
      "tel": soup.select('#content .list_item_biztel div.txt')[0].text,
      "address": soup.select('#content .list_item_address span.addr')[0].text,
      "img": soup.select('a.naver-splugin')[0].get('data-kakaotalk-image-url')
    }

if __name__ == "__main__":
  # id 가져오기
  # BASE_URL = "https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=%s"
  # res = rq.get(BASE_URL%('연남서식당'))
  # soup = BeautifulSoup(res.content, 'lxml')

  # a = soup.select('.api_more_theme')[0].get('href')
  # print(a)

  # # 기본정보 
  BASE_URL = "https://store.naver.com/restaurants/detail?entry=plt&id=11708756&query=%s&tab=receiptReview&tabPage=0"
  res = rq.get(BASE_URL%('연남서식당'))
  soup = BeautifulSoup(res.content, 'lxml')

  link = soup.select('a.link')

  # for i in soup.select('.list_bizinfo > .list_item'):
  #   print(i.text)

  query_parsed = urlparse(link[0].get('href'))
  store_id=parse_qs(query_parsed.query)['id'][0]

  # 댓글 가져오기
  BASE_URL="https://store.naver.com/restaurants/detail?entry=plt&id=%s&query=%s&tab=receiptReview&tabPage=2"
  res = rq.get(BASE_URL%(store_id, '연남서식당'))
  soup = BeautifulSoup(res.content, 'lxml')

  reviews = soup.select('.list_receipt_review li')

  for review in reviews:
    print(review.select('.review_txt')[0].text)