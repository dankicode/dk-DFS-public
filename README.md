# dk-dfs
### Weekly Process
1. update data/needUpdateProjections with projections csv from roto/fantasydata
2. update data/needUpdateHistoricalFloor with csv from current year to include previous week's outcome data from fantasydata
3. update momentum from previous week's results with csv from fantasydata
4. check config.py to create overrides/adjust different variations of lineups
5. run start.py


### Data Flow
1. historicalFloor.py runs to generate a dataframe with the most up to date historical floor data for each player
2. TODO: add momentum flow
3. inputDataRaw.py runs consuming dataframes generated from steps 1/2 and weekly updated csvs in data/needUpdateProjections generating an aggregate dataframe with all raw data necessary to generate lineups
4. inputDataProcessed.py runs with specific parameters passed in from config.py which includes
  a. lineupConfig - determines which variations of point projection type (floor, momentum, avg, all) and filtering (qb salary/value cap) to use when generating lineups to test different methods against each other
  b. preProcessConfig - modifiable paramters for filtering (qb salary/value cap)

  It takes these paramters and creates a dataframe with a specific type of projection (floor, momentum, avg, all) and players filtered or not-filtered, which is then used in optimizer.py

5. optimizer.py take the input from step 4 and generates an optimal lineup -- and creates a csv for each in data/projections so we can analyze performance and for recordkeeping

Note: step 5 may run multiple times to generate multiple lineups based on the lineupConfig length in config.py

# Strategies
1. Average: Take average projected scores from Rotowire and FantasyData.
2. QB Cap: # DKO TODO 
3. Floor: # DKO TODO
4. Momentum: Momentum is defined as number of games a player exceeded projections divided by total number of games played. This metric is calculated from the 2019 - Present seasons. Must recalculate weekly (e.g. Week 5 stats used to update momentum score for Week 6). Players with a momentum score > 0.5 recieve a multiplier > 1.
5. Touches/Targets: **NOT IMPLEMENTED**