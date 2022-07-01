import smtplib
# Imports the main grid variable from odds Scrapper (calculates arbitrage with the format given from the scrapper class)
# Only calculates arbitrage for 2 possible out comes, meaning no parlays and no draw odds.

# https://www.pinnacle.com/en/betting-resources/betting-tools/arbitrage-calculator

class Calculations:
  def __init__(self, grid, sportName) -> None:
    # The grid to preform calculations on
    self.grid = grid

    # Name of the given sport
    self.sportName = sportName

    # The email message which is going to be emailed when there is arbitrage
    self.emailMessage = ""

    self.emailMsgArray = []

    # The Implied Probability
    self.impProb = 101

    # Name of arbitrage site 1 and 2
    self.site1 = None
    self.site2 = None

    # Name of arbitrage players 1 and 2
    self.team1 = None
    self.team2 = None

    # odds of bet 1 and bet 2
    self.betOdds1 = None
    self.betOdds2 = None

    # index position of player 1
    self.index = None
    # index position of site 1
    self.index1 = None
    # index position of site 2
    self.index2 = None

  # Gets the Email Message Array
  def getEmailMsgArray(self):
    return self.emailMsgArray

  # Sets the Email Message Array
  def setEmailMsgArray(self, array):
    self.emailMsgArray = array

  # Prints the grid
  def print(self):
    print(self.grid)

  # Prints the Arbitrage site, name, and odds of both sides of the given match
  def teamComparison(self):
    # print("-----")
    # print("Sport :",self.sportName)
    # print("Site 1: ",self.site1, "| Team Name: ",self.team1, "| Odds: ",self.betOdds1)
    # print("Site 2: ",self.site2, "| Team Name: ",self.team2, "| Odds: ",self.betOdds2)
    # print("-----")
    self.emailMessage+="======\n"
    self.emailMessage+="Implied Probability: {}\n".format(self.impProb)
    self.emailMessage+="-----\n"
    self.emailMessage+="Sport : {}\n".format(self.sportName)
    self.emailMessage+="Site 1: {} | Team Name: {} | Odds: {}\n".format(self.site1, self.team1, self.betOdds1)
    self.emailMessage+="Site 2: {} | Team Name: {} | Odds: {}\n".format(self.site2, self.team2, self.betOdds2)
    self.emailMessage+="-----\n"

  def emailUser(self):
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login("WiseBetz100@gmail.com", "wrpierwlyhfdeujv")
    server.sendmail("WiseBetz100@gmail.com",
                    "ReceiverOfGoodNews@gmail.com",
                    self.emailMessage)
    server.quit()

  # Converts american odds to decimal odds
  def toDecimal(self, american_odds):
    if(american_odds<0):
      return (100/abs(american_odds))+1
    else:
      return (american_odds/100)+1

  # Converts both odds to implied probability (arbitrage is less than 100% or 1)
  def impliedProbability(self, odds1, odds2):
    return (1/self.toDecimal(odds1))+(1/self.toDecimal(odds2))


  # Determins if 2 odds have Arbitrage and if so, returns true. This method also prints out arbitrage information to the user
  def isArbitrage(self, odds1, odds2):
    self.emailMessage = ""
    impProb = self.impliedProbability(odds1, odds2)
    wasEmailed = False
    if(impProb < 1):
      self.betOdds1 = odds1
      self.betOdds2 = odds2
      self.site1 = self.grid[0][self.index1]
      self.site2 = self.grid[0][self.index2]
      self.team1 = self.grid[self.index][0]
      self.team2 = self.grid[self.index+1][0]
      self.impProb = impProb
      # print("======")
      # print("Implied Probability is", impProb)
      self.teamComparison()
      #TODO might want to grab multiple arbitrage oportunities if you can (program doesn't do that yet)
      # assumed pay out is $100
      self.moneyRatio(odds1, odds2, 100)

      # print("what?")
      for array in self.emailMsgArray:
        # if(array == self.emailMessage):
        if(array.__eq__(self.emailMessage)):
          wasEmailed = True
          # print("wasEmailed")
      if(not wasEmailed):
        self.emailUser()
        # print("ok")
        self.emailMsgArray.append(self.emailMessage)
        self.emailMessage = "" #TODO make change
        wasEmailed = True
        # print(self.emailMessage)

      return True
    return False

  # Finds if there is arbitrage in the grid
  def anyArbitrage(self, grids):
    r=1
    x=0
    hasArb = False
    while(r<len(self.grid)):
      notReapeat = False
      # MatchSet is a 2d array with 2 different arrays holding the odds from both sides of a match
      matchSet = [[]]
      matchSet.append([])
      # Adds None in the space for the playername
      matchSet[0].append(None)
      matchSet[1].append(None)
      for c in range(len(self.grid[0])):
        # Skips the first list and the first index of each list
        if(r+1 != 0 and r != 0 and c != 0 and r+1 < len(self.grid)):
          if(grids[r][c] != '' and grids[r+1][c] != ''):
            matchSet[0].append(int(grids[r][c]))
            matchSet[1].append(int(grids[r+1][c]))
          else:
            # Adds None in the space for the values which don't exist
            matchSet[0].append(None)
            matchSet[1].append(None)
      self.index = r
      # Uses the newly made MatchSet to then find the best chance of arbitrage
      if(self.bestChance(matchSet) and x < 2):
        x+=1
        hasArb = True
      r+=2
    #TODO do something here
    return hasArb

# Finds the largest element from both arrays in the 2d array and checks if it is an arbitrage or not
# Also stores the index of the highest value to trace back to the right Bookie
  def bestChance(self, matchSet):
    # Finds the largest value for the first set
    # print(matchSet)
    large1 = -100000
    for i in range(len(matchSet[0])):
      if(matchSet[0][i] != None):
        if(matchSet[0][i]>large1):
          large1 = matchSet[0][i]
          self.index1 = i
    # Finds the largest value for the second set
    large2 = -100000
    for i in range(len(matchSet[1])):
      if(matchSet[1][i] != None):
        if(matchSet[1][i]>large2):
          large2 = matchSet[1][i]
          self.index2 = i
    # Calls the is arbitrage function to see if the two largest numbers are arbitrage
    return self.isArbitrage(large1,large2)

  # Finds out how much money should be put down (with the assuming price of total money put down) along with the ratio (if arbitrage)
  def moneyRatio(self, odds1, odds2, payout):
    #TODO https://thearbacademy.com/arbitrage-calculation/ this website might help

    # Gets decimal odds to perform calcultions
    odd1 = self.toDecimal(odds1)
    odd2 = self.toDecimal(odds2)

    # Determins how much money to stake on both sides of the bet
    stake1 = (payout)/odd1
    stake2 = (payout)/odd2

    # Determins the ratio to stake on both sides of the bet
    ratio1 = stake1/stake2
    ratio2 = stake2/stake1

    #TODO double cheek of ratio works as intended
    # Prints the information to the user

    # print("Bet $%f" %stake1, "on", self.team1, "to win $%f" %(payout - stake1), "profit. Bet 1 needs", ratio1, "times more than Bet 2.")
    # print("Bet $%f" %stake2, "on", self.team2, "to win $%f" %(payout - stake2), "profit. Bet 2 needs", ratio2, "times more than Bet 1.")
    # print("Net profit is $", payout-stake1-stake2)
    # print("======")

    self.emailMessage+="Bet ${} on {} to win ${} profit. Bet 1 needs {} times more than Bet 2.\n".format(stake1, self.team1, (payout - stake1), ratio1)
    self.emailMessage+="Bet ${} on {} to win ${} profit. Bet 2 needs {} times more than Bet 2.\n".format(stake2, self.team2, (payout - stake2), ratio2)
    self.emailMessage+="Net profit is ${}\n".format(payout-stake1-stake2)
    self.emailMessage+="DISCLAIMER, if odds are heavily scewed there might be an error with the sites scraped.\n"
    self.emailMessage+="======\n"