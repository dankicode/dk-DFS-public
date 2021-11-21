import pandas as pd 
import historicalFloor as historicalFloor
import momentum as momentum

# all input files
df_fantasy_data = pd.read_csv('./data/needUpdateProjections/fantasydata-projections.csv')
df_rotowire = pd.read_csv('./data/needUpdateProjections/rotowire-projections.csv')
df_historical = historicalFloor.getHistoricalFloorData()
df_momentum = momentum.getMomentum() 

# filters and merging
df_rotowire = df_rotowire[['PLAYER', 'FPTS']]
df_historical = df_historical[['Name', '.75-interval-L']]
df_momentum = df_momentum[['Name_2021', 'multiplier']]
df_rotowire.columns = ['Name', 'FantasyPointsRotowire']
df_momentum.columns = ['Name', 'MomentumMultiplier']
df_projections_merged = pd.merge(df_fantasy_data, df_rotowire, on="Name")
df_historical_projections_merged = pd.merge(df_projections_merged, df_historical, on="Name")

df_historical_projections_momentum_merged = pd.merge(df_historical_projections_merged, df_momentum, on="Name", how='left').fillna(1) 

df_final_input = df_historical_projections_momentum_merged[['Name', 'Position', 'Team', 'OperatorSalary', 'FantasyPointsRotowire', 'FantasyPointsDraftKings', 'MomentumMultiplier', '.75-interval-L']]

def getInputDataRaw():
  return df_final_input