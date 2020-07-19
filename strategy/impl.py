from abc import ABC
import abc

class Crawler(ABC):
  
  def __init__(self):
    pass

  @abc.abstractmethod
  def store_to_id(self, name):
    pass