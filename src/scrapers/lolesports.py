
import requests
import csv
import os
import time

LEAGUES = [
    'worlds',
    'lcs', 
    'lec', 
    'lck', 
    'lpl', 
    'msi',
]

def get_games(gameIds):
    url = "https://esports-api.lolesports.com/persisted/gw/getGames?hl=en-US"
    if (len(gameIds) > 0):
        url += "&id=" + ",".join(gameIds)
    payload={}
    headers = {
        'x-api-key': '0TvQnueqKa5mxJntVWt0w4LpLfEkrV1Ta8rQBb9Z'
    }
    # print(url)
    # return
    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()['data']['games']
def get_completed_events(tournamentIds):
    url = "https://esports-api.lolesports.com/persisted/gw/getCompletedEvents?hl=en-US"
    # Add tournamentIds to filter by
    if (len(tournamentIds) > 0):
        url += "&tournamentId=" + ",".join(tournamentIds)
    payload={}
    headers = {
        'x-api-key': '0TvQnueqKa5mxJntVWt0w4LpLfEkrV1Ta8rQBb9Z'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()['data']['schedule']['events']

def get_tournaments_for_league(leagues=[]):    
    url = "https://esports-api.lolesports.com/persisted/gw/getTournamentsForLeague?hl=en-US"
    if (len(leagues) > 0):
        url += "&leagueId=" + ",".join(leagues)

    payload={}
    headers = {
        'x-api-key': '0TvQnueqKa5mxJntVWt0w4LpLfEkrV1Ta8rQBb9Z'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    return [(t['slug'], t['id']) for league in response.json()['data']['leagues'] for t in league['tournaments']]

def scrape():
    # ok
    cached = os.path.isfile('lol-games.csv')
    if cached:
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
            events.extend([(slug, e['match']['id'], g['id'], e['startTime']) for e in get_completed_events([tournamentId]) for g in e['games']])
            
            if i % 15 == 0:
                time.sleep(5)
            # break

        # save to a file, to avoid going back to the api and scrape it all again
        with open('lol-games.csv','w', newline='') as out:
            csv_out=csv.writer(out)
            csv_out.writerow(('tournament', 'match_id', 'game_id', 'start_time'))
            csv_out.writerows(events)

    
    # Step 3: For each event in a schedule, find the event details and collect all of their games and start times
    # use /getEventDetails
    all_game_ids = [e[2] for e in events]
    chunks = [all_game_ids[i:i+400] for i in range(0, len(all_game_ids), 400)]
    for game_ids in chunks:
        games = get_games(game_ids)
        print(len(games))
        print(games[:5])
        break
    reverse_offset = {}
    for game in games:
        reverse_offset[game['id']] = next((x['offset'] for x in game['vods'] if 'offset' in x), None)
    
    super_events = [(e[0], e[1], e[2], e[3], reverse_offset[e[2]]) for e in events if e[2] in reverse_offset]
    print(super_events)
    
    # Step 4: For each game, collect the live game details, and collect all relevant information on team and players
    #         At a given point of the game time
    # use /window for this
    # To get results, you must use the gameStartTime and the offset in order to add them up and find the time at which point there is information
