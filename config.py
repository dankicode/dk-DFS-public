import constants

# to be updated weekly
week = 5

# manual overrides (to be updated weekly)
preProcessConfig = { 
  "playerConfig" : { 
    "playersToAdd": [], 
    "playersToOmit": ['Ben Roethlisberger', 'Mac Jones', 'Jacoby Brissett']
  }, 
  "teamConfig": { 
    #[teamName]: countOfPlayers
    "playersPerTeam": {}
  },
  "positionConfig": { 
    "salaryRange": { 
      "QB": { 
         "min": 2000, 
         "max": 6000
      }
    }, 
    # Fantasy points per $1000
    "valueRange": {
      "QB": { 
        "min": 2, 
        #represents infinity (no cap)
        "max": 1000
      }
    }
  }
}

lineupConfig = [
  # avg + no qb cap
  {
    "preProcess": False,
    "projectionType": constants.PROJECTION_TYPES["average"]
  }, 
  # floor + no qb cap
  {
    "preProcess": False,
    "projectionType": constants.PROJECTION_TYPES["floor"]
  }, 
  # momentum + no qb cap
  {
    "preProcess": False,
    "projectionType": constants.PROJECTION_TYPES["momentum"]
  }, 
  # avg + qb cap
  {
    "preProcess": True,
    "projectionType": constants.PROJECTION_TYPES["average"]
  }, 
  # all + qb cap
  {
    "preProcess": True,
    "projectionType": constants.PROJECTION_TYPES["all"]
  }
]

#add extra properties to lineup config 
config = list(map(lambda conf: {**conf, **{"week": week, "preProcessConfig": preProcessConfig}}, lineupConfig))

def getConfig():
  return config

