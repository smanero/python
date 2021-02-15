from enum import Enum
from urllib import request

class Aim(Enum):
   DIET = 1
   STRENGTH = 2
   SPEED = 3
   ELASTICITY = 4
   FLEXIBILITY = 5

class Level(Enum):
   NEWBIE = 1
   MEDIUM = 2
   HARD = 3
   HARDCORE = 4

class Item:
   def __init__(self, name : str, desc : str, dur : str):
      self.name = name
      self.desc = desc
      self.dur = dur

class Diet:
   def __init__(self, name : str, desc : str, dur : str, aims):
      super().__init__(name, desc, dur)
      self.aims = aims

class Plan(Item):
   def __init__(self, name : str, desc : str, dur : str, owner : str, aim: Aim, level: Level, sessions):
      super().__init__(name, desc, dur)
      self.owner = owner
      self.aim = aim
      self.level = level
      self.sessions = sessions

class Session:
   def __init__(self, name : str, desc : str, dur : str, stages):
      super().__init__(name, desc, dur)
      self.stages = stages

class Stage:
   def __init__(self, name : str, desc : str, dur : str, steps):
      super().__init__(name, desc, dur)
      self.steps = steps

class Step:
   def __init__(self, name : str, desc : str, dur : str, url : str):
      super().__init__(name, desc, dur)
      self.url = url

   def checkUrl(self):
      req = request.urlopen(self.url)
      assert 200 == req.getcode()