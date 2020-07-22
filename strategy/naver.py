import requests as rq
from bs4 import BeautifulSoup
from urllib import parse
from urllib.parse import urlparse, parse_qs, parse_qsl

from models.place import Place
from models.comment import Comment

from utils.crypto import encode_sha2

class Naver():
  platform = 'Naver'

  def __init__(self):
    pass

  async def start(self, store_name):
    print('platform: %s, store_name: %s'%(self.platform, store_name))
    store_infos = self.get_id(store_name)
    place = Place(store_infos['id'], store_infos['name'], store_infos["tel"], store_infos['address'], store_infos['img'])
    place.show()
    placeId = 0

    if store_infos['id']:
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
    search_url = 'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=%s'
    res = rq.get(search_url%(store_name), headers={
      'Referer': search_url%(parse.quote(store_name)),
      "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
    })
    soup = BeautifulSoup(res.content, 'lxml')
    
    if len(soup.select('a.api_more_theme')) and soup.select('a.api_more_theme')[0].get('href').find('store.naver.com')> -1:
      store_id = parse_qs(soup.select('a.api_more_theme')[0].get('href'))['id'][0]
      name_dom = soup.select('#place_main_ct .biz_name_area .biz_name')
      tel_dom = soup.select('#place_main_ct .list_item_biztel div.txt')
      address_dom = soup.select('#place_main_ct .list_item_address span.addr')
      img_dom = soup.select('#place_main_ct .top_photo_area img')

      return {
        "id": store_id ,
        "name": len(name_dom) and name_dom[0].text,
        "tel": len(tel_dom) and tel_dom[0].text,
        "address": len(address_dom) and address_dom[0].text,
        "img": len(img_dom) and img_dom[0].get('src')
      }
    else :
      return {
        "id": None,
        "name": None,
        "tel": None,
        "address": None,
        "img": None,
      }

  def get_comments(self, placeId, store_name, store_id):
    page = 1
    display = 10
    url = "https://store.naver.com/sogum/api/receiptReviews?businessId=%s&page=%d&display=%d"
    
    comments = []
    is_exist = False

    while True:
      res = rq.get(url%(store_id, page, display), headers = {
        'Referer': 'https://store.naver.com/restaurants/detail?entry=plt&id=%s&tab=receiptReview'%(store_id),
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
      })
      res_data = res.json()
      res_comments = res_data.get('items', [])
      for res_comment in res_comments:
        C = Comment(
          placeId, store_id, self.platform, 
          res_comment['authorId'], encode_sha2(res_comment['body']), res_comment['body'], res_comment['rating']
        )
        is_exist = C.is_exist_comment()
        print(is_exist)
        if not is_exist:
          comments.append(C)
        if is_exist:
          break
      
      page += 1

      if len(res_comments) < display or is_exist:
        break

    return comments


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