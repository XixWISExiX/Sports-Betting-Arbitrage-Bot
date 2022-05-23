from OddsScrapper import Scraper
import time
from threading import Timer

# Creats a scraper object to then scrap data through various means and then find arbitrage afterwards
s = Scraper()
# TODO if odds are heavaly scewed, then there might be something wrong

# TODO if the site is down then the program might shut down

# A dummy method to plug into the timer
def dummyMethod(val):
  val = "done"

# Method which restest the timer
def reset(timer, interval, function):
  timer.cancel()
  timer = Timer(interval, function)
  timer.start()

# There are 86400 seconds in a day (message array refreshes every 24 hours)
tmr = Timer(86400, dummyMethod, [])
tmr.start()

while(True):
  if(not tmr.is_alive()):
    reset(tmr, dummyMethod, ["ok"])
    msgArray = []

  s.oddsSharkMMA()
  msgArray = s.arbitrage(msgArray)
  s.clearData()

  s.oddsSharkNHL()
  msgArray = s.arbitrage(msgArray)
  s.clearData()

  s.oddsSharkNBA()
  msgArray = s.arbitrage(msgArray)
  s.clearData()

  s.oddsSharkMLB()
  msgArray = s.arbitrage(msgArray)
  s.clearData()

#TODO might need to check if the same 2 teams are having a match on a different day (could be a future bug)