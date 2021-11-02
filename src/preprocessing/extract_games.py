

import requests
import csv
import os
import time
from datetime import datetime, timedelta
from scrapers import leaguepedia
from scrapers.lolesports import get_tournaments_for_league, get_window, get_teams, get_completed_events

LOL_GAMES_CACHE = '__cache__/lol-games-cache.csv'
# Extracts game data from the lolesports.com API 
# Minute mark: used later to define the snapshot analyzed
def extract(minute_mark=15, output_file='', tournament_year='2021'):
    # Check if the csv file already exists
    # TODO: save on a cached CSV too (cache/lolesports-games.csv)
    if os.path.isfile(LOL_GAMES_CACHE):
        with open(LOL_GAMES_CACHE, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)
            events = [tuple(row) for row in reader]
    else:
        print("not cached!")

        # Step 0: Connect to the unofficial league of legends api
        # https://vickz84259.github.io/lolesports-api-docs/#tag/events
        
        # Step 1: Get all tournaments for every league, get the tournaments to analyze. 
        #         Then, filter the leagues, stick to data from Jan 01, 2021 and later
        # API: use /getTournamentsForLeague        
        # 
        # TODO: Specify the year the user wants (or list of years)
        tournaments = [t for t in filter(lambda x: tournament_year in x[0], get_tournaments_for_league())]

        # For each tournaments, get all the games related to it, along with their start time
        i = 0
        events = []

        for slug, tournamentId in tournaments:
            i += 1
            print((str)(i) + '/' + (str)(len(tournaments)))
            events.extend([(slug, e['match']['id'], g['id'], e['startTime'], (e['games'].index(g) + 1)) for e in get_completed_events([tournamentId]) for g in e['games']])
            
            if i % 15 == 0:
                time.sleep(5)
            # break

        # save to a file, to avoid going back to the api and scrape it all again
        with open(LOL_GAMES_CACHE,'w', newline='') as out:
            csv_out=csv.writer(out)
            csv_out.writerow(('tournament', 'match_id', 'game_id', 'start_time', 'game_number'))
            csv_out.writerows(events)

    # Step 2: Collect teams
    # TODO: save on a cached CSV too (cache/lolesports-teams.csv)
    # TODO: This does not need to be here. Send to step 2 for finding winners
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
    out = open('lol-results-2020.csv','w', newline='')
    csv_out=csv.writer(out)
    csv_out.writerow(headers)    

    for tournament, match_id, game_id, starting_time, game_number in events:
        i += 1

        # Call it the first time to get the raw starting time. We use this in order to figure out
        # What minute mark to use next
        window = get_window(game_id)
        if window is None:
            # If no window is found, do not go further; this
            # often happens whenever the game does not 
            # exist or never actually happened
            continue
    
        stripped_datetime = window['frames'][0]['rfc460Timestamp'][:-1].split('.')[0]
        timestamp = datetime.fromisoformat(stripped_datetime)
        starting_time = timestamp - timedelta(seconds=timestamp.second % 10)

        # At this step, we get the actual snapshot based
        # on the `minute_mark` parameter provided by
        # the user.
        #     
        window = get_window(game_id, "%sZ" % (starting_time + timedelta(minutes=minute_mark)).isoformat())
        game_metadata = window['gameMetadata']
        blu_teamid = window['gameMetadata']['blueTeamMetadata']['esportsTeamId']
        red_teamid = window['gameMetadata']['redTeamMetadata']['esportsTeamId']
        frame = window['frames'][0]
        

        # Get the winner from Leaguepedia Data       
        # FIXME: Send this to the second step
        winner = leaguepedia.get_game_winner(
            teams[blu_teamid],
            teams[red_teamid],
            game_number,
            timestamp
        )

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

        # TODO: Might be fun to know what champions were used in the game
        # blu_champions = [c['championId'] for c in blu_team['participantMetadata']]
        # red_champions = [c['championId'] for c in red_team['participantMetadata']]

        # Display the information from before
        # display_lane_stats(frame)
        # print(row)
        csv_out.writerow(row)

        if i % 100 == 0:
            print((str)(i) + '/' + (str)(len(events)))
            time.sleep(5)

if __name__ == "__main__":
    main();
