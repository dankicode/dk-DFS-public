import pandas as pd

#todo refactor 
players = ["Atlanta Falcons", "Matthew Stafford", "Alvin Kamara", "D'Andre Swift", "Cole Kmet", "Amari Cooper", "Darnell Mooney", "Davante Adams", "Robert Woods"]
backfillDF = pd.read_csv('data/backfills/NFL-HistoricalProduction-week4.csv')
formattedDF = backfillDF.drop(
  [
    'DK Points', 
    'Opp Position Rank', 
    'FDSal', 
    'DKSal'
  ], axis=1).rename(columns={'FD Points': 'dk_points'})
playersPoints = formattedDF.loc[formattedDF['Player'].isin(players)]
total = playersPoints['dk_points'].sum()
print(total)
