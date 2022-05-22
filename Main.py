from OddsScrapper import Scrapper

# TODO create an infinate loop which finds arbitrage

# Creats a scraper object to then scrap data through various means and then find arbitrage afterwards
s = Scrapper()
# TODO find all arbitrage, not just one, and make sure that it is not repeated 
s.oddsSharkMMA()

# s.draftKingsMMA()
# s.CaesarsMMA()

# s.FanduelMMA()
# s.printData()

# s.arbitrage()

# s.testData1()
# s.testData2()
s.arbitrage()
#TODO might need to check if the same 2 teams are having a match on a different day (could be a future bug)