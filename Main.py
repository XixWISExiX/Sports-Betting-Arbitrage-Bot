from OddsScrapper import Scraper

# TODO create an infinate loop which finds arbitrage

# Creats a scraper object to then scrap data through various means and then find arbitrage afterwards
s = Scraper()
# TODO find all arbitrage, not just one, and make sure that it is not repeated 
s.oddsSharkMMA()
s.arbitrage()
#TODO might need to check if the same 2 teams are having a match on a different day (could be a future bug)