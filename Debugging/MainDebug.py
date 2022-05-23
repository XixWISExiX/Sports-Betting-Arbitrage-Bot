from OddsScrapperDebug import Scraper

# Creats a scraper object to then scrap data through various means and then find arbitrage afterwards
s = Scraper()
# TODO if odds are heavaly scewed, then there might be something wrong

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