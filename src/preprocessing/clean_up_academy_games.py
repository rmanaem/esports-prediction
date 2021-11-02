import os
import csv
from datetime import datetime
from scrapers import leaguepedia
from scrapers.lolesports import get_window, get_teams
ACADEMY_LEAGUES = [
    'proving_grounds_2021',
    'lcs_academy_2021',
    'cblol_academy_2021', 
    'turkey_academy_league_2021', 
    'lcs_academy_2021_summer'
]

MAPPING = {
    'ZOOS': 'ZOO',
    'CLG': 'CLGA'
}
def clean_up_academy_games():
    if os.path.isfile('lol-results-1.csv'):
        # Open the new file that will hold the corrected results
        out = open('lol-results-2.csv','w', newline='')
        csv_out = csv.writer(out) 

        teams = {}
        for team in get_teams():
            teams[team['id']] = team
        
        # Read from the original file
        with open('lol-results-1.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            csv_out.writerow(next(reader, None))
            i = 0
            for raw_row in reader:
                i += 1
                game = tuple(raw_row)
                
                if game[8] == '':
                    window = get_window(game[1])
                    blu_teamid = window['gameMetadata']['blueTeamMetadata']['esportsTeamId']
                    red_teamid = window['gameMetadata']['redTeamMetadata']['esportsTeamId']
            
                    winner = leaguepedia.get_game_winner(teams[blu_teamid], teams[red_teamid], game[5], datetime.fromisoformat(game[4]))
                    row = game[:8] + (winner,) + game[9:]
                else:
                    row = game
                csv_out.writerow(row)
    else:
        print("Missing lol-results.csv")    
            
if __name__ == "__main__":
    clean_up_academy_games();