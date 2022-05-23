from OddsScrapper import Scraper

# Creats a scraper object to then scrap data through various means and then find arbitrage afterwards
s = Scraper()
# TODO if odds are heavaly scewed, then there might be something wrong
i = 0

while(i<2):
  s.oddsSharkMMA()
  s.arbitrage()
  s.clearData()

  s.oddsSharkNHL()
  s.arbitrage()
  s.clearData()

  s.oddsSharkNBA()
  s.arbitrage()
  s.clearData()

  s.oddsSharkMLB()
  s.arbitrage()
  s.clearData()

  i+=1

#TODO might need to check if the same 2 teams are having a match on a different day (could be a future bug)