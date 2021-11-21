SALARY_CAP = 50000
ROSTER_COUNT = 9

# flex position is baked into the roster (no explicit FLEX position)
ROSTER_POSITION_COUNT = {
    "QB": 1,
    "RB": 3,
    "WR": 4,
    "TE": 2,
    "DST": 1
}

VALID_POSITIONS = ["QB", "RB", "TE", "WR", "DST"]

# to be updated whenever a new projectionType is added
PROJECTION_TYPES = {
  "average": "average", 
  "floor": "floor", 
  "momentum": "momentum", 
  "all": "all"
}