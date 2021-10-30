
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

def scrape():
    # ok
    if os.path.isfile('lol-games.csv'):
        print("cached!")
        with open('lol-games.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)
            events = [tuple(row) for row in reader]
    else:
        print("not cached!")

        # Step 0: Connect to the unofficial league of legends api
        # https://vickz84259.github.io/lolesports-api-docs/#tag/events
        
        # Step 1: Get all tournaments for every league, get the tournaments to analyze. 
        # use /getTournamentsForLeague
        all_tournaments = get_tournaments_for_league()
        
        # Filter the leagues, stick to data from Jan 01, 2021 and later
        tournaments_2021 = [t for t in filter(lambda x: '2021' in x[0], all_tournaments)]

        # For each tournaments, get all the games related to it, along with their start time
        i = 0
        events = []

        for slug, tournamentId in tournaments_2021:
            i += 1
            print((str)(i) + '/' + (str)(len(tournaments_2021)))
            events.extend([(slug, e['match']['id'], g['id'], e['startTime'], (e['games'].index(g) + 1)) for e in get_completed_events([tournamentId]) for g in e['games']])
            
            if i % 15 == 0:
                time.sleep(5)
            # break

        # save to a file, to avoid going back to the api and scrape it all again
        with open('lol-games.csv','w', newline='') as out:
            csv_out=csv.writer(out)
            csv_out.writerow(('tournament', 'match_id', 'game_id', 'start_time', 'game_number'))
            csv_out.writerows(events)

    # Step 2: Collect teams
    teams = {}
    for team in get_teams():
        teams[team['id']] = team
    
    # Step 3: For each game, collect the live game details, and collect all relevant information on team and players
    #         At a given point of the game time
    # use /window for this
    # To get results, you must use the gameStartTime and the offset in order to add them up and find the time at which point there is information
    i = 0
        
    headers = [
        'tournament_slug',
        'game_id',
        'match_id', 
        'patch', 
        'starting_time',
        'game_number',
        'blue_team',
        'red_team',
        'winner',
        'blue_total_gold',
        'blue_inhibitors',
        'blue_towers',
        'blue_barons',
        'blue_total_kills',
        'blue_dragons',
        'blue_total_cs',
        'red_total_gold',
        'red_inhibitors',
        'red_towers',
        'red_barons',
        'red_total_kills',
        'red_dragons',
        'red_total_cs',
    ]
    out = open('lol-results.csv','w', newline='')
    csv_out=csv.writer(out)
    csv_out.writerow(headers)
    minute_mark = 15

    for tournament, match_id, game_id, starting_time, game_number in events:
        i += 1

        window = get_window(game_id)
        if window is None:
            # Do not go further, because game most likely does not exist
            continue
        # get the time
        stripped_datetime = window['frames'][0]['rfc460Timestamp'][:-1].split('.')[0]
        timestamp = datetime.fromisoformat(stripped_datetime)
        starting_time = timestamp - timedelta(seconds=timestamp.second % 10)
        
        window = get_window(game_id, "%sZ" % (starting_time + timedelta(minutes=minute_mark)).isoformat())
        game_metadata = window['gameMetadata']
        blu_teamid = window['gameMetadata']['blueTeamMetadata']['esportsTeamId']
        red_teamid = window['gameMetadata']['redTeamMetadata']['esportsTeamId']
        

        # Get the winner        
        winner = leaguepedia.get_game_winner(
            teams[blu_teamid],
            teams[red_teamid],
            game_number,
            timestamp
        )
        
        
        frame = window['frames'][0]

        # Data Extracted
        row = []
        row.append(tournament)
        row.append(window['esportsGameId'])
        row.append(window['esportsMatchId'])
        row.append(".".join(game_metadata['patchVersion'].split('.')[:2]))
        row.append(starting_time.isoformat(' '))
        row.append(game_number)
        row.append(teams[blu_teamid]['code'])
        row.append(teams[red_teamid]['code'])
        row.append(winner)

        #  Team Stats
        row.extend([
            frame['blueTeam']['totalGold'],
            frame['blueTeam']['inhibitors'],
            frame['blueTeam']['towers'],
            frame['blueTeam']['barons'],
            frame['blueTeam']['totalKills'],
            len(frame['blueTeam']['dragons']),
            sum([p['creepScore'] for p in frame['blueTeam']['participants']])
        ])
        row.extend([
            frame['redTeam']['totalGold'],
            frame['redTeam']['inhibitors'],
            frame['redTeam']['towers'],
            frame['redTeam']['barons'],
            frame['redTeam']['totalKills'],
            len(frame['redTeam']['dragons']),
            sum([p['creepScore'] for p in frame['redTeam']['participants']])
        ])
        # Might be fun to know what champions were used
        # blu_champions = [c['championId'] for c in blu_team['participantMetadata']]
        # red_champions = [c['championId'] for c in red_team['participantMetadata']]

        # Display the information from before
        # display_lane_stats(frame)
        # print(row)
        csv_out.writerow(row)

        if i % 100 == 0:
            print((str)(i) + '/' + (str)(len(events)))
            time.sleep(5)
            


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