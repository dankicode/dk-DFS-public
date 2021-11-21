import pandas as pd 
import statistics as stat
import constants
import inputDataRaw as inputData

#projections

def updatedProjection(row):
  return stat.mean([row['FantasyPointsRotowire'], row['FantasyPointsDraftKings']])

def updatedProjectionMomentum(row):
  return updatedProjection(row) * row['MomentumMultiplier']

#todo this should be a multiplier
def updatedProjectionFloor(row):
  avgProjected = updatedProjection(row)
  #the .75 intervalL should be less than avg projected but not less than by more than 25% to cap the weight of this metric
  if ((avgProjected > row['.75-interval-L']) & ((row['.75-interval-L']*1.25) >= avgProjected)):
    return stat.mean([avgProjected, row['.75-interval-L']]) 
  else:
    return avgProjected

def updatedProjectionAll(row):
  return updatedProjectionFloor(row) * row['MomentumMultiplier']


# to be updated whenever a new projectionType is added
projectionMethods = {
  constants.PROJECTION_TYPES['average']: updatedProjection,
  constants.PROJECTION_TYPES['floor']: updatedProjectionFloor,
  constants.PROJECTION_TYPES['momentum']: updatedProjectionMomentum,
  constants.PROJECTION_TYPES['all']: updatedProjectionAll
}

#value (points per $1000 spent)

def updatedValue(row):
  newValue = (1000*row['FP']) / row['OperatorSalary']
  return newValue

#boolean whether floor was included (ie whether within 25% range of avg projection)

def includedHistoricalFloor(row):
  avgProjected = stat.mean([row['FantasyPointsRotowire'], row['FantasyPointsDraftKings']])
  return (avgProjected > row['.75-interval-L']) & ((row['.75-interval-L']*1.25) >= avgProjected)


#manual overrides
def filterWithConfig(config):
  def filter(row):
    return filterPositionBySalary(row, config) & filterPositionByValue(row, config) & filterPlayer(row, config)
  return filter

def filterPositionBySalary(row, config):
  salaryRangeConfig  = config["preProcessConfig"]["positionConfig"]["salaryRange"]
  positionConfig = salaryRangeConfig.get(row['Position'], None)
  if (positionConfig): 
    return (row['OperatorSalary'] > positionConfig.get('min')) & (row['OperatorSalary'] < positionConfig.get('max'))
  else: 
    return True

def filterPositionByValue(row, config):
  valueRangeConfig  = config["preProcessConfig"]["positionConfig"]["valueRange"]
  positionConfig = valueRangeConfig.get(row['Position'], None)
  if (positionConfig): 
    return (row['Val'] > positionConfig.get('min')) & (row['Val'] < positionConfig.get('max'))
  else: 
    return True

def filterPlayer(row, config):
  playersToOmit  = config["preProcessConfig"]["playerConfig"]["playersToOmit"]
  if (len(playersToOmit)): 
    return row['Name'] not in playersToOmit
  else: 
    return True

def getInputDataProcessed(config):
  df_final = inputData.df_final_input
  df_final = df_final[df_final.Position.isin(constants.VALID_POSITIONS)]
  df_final['FP'] = df_final.apply(projectionMethods[config['projectionType']], axis=1)
  df_final['Val'] = df_final.apply(updatedValue, axis=1)
  df_final['inclFlr'] = df_final.apply(includedHistoricalFloor, axis=1)
  if config['preProcess'] == True:
    df_final = df_final[df_final.apply(filterWithConfig(config), axis=1)]
  df_final = df_final[['Name', 'Team', 'Position', 'Val', 'OperatorSalary', 'FP']]
  df_final.columns = ['Name', 'Team', 'Pos', 'Val', 'Sal', 'FP']
  return df_final


