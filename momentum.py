import pandas as pd
import numpy as np

# import actual and projected historical data from 2019, 2020, 2021 seasons
actual_2019 = pd.read_csv('./data/fntsy-data_2019_ffb-weekly-stats_reg-season_dkng.csv')
projected_2019 = pd.read_csv('./data/fntsy-data_2019_ffb-weekly-projections_reg-season_dkng.csv')
actual_2020 = pd.read_csv('./data/fntsy-data_2020_ffb-weekly-stats_reg-season_dkng.csv')
projected_2020 = pd.read_csv('./data/fntsy-data_2020_ffb-weekly-projections_reg-season_dkng.csv')
actual_2021 = pd.read_csv('./data/fntsy-data_2021_ffb-week1-to-week5-stats_reg-season_dkng.csv')
projected_2021 = pd.read_csv('./data/fntsy-data_2021_ffb-week1-to-week5-projections_reg-season-dkng.csv')

# manually adjust 2020 columns from 'FantasyPointsPerGame' to 
# FantastyPointsPerGameDraftKings for consistency with other csv files
projected_2020 = projected_2020.rename(columns={'FantasyPointsPerGame': 'FantasyPointsPerGameDraftKings'})
actual_2020 = actual_2020.rename(columns={'FantasyPointsPerGame': 'FantasyPointsPerGameDraftKings'})

def df_filter(df):
    '''Select only columns of interest, sort data, rename columns'''

    df = df[['Week','Name', 'Team', 'Position', 'Opponent', 'FantasyPointsPerGameDraftKings']]
    df = df.sort_values(by=['Week', 'FantasyPointsPerGameDraftKings', 'Name', 'Position'],
                          ascending = [True, False, True, True])
    df = df.rename(columns={'Position': 'POS', 'Opponent': 'OPP', 'FantasyPointsPerGameDraftKings': 'FPPG'})
    return df

# apply filter
actual_2019 = df_filter(actual_2019)
projected_2019 = df_filter(projected_2019)
actual_2020 = df_filter(actual_2020)
projected_2020 = df_filter(projected_2020)
actual_2021 = df_filter(actual_2021)
projected_2021 = df_filter(projected_2021)

# add prefix to dataframes
# 'a' indicates actual stats, 'p' indicates projected stats
actual_2019 = actual_2019.add_prefix('a2019_')
projected_2019 = projected_2019.add_prefix('p2019_')
actual_2020 = actual_2020.add_prefix('a2020_')
projected_2020 = projected_2020.add_prefix('p2020_')
actual_2021 = actual_2021.add_prefix('a2021_')
projected_2021 = projected_2021.add_prefix('p2021_')

# merge & clean actual and projected for 2019
merged_2019 = projected_2019.merge(actual_2019, how='outer', left_on=['p2019_Name', 'p2019_Week'],
                                   right_on=['a2019_Name', 'a2019_Week'], indicator=True)
merged_2019 = merged_2019[['p2019_Week', 'p2019_Name', 'p2019_Team', 'p2019_POS', 'p2019_OPP',
                      'p2019_FPPG', 'a2019_FPPG', '_merge']]
merged_2019 = merged_2019.rename(columns={'p2019_Week': '2019_Week', 'p2019_Name': '2019_Name',
                                          'p2019_POS': '2019_POS', 'p2019_OPP': 'OPP'})
merged_2019 = merged_2019[merged_2019['2019_POS'].isin(['RB', 'WR', 'QB', 'TE', 'DST'])]
merged_2019 = merged_2019.dropna()

# merge & clean actual and projected for 2020
merged_2020 = projected_2020.merge(actual_2020, how='outer', left_on=['p2020_Name', 'p2020_Week'],
                                   right_on=['a2020_Name', 'a2020_Week'], indicator=True)
merged_2020 = merged_2020[['p2020_Week', 'p2020_Name', 'p2020_Team', 'p2020_POS', 'p2020_OPP',
                      'p2020_FPPG', 'a2020_FPPG', '_merge']]
merged_2020 = merged_2020.rename(columns={'p2020_Week': '2020_Week', 'p2020_Name': '2020_Name',
                                          'p2020_POS': '2020_POS', 'p2020_OPP': 'OPP'})
merged_2020 = merged_2020[merged_2020['2020_POS'].isin(['RB', 'WR', 'QB', 'TE', 'DST'])]
merged_2020 = merged_2020.dropna()

# merge & clean actual and projected for 2021
merged_2021 = projected_2021.merge(actual_2021, how='outer', left_on=['p2021_Name', 'p2021_Week'],
                                   right_on=['a2021_Name', 'a2021_Week'], indicator=True)
merged_2021 = merged_2021[['p2021_Week', 'p2021_Name', 'p2021_Team', 'p2021_POS', 'p2021_OPP',
                      'p2021_FPPG', 'a2021_FPPG', '_merge']]
merged_2021 = merged_2021.rename(columns={'p2021_Week': '2021_Week', 'p2021_Name': '2021_Name',
                                          'p2021_POS': '2021_POS', 'p2021_OPP': 'OPP'})
merged_2021 = merged_2021[merged_2021['2021_POS'].isin(['RB', 'WR', 'QB', 'TE', 'DST'])]
merged_2021 = merged_2021.dropna()


def momentum(df, season):
    df['delta'] = df[f'a{season}_FPPG'] - df[f'p{season}_FPPG']
    df['pos_delta'] = df.apply(lambda x: 1 if x.delta > 0 else 0, axis=1)
    avg_delta = df.groupby(f'{season}_Name').apply(lambda x: x.delta.mean()).reset_index()
    momentum_scores = df.groupby(f'{season}_Name').apply(lambda x: x.pos_delta.sum()/len(x)).reset_index()
    games_played = df.groupby(f'{season}_Name').apply(lambda x: len(x)).reset_index()
    season_pos_delta = df.groupby(f'{season}_Name').apply(lambda x: x.pos_delta.sum()).reset_index()
    momentum = season_pos_delta.merge(games_played, on=f'{season}_Name')
    momentum = momentum.rename(columns={'0_x': f'games_exceeded_{season}', 
                              '0_y': f'games_played_{season}'})

    momentum = momentum.merge(momentum_scores, on=f'{season}_Name')
    momentum = momentum.rename(columns={0: 'momentum'})
    momentum = momentum.merge(avg_delta, on=f'{season}_Name')
    momentum = momentum.rename(columns={f'{season}_Name': f'Name_{season}', 0: f'avg_delta_{season}'})

    return momentum


momentum_2019 = momentum(merged_2019, 2019)
momentum_2020 = momentum(merged_2020, 2020)

# requires weekly updates
momentum_2021 = momentum(merged_2021, 2021) 


# momentum merge
momentum_merged = momentum_2021.merge(momentum_2020, how='left', left_on='Name_2021', right_on='Name_2020', indicator='21_20_merge')
momentum_merged = momentum_merged.merge(momentum_2019, how='left', left_on='Name_2021', right_on='Name_2019', indicator='21_19_merge')
# fill numerical values with zero if NaN
momentum_merged[['games_exceeded_2021', 'games_played_2021', 'avg_delta_2021', 
                 'games_exceeded_2020', 'games_played_2020', 'avg_delta_2020',
                 'games_exceeded_2019', 'games_played_2019', 'avg_delta_2019'
                ]] = momentum_merged[['games_exceeded_2021', 'games_played_2021', 'avg_delta_2021', 
                 'games_exceeded_2020', 'games_played_2020', 'avg_delta_2020',
                 'games_exceeded_2019', 'games_played_2019', 'avg_delta_2019'
                ]].fillna(0)

# cumulative games played
momentum_merged['cum_games'] = momentum_merged.games_played_2021 + momentum_merged.games_played_2020 + \
                               momentum_merged.games_played_2019

# cumulative exceeded
momentum_merged['cum_exceeded'] = momentum_merged.games_exceeded_2021 + momentum_merged.games_exceeded_2020 + \
                               momentum_merged.games_exceeded_2019

# cumulative momentum
momentum_merged['cum_momentum'] = momentum_merged.cum_exceeded / momentum_merged.cum_games

# cumulative average delta
momentum_merged['cum_avg_delta'] = (momentum_merged.avg_delta_2021 * momentum_merged.games_played_2021 + \
                                momentum_merged.avg_delta_2020 * momentum_merged.games_played_2020 + \
                                momentum_merged.avg_delta_2021 * momentum_merged.games_played_2021) / \
                                momentum_merged.cum_games

def multiplier(momentum):
    '''implement momentum multiplier'''
    if momentum < 0.25:
        m = 0.9
    elif momentum < 0.5:
        m = 0.95
    elif momentum == 0.5:
        m = 1.0
    elif momentum < 0.75:
        m = 1.05
    else:
        m = 1.1
    return m    

momentum_merged['multiplier'] = momentum_merged.cum_momentum.apply(lambda x: multiplier(x))

# filter out multiplier for players less than 5 total games played
momentum_merged = momentum_merged[momentum_merged.cum_games > 5]

def getMomentum():
    print(momentum_merged)
    return momentum_merged