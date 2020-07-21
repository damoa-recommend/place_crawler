import json
from dotenv import load_dotenv
import os,sys

load_dotenv()

def get_config():
  mode = os.getenv('MODE') or 'develop'
  with open('config/config.json', 'r') as f:
    lines = [line.replace('\n', '') for line in f.readlines()]

    json_data = json.loads(''.join(lines))
    data = json_data[mode]
  return data

if __name__ == '__main__': 
  data = get_config()
  print(data)