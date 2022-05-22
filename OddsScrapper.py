import math
from unittest import skip

import pandas as pd
from Calculations import Calculations
from selenium import webdriver
import chromedriver_autoinstaller

# Scrapper object which makes a grid to hold the name of the players and the odds of the given matches with their
# corrisponding sports books
class Scraper:
  def __init__(self):
    self.grid = [[]]
    # self.grid.append([])
    # self.grid[0].append("Players Names")
    # self.grid[0].append("Draft Kings")
    # self.grid[0].append("Caesars")
    # self.grid[0].append("Fanduel")

  # prints out the grid
  def printData(self):
    print(self.grid)

  #clears the content of the grid
  def clearData(self):
    self.grid = [[]]

  # data1 to test the calculations class
  def testData1(self):
    self.grid = [[]]
    self.grid[0].append("Names")
    self.grid[0].append("Odds")
    self.grid.append([])
    self.grid[1].append("Heads")
    self.grid[1].append("+150")
    self.grid.append([])
    self.grid[2].append("Tails")
    self.grid[2].append("+150")

  # data2 to test the calculations class
  def testData2(self):
    self.grid = [[]]
    self.grid[0].append("Names")
    self.grid[0].append("Odds")
    self.grid[0].append("Other Odds")
    self.grid.append([])
    self.grid[1].append("Heads")
    self.grid[1].append("+150")
    self.grid[1].append("-100")
    self.grid.append([])
    self.grid[2].append("Tails")
    self.grid[2].append("-100")
    self.grid[2].append("+150")

  # A helper method to find the index of a certain value in a list and if the value is not in the index
  # the method returns -1
  def index_of(self, val, in_list):
    try:
        return in_list.index(val)
    except ValueError:
        return -1 

  # Finds if there is arbitrage in the grid
  def arbitrage(self):
    calc = Calculations(self.grid)
    calc.print()
    #TODO if true send an email to the user
    print(calc.anyArbitrage(self.grid))

  # Grabs the odds using the OddsShard website (MMA ODDS)
  def oddsSharkMMA(self):
    chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                          # and if it doesn't exist, download it automatically,
                                          # then add chromedriver to path
    driver = webdriver.Chrome()

    website = "https://www.oddsshark.com/ufc/odds"
    # website = "https://www.oddsshark.com/nhl/odds"
    driver.get(website)

    # adds different betting cites to the first array
    books = driver.find_elements_by_xpath('//div[@class="op-block__books"]/div/a')
    betting_sites = []
    betting_sites.append("Opening Odds")

    count1 = 0
    for book in books:
      if(book.get_attribute("aria-label") == book.get_attribute("aria-label").upper()):
        if(count1 != 0):
          betting_sites.append(book.get_attribute("aria-label"))
        else:
          count1+=1

    # gets the match participants names
    names = driver.find_elements_by_xpath('//div[@class="op-block__matchup-team-wrapper"]/div/a/span')
    name_array = []
    name_array2 = []

    count = 0
    counter = 0
    for name in names:
      if(count == 0):
        if(counter % 2 == 0):
          name1 = name.text
          name_array.append(name1)
          counter+=1
        else:
          name2 = name.text
          name_array2.append(name2)
          counter+=1
        count+=1
      else:
        count-=1

    # Getting the odds from each site and removes opening odds
    odds_top = driver.find_elements_by_xpath('//div[@class="op-block__cell-first-row"]/div')
    odds_top_list = [[]]
    counter = 0
    c = 0
    for top in odds_top:
      if(count == 0):
        tops = top.text
        odds_top_list[c].append(tops)
        count+=1
        counter+=1
        if(counter == len(betting_sites)):
          counter=0
          odds_top_list[c].pop(0)
          odds_top_list.append([])
          # openingNum = 0
          c+=1
      else:
        count-=1

    odds_bottom = driver.find_elements_by_xpath('//div[@class="op-block__cell-second-row"]/div')
    odds_bottom_list = [[]]
    counter = 0
    c = 0
    for bot in odds_bottom:
      if(count == 0):
        bots = bot.text
        odds_bottom_list[c].append(bots)
        count+=1
        counter+=1
        if(counter == len(betting_sites)):
          counter=0
          odds_bottom_list[c].pop(0)
          odds_bottom_list.append([])
          c+=1
      else:
        count-=1

    # Finding all the null locations (there are participants with 0 odds listed)
    nullls = driver.find_elements_by_xpath('//div[@class="op-block__separator odds-block__separator--right"]/following-sibling::div')
    null_indecies = []
    counter = 0
    for nul in nullls:
      if(nul.get_attribute("class") == "op-block__row not-futures no-odds-wrapper"):
        null_indecies.append(math.floor(counter/2))
      if(counter == len(odds_bottom_list)*2):
        break
      counter+=1

    # Quits the website
    driver.quit()

    count = 0
    for n in null_indecies:
      if(n < len(name_array) and n < len(name_array2)):
        name_array.pop(n-count)
        name_array2.pop(n-count)
        count+=1

    # Adding First participant to Odds
    i=0
    for array in odds_top_list:
      array.insert(0, name_array[i])
      i+=1
    # Adding Second participant to Odds
    i=0
    for array in odds_bottom_list:
      array.insert(0, name_array2[i])
      i+=1

    # Combining both participant and odds
    main_grid = [[]]
    i=0
    a=0
    b=0
    for l in range(len(odds_bottom_list)+len(odds_top_list)):
      if(i % 2 == 0):
        main_grid.append(odds_top_list[a])
        a+=1
      else:
        main_grid.append(odds_bottom_list[b])
        b+=1
      i+=1

    # MIGHT BE ERROR HERE IN THE FUTURE
    main_grid.pop(0)
    main_grid.pop(len(main_grid)-1)
    main_grid.pop(len(main_grid)-1)

    betting_sites.insert(0, "Fighter Names")
    betting_sites.pop(1)
    main_grid.insert(0, betting_sites)
    # All values are now stored in a 2d array called main grid which will be assigned to the grid variable
    self.grid = main_grid

#TODO Scrap more sites (scrape the individual sites differently)







#------------------------------------------------------------------------------------------
#TODO EVERYTHING PAST THIS POINT IS EXPIRIMENTAL AND DOESN'T WORK AS INTENDED
  def draftKingsMMA(self):
    chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                          # and if it doesn't exist, download it automatically,
                                          # then add chromedriver to path
    driver = webdriver.Chrome()

    website = "https://sportsbook.draftkings.com/leagues/mma/88670562"
    driver.get(website)

    # Name of team/player
    names = driver.find_elements_by_xpath('//div[@class="sportsbook-outcome-body-wrapper"]/div/span')
    nameArr = []
    for name in names:
      nameArr.append(name.text)

    # Odds of team/player
    odds = driver.find_elements_by_xpath('//div[@class="sportsbook-outcome-body-wrapper"]/div/div/span')
    oddsArr = []
    for odd in odds:
      oddsArr.append(odd.text)

    # Checks if the name is in the grid and if it's not, add it along with odds.
    for i in range(len(nameArr)):
      # Checks if the name is in the not in the grid and adds the odds.
      if(not any(nameArr[i] in sublist for sublist in self.grid)):
        self.grid.append([])
        self.grid[len(self.grid)-1].append(nameArr[i])
        self.grid[len(self.grid)-1].append(oddsArr[i])
      else:
        # Adds the odds to the given player array if the player exsists on that array
        for j in range(len(self.grid)):
          if(self.index_of(nameArr[i], self.grid[j]) != -1):
            self.grid[j].append(oddsArr[i])
    # adds '' to names which are not touched by this method
    for i in range(len(self.grid)):
      if(len(self.grid[i]) < 2):
        self.grid[i].append('');
    # print(self.grid)
    driver.close()
  
  def CaesarsMMA(self):
    chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                          # and if it doesn't exist, download it automatically,
                                          # then add chromedriver to path
    driver = webdriver.Chrome()

    website = "https://www.williamhill.com/us/co/bet/ufcmma"
    driver.get(website)

    # Name of team/player
    names = driver.find_elements_by_xpath('//div[@class="teamLabel maxIOSHeight"]/span')
    nameArr = []
    #TODO not gathering all names
    for name in names:
      nameArr.append(name.text)
    # print(nameArr)

    #TODO not gathering all odds
    # Odds of team/player
    odds = driver.find_elements_by_xpath('//div[@class="oddsView"]/div')
    oddsArr = []
    count = 0
    for odd in odds:
      # print(odd.text)
      if (count > 1):
        oddsArr.append(odd.text)
      count+=1

    # print(oddsArr)

    # print(self.grid)
    # Checks if the name is in the grid and if it's not, add it along with odds.
    for i in range(len(nameArr)):
      # Checks if the name is in the not in the grid and adds the odds.
      if(not any(nameArr[i] in sublist for sublist in self.grid)):
        #TODO this could be wrong
        self.grid.append([])
        self.grid[len(self.grid)-1].append(nameArr[i])
        # Adds a none because Draft kings doesn't have a list if this is checked
        self.grid[len(self.grid)-1].append('')
        self.grid[len(self.grid)-1].append(oddsArr[i])
      else:
        # Adds the odds to the given player array if the player exsists on that array
        for j in range(len(self.grid)):
          if(self.index_of(nameArr[i], self.grid[j]) != -1):
            self.grid[j].append(oddsArr[i])
    # adds '' to names which are not touched by this method
    for i in range(len(self.grid)):
      # if(len(self.grid[i]) < len(self.grid[0])):
      if(len(self.grid[i]) < 3):
        self.grid[i].append('');

    # print(self.grid)
    driver.close()

  def FanduelMMA(self):
    # chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
    #                                       # and if it doesn't exist, download it automatically,
    #                                       # then add chromedriver to path
    # driver = webdriver.Chrome()

    website = "https://nj.pointsbet.com/sports/mma/UFC"
    self.driver.get(website)

    # Name of team/player
    # names = driver.find_elements_by_xpath('//span[@class="ae aj iu iv iw ix ij ik il io iy s gd dw iz h i j ak l m al o am q an br"]')
    names = self.driver.find_elements_by_xpath('//span[@class="f1fdaby6"]')
    nameArr = []
    print("sad")
    for name in names:
      print(name.text)
      nameArr.append(name.text)

    # Odds of team/player
    odds = self.driver.find_elements_by_xpath('//span[@class="fheif50"]')
    oddsArr = []
    for odd in odds:
      print(odd.text)
      oddsArr.append(odd.text)

    # Checks if the name is in the grid and if it's not, add it along with odds.
    for i in range(len(nameArr)):
      # Checks if the name is in the not in the grid and adds the odds.
      if(not any(nameArr[i] in sublist for sublist in self.grid)):
        self.grid.append([])
        self.grid[len(self.grid)-1].append(nameArr[i])
        self.grid[len(self.grid)-1].append(oddsArr[i])
      else:
        # Adds the odds to the given player array if the player exsists on that array
        for j in range(len(self.grid)):
          if(self.index_of(nameArr[i], self.grid[j]) != -1):
            self.grid[j].append(oddsArr[i])
    # adds '' to names which are not touched by this method
    for i in range(len(self.grid)):
      # The integer number should change with the position which the code is being declaired
      if(len(self.grid[i]) < 4):
        self.grid[i].append('');
        # self.grid[i].append('');
    # print(self.grid)
    self.driver.close()