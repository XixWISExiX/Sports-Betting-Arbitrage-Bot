# from selenium import webdriver
# import chromedriver_autoinstaller


# chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
#                                       # and if it doesn't exist, download it automatically,
#                                       # then add chromedriver to path

# PATH = "C:\Program Files (x86)\chromedriver.exe"
# driver = webdriver.Chrome()
# driver.get("http://www.python.org")
# # assert "Python" in driver.title

from OddsScrapper import Scrapper

s = Scrapper()
# s.oddsSharkUFC()
s.draftKingsTennis()
# s.betMGMTennis()
#TODO might need to check if the same 2 teams are having a match on a different day (could be a future bug)