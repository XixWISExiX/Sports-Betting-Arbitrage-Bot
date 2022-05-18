
# Imports the main grid variable from odds Scrapper (MORE VARIABLES WILL BE MADE WITH MORE SCRAPES)

# Grab the index to the corisponding bookies
class Calculations:
  def __init__(self, grid) -> None:
    self.grid = grid

    self.site1 = None
    self.team1 = None
    self.betOdds1 = None

    self.team2 = None
    self.bet2 = None
    self.betOdds2 = None

    self.index1 = None
    self.index2 = None

  def print(self):
    print(self.grid)

  def printAll(self):
    print("-----")
    print("Site 1: ",self.site1, "| Team Name: ",self.team1, "| Odds: ",self.betOdds1)
    print("Site 2: ",self.site2, "| Team Name: ",self.team2, "| Odds: ",self.betOdds2)
    print("-----")

  def toDecimal(self, american_odds):
    if(american_odds<0):
      return (100/abs(american_odds))+1
    else:
      return (american_odds/100)+1

  # Converts numbers to implied probability that is less than 100%
  def impliedProbability(self, odds1, odds2):
    return (1/self.toDecimal(odds1))+(1/self.toDecimal(odds2))


  #TODO If isArbitrage returns true, then this should email the user the match and the sites
  def isArbitrage(self, odds1, odds2):
    impProb = self.impliedProbability(odds1, odds2)
    # print(impProb)
    if(impProb < 1):
      self.betOdds1 = odds1
      self.betOdds2 = odds2
      self.printAll()
      return True
    return False

  def anyArbitrage(self, grids):
    # All values in the grid should be the same length so just use 0
    r=1
    while(r<len(self.grid)):
      matchSet = [[]]
      matchSet.append([])
      for c in range(len(self.grid[0])):
        # Skips the first list and the first index of each list
        if(r+1 != 0 and r != 0 and c != 0):
          if(grids[r][c] != '' and grids[r+1][c] != ''):
            matchSet[0].append(int(grids[r][c]))
            matchSet[1].append(int(grids[r+1][c]))
          # print("Row is ",r)
          # print("Col is ",c)

        # self.site1 = grids[0][r]
        # self.site2 = grids[0][r]
        # self.team1 = grids[r][0]
        # self.team2 = grids[r+1][0]
      if(self.bestChance(matchSet)):
        #TODO find which sites and which matches
        # print(matchSet)
        return True
      r+=2
    return False

# Finds the largest element from both arrays in the 2d array and checks if it is an arbitrage or not
# Also stores the index of the highest value to trace back to the right Bookie
  def bestChance(self, matchSet):
    # print(matchSet)
    large1 = -100000
    for i in range(len(matchSet[0])):
      if(matchSet[0][i]>large1):
        large1 = matchSet[0][i]
        self.index1 = i+1
    large2 = -100000
    for i in range(len(matchSet[1])):
      if(matchSet[1][i]>large2):
        large2 = matchSet[1][i]
        self.index2 = i+1
    # print(large1)
    # print(large2)
    # print(self.index1)
    # print(self.index2)

    self.site1 = self.grid[0][self.index1]
    self.site2 = self.grid[0][self.index2]
    self.team1 = self.grid[self.index1][0]
    self.team2 = self.grid[self.index2][0]

    return self.isArbitrage(large1,large2)

#TODO Find out how much money should be put down (or at least a ratio if arbitrage)
  def moneyRatio(self):
    return;