from strategy.google import Google
from strategy.naver import Naver
from strategy.kakao import Kakao

from pandas import read_csv
import random, time, asyncio, argparse, sys

class Place():
  
  def __init__(self):
    self.crawlers = []

  def register(self, target):
    self.crawlers.append(target)
    return self

  async def execute(self):
    df = read_csv('./data/places.csv')
    
    for index, row in df.iterrows():
      asyncios = []
      
      for crawler in self.crawlers:    
        asyncios.append(crawler.start(row['name']))
      
      await asyncio.wait(asyncios)    
      delay_time = random.uniform(1, 3)
      print('delay time: %f\n'%(delay_time))
      time.sleep(delay_time)
      # break

  def start(self):
      asyncio.run(self.execute())

if __name__ == "__main__":
  parser = argparse.ArgumentParser()

  # nargs: arguments의 수
  # ? -> arg가 없으면 default값으로
  parser.add_argument(
      'name', nargs='?', default=False, help="Write name you want to say Hello.")

  # 버전확인 옵션추가
  # action: 해당 argument가 추가될 때 일어나는 액션 (여기서는 version을 true로)
  parser.add_argument('-v', '--version', action="store_true",
                      help="Show version of this program")
  args = parser.parse_args()
  
  if args.version:
    print('1.0.0')
    sys.exit()

  g = Google()
  k = Kakao()
  n = Naver()
  
  place = Place()
  place.register(n)#.register(k) #.register(g)

  place.start()