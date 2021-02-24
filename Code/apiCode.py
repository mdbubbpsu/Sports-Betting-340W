import pandas as pd
import numpy as np
import json
import requests


def test():
    games = pd.read_csv(
        '/Users/mattbubb/Spring_2021/DS_340W/Sports-Betting-340W/Data/nba_games_all.csv')
    colToDrop = ['oreb', 'dreb', 'reb', 'ast',
                 'stl', 'blk', 'tov', 'pf', 'pts', 'min', 'fgm', 'fga', 'fg_pct', 'fg3m', 'fg3a', 'fg3_pct']
    g = games.drop(colToDrop, axis=1).sort_values('game_date', ascending=False)
    moneyLine = pd.read_csv(
        '/Users/mattbubb/Spring_2021/DS_340W/Sports-Betting-340W/Data/nba_betting_money_line.csv')
    print(g.isna().sum())
    g = g.drop_duplicates('game_id')
    g = g.rename({'wl': 'homeTeamResult', 'team_id': 'homeTeamID'}, axis=1)
    g = g.merge(moneyLine, how='inner', on='game_id')
    g = g.pivot_table(index=['game_id', 'matchup', 'game_date',  'w', 'l', 'w_pct', 'season_type', 'season'], columns='book_name',
                      values=['price1', 'price2'])
    return g


def req():
    reqString = 'https://api.the-odds-api.com/v3/odds/?sport=basketball_nba&region=us&mkt=h2h&oddsFormat=american&apiKey=64832010d163c09e91797967158ee648'
    response = requests.get(reqString)
    jsonObj = response.json()
    return pd.read_json(json.dumps(jsonObj['data']))


def editCSV():
    test = pd.read_csv(
        '/Users/mattbubb/Spring_2021/DS_340W/Sports-Betting-340W/Data/APICSV.csv')
    droppedCols = test.drop(
        ['sport_nice', 'sport_key'], axis=1)
    return droppedCols


if __name__ == '__main__':
    print(test())

    # ONLY NEED TO RUN THESE NEXT TWO LINES ONE PER DAY TO GET CSV
    # api = req()
    # df = api.to_csv('/Users/mattbubb/Spring_2021/DS_340W/Sports-Betting-340W/Data/APICSV.csv', index=False)
    '''
    usable = editCSV()
    count = 0
    master = ""
    masterLst = []
    for i in usable.iloc[:1]['sites'][0][1:-1].split(','):
        j = i.replace('\'', '\"') + ','
        if "h2h_lay" not in j:
            count += 1
            # print(j, count)
            masterLst.append(j)
    print(len(masterLst))
    count = 0
    subLst = []
    antlst = []
    for j in range(len(masterLst)-1):
        subString = ''
        count += 1
        if j == len(masterLst) - 1:
            masterLst[j] = masterLst[j][:-1]
        if len(masterLst[j]) <= 6:
            masterLst[j] = masterLst[j][:-1] + '}},'
            # Second line of lay odds removed
            masterLst.pop(j+1)
        subString += masterLst[j]
        subLst.append(masterLst[j])
    count = 1
    for a in subLst:
        if count % 5 != 0:
            print(a, end="")
        else:
            print(a, count)
        count += 1
'''
