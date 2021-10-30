
import requests
import csv
import os
import time
from datetime import datetime, timedelta
from scrapers import leaguepedia

LEAGUES = [
    'worlds',
    'lcs', 
    'lec', 
    'lck', 
    'lpl', 
    'msi',
]

HEADERS = {
        'x-api-key': '0TvQnueqKa5mxJntVWt0w4LpLfEkrV1Ta8rQBb9Z'
    }

def get_window(game_id, start_time=None):
    url = "https://feed.lolesports.com/livestats/v1/window/%s" % game_id
    if (start_time is not None):
        url += "?startingTime=%s" % start_time
    response = requests.request("GET", url, headers=HEADERS)
    if response.status_code == requests.codes.no_content:
        return None
    return response.json()

def get_teams():
    url = "https://esports-api.lolesports.com/persisted/gw/getTeams?hl=en-US"
    response = requests.request("GET", url, headers=HEADERS)
    return response.json()['data']['teams']

def get_games(gameIds):
    url = "https://esports-api.lolesports.com/persisted/gw/getGames?hl=en-US"
    if (len(gameIds) > 0):
        url += "&id=" + ",".join(gameIds)
    payload={}
    # print(url)
    # return
    response = requests.request("GET", url, headers=HEADERS)
    
    return response.json()['data']['games']

def get_completed_events(tournamentIds):
    url = "https://esports-api.lolesports.com/persisted/gw/getCompletedEvents?hl=en-US"
    # Add tournamentIds to filter by
    if (len(tournamentIds) > 0):
        url += "&tournamentId=" + ",".join(tournamentIds)
    payload={}
    response = requests.request("GET", url, headers=HEADERS)
    return response.json()['data']['schedule']['events']

def get_tournaments_for_league(leagues=[]):    
    url = "https://esports-api.lolesports.com/persisted/gw/getTournamentsForLeague?hl=en-US"
    if (len(leagues) > 0):
        url += "&leagueId=" + ",".join(leagues)
    payload={}
    response = requests.request("GET", url, headers=HEADERS)
    return [(t['slug'], t['id']) for league in response.json()['data']['leagues'] for t in league['tournaments']]

def append_first_blood_and_turret():
    with open('lol-results.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        events = [tuple(row) for row in reader]
    
    for game in events:
        window = get_window(game[2])
        for frame in window['frames']:
            # check if blue team has first blood
            # check if red team has first blood
            # do the same for first turret
            break


def display_lane_stats():
    # Lane Stats (I'm leaving this aside for now, because it seems to complicate the model)        
    # 1,6 - top; 2,7 - jungle; 3,8 - mid; 4,9 - bottom; 5,10 - support
        
        
        # blu_lane_state = [(p['level'], p['creepScore'], p['totalGold']) for p in frame['blueTeam']['participants']]
        # red_lane_state = [(p['level'], p['creepScore'], p['totalGold']) for p in frame['redTeam']['participants']]

        # blu_kda = [(p['kills'], p['deaths'], p['assists']) for p in frame['blueTeam']['participants']]
        # red_kda = [(p['kills'], p['deaths'], p['assists']) for p in frame['redTeam']['participants']]

        # blu_state = [
        #     frame['blueTeam']['totalGold'],
        #     frame['blueTeam']['inhibitors'],
        #     frame['blueTeam']['towers'],
        #     frame['blueTeam']['barons'],
        #     frame['blueTeam']['totalKills'],
        #     len(frame['blueTeam']['dragons']),
        # ]
        # red_state = [
        #     frame['redTeam']['totalGold'],
        #     frame['redTeam']['inhibitors'],
        #     frame['redTeam']['towers'],
        #     frame['redTeam']['barons'],
        #     frame['redTeam']['totalKills'],
        #     len(frame['redTeam']['dragons']),
        # ]
    # print('================================')
    # print("Patch: %s" % patch_version)
    # print("Tournament: %s" % tournament)
    # print("Date: %s" % starting_time.isoformat())
    # print("Blue: %s (%s)" % (blu_teamid, teams[blu_teamid]['name']))
    # print("Red:  %s (%s)" % (red_teamid, teams[red_teamid]['name']))
    # print('================================')
    # print("Picks:")
    # print(blu_champions)
    # print(red_champions)
    # print('================================')
    # print("Game Stats (Gold, Inhibs, Towers, Barons, Kills, Dragons):")
    # print(blu_state)
    # print(red_state)
    # print('================================')
    # print("Stats per lane (CS, Gold, Level):")
    # print(blu_lane_state)
    # print(red_lane_state)
    # print('================================')
    # print("KDA per lane:")
    # print(blu_kda)
    # print(red_kda)
    return