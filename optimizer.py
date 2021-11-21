import re
import pulp
import pandas as pd 
import constants

from pulp.apis.coin_api import PULP_CBC_CMD

import inputDataProcessed as inputData

def outputLineups(prob, conf):
    div = '---------------------------------------\n'
    score = str(prob.objective)
    constraints = [str(const) for const in prob.constraints.values()]

    players = []
    projectedPoints = []
    salary = []

    # get players who's projected points are greater than zero
    for v in prob.variables():
        score = score.replace(v.name, str(v.varValue))
        constraints = [const.replace(v.name, str(v.varValue)) for const in constraints]
        if v.varValue != 0:
            players.append(v.name)
    print(div)

    # get points for players
    projectedPoints = list(map(lambda points: float(points[0:points.index('*')]),re.findall("[0-9\.]+\*1.0", score)))

    # get salaries for players
    for constraint in constraints:
        constraint_pretty = " + ".join(re.findall("[0-9\.]+\*1.0", constraint))
        if constraint_pretty != "": 
            salary = list(map(lambda salary: float(salary[0: salary.index('*')]), re.findall("[0-9\.]+\*1.0", constraint)))
    
    # combine all above data 
    lineup = []
    for idx, _val in enumerate(players):
        data = {
            "name": players[idx],
            "projectedPoints": projectedPoints[idx],
            "salary": salary[idx]
        }
        lineup.append(data)
    df_projections = pd.DataFrame.from_records([data for data in lineup])
    print(df_projections, df_projections['projectedPoints'].sum(), df_projections['salary'].sum())

    # output result of each variation into csv
    df_projections.to_csv("./data/projections/week%s-preprocess-%s-projectiontype-%s.csv"%(conf['week'], conf['preProcess'], conf['projectionType']))


def createLineups(config):
    projected = inputData.getInputDataProcessed(config)
    projected_filtered = projected[['Name', 'Pos', 'Sal', 'FP']]
    # ex: {QB: {'Patrick Mahomes: 8100...}...}
    pos_to_player_salary = {} 
    # ex: {QB: {'Patrick Mahomes: 28.23...}...}
    pos_to_player_points = {}
    # all positions in form [QB, RB, WR ...] -- may be unnecessary
    allPositions = projected_filtered.Pos.unique()
    for pos in allPositions:
        player_data_for_pos = projected_filtered[projected_filtered.Pos == pos]
        player_to_salary = list(player_data_for_pos[["Name", "Sal"]].set_index("Name").to_dict().values())[0]
        player_to_points = list(player_data_for_pos[["Name", "FP"]].set_index("Name").to_dict().values())[0]
        pos_to_player_salary[pos] = player_to_salary
        pos_to_player_points[pos] = player_to_points

    _vars = {k: pulp.LpVariable.dict(k, v, cat='Binary') for k, v in pos_to_player_points.items()}

    problem = pulp.LpProblem("Lineup", pulp.LpMaximize)

    rewards = []
    costs = []
    roster_list = []

    # Setting up the reward
    for k, v in _vars.items():
        costs += pulp.lpSum([pos_to_player_salary[k][i] * _vars[k][i] for i in v])
        rewards += pulp.lpSum([pos_to_player_points[k][i] * _vars[k][i] for i in v])
        roster_list += [_vars[k][i] for i in v]
        
        if k == 'QB' or k == 'DST':
            problem += pulp.lpSum([_vars[k][i] for i in v]) == constants.ROSTER_POSITION_COUNT[k]
        else:
            # need to at least hit 2RB/3WR/1TE
            problem += pulp.lpSum([_vars[k][i] for i in v]) >= constants.ROSTER_POSITION_COUNT[k] - 1
        
    problem += pulp.lpSum(rewards)
    problem += pulp.lpSum(costs) <= constants.SALARY_CAP
    # impose count of 9 players
    problem += pulp.LpConstraint(pulp.lpSum(roster_list), rhs=constants.ROSTER_COUNT, name='count')
    problem.solve(PULP_CBC_CMD(msg=0))
    outputLineups(problem, config)
