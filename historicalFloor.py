import pandas as pd
from pulp import constants 
import researchpy as rp
import glob as gl
import constants

pd.set_option("display.min_rows", 50, "display.max_rows", 150, "display.max_columns", None) 

# 75th percentile
def q75(x):
    return x.quantile(0.75)

# 50th Percentile
def q50(x):
    return x.quantile(0.5)

# 25th Percentile
def q25(x):
    return x.quantile(0.25)

#update 2021_historical.csv with most recent week
all_files = gl.glob("data/needUpdateHistoricalFloor/*.csv")

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)

df = pd.concat(li, axis=0, ignore_index=True)
dfWithValidPositions = df[df['Position'].isin(constants.VALID_POSITIONS)]
dfWithMostRecentMetadata = pd.read_csv('./data/needUpdateHistoricalFloor/2021_historical.csv')[['Name', 'Team', 'Position']].drop_duplicates(subset="Name", keep="last")[df['Position'].isin(constants.VALID_POSITIONS)]


resultCI = rp.summary_cont(dfWithValidPositions['FantasyPointsDraftKings'].groupby(dfWithValidPositions['Name']), conf=0.75)
result = dfWithValidPositions.groupby('Name').agg({'FantasyPointsDraftKings': ['min', 'max', 'median', q25, q50, q75]})
mergedMetadata = pd.merge(dfWithMostRecentMetadata, result, on="Name")
mergedStats = pd.merge(mergedMetadata, resultCI, on='Name').sort_values(by=['Mean'], ascending=False)
mergedStats.columns = ['Name', 'Team', 'Position', 'Min', 'Max', 'Median', 'q25', 'q50', 'q75', 'N', 'Mean', 'Std', 'SE', '.75-interval-L', '.75-interval-H']
reordered = mergedStats[['Name', 'Team', 'Position', 'Median', 'Mean', 'Std', 'Min', 'Max', 'N', '.75-interval-L', '.75-interval-H', 'q25', 'q50', 'q75', 'SE']]


def getHistoricalFloorData():
    return reordered
