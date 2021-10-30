import os
import csv
from datetime import datetime
from scrapers import leaguepedia

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
    if os.path.isfile('lol-results.csv'):
        # Open the new file that will hold the corrected results
        out = open('lol-results-1.csv','w', newline='')
        csv_out = csv.writer(out) 

        # Read from the original file
        with open('lol-results.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            csv_out.writerow(next(reader, None))
            i = 0
            for raw_row in reader:
                i += 1
                print((str)(i))
                game = tuple(raw_row)
                if game[0] in ACADEMY_LEAGUES and game[8] == '':
                    winner = leaguepedia.get_game_winner(game[6], game[7], game[5], datetime.fromisoformat(game[4]))
                    row = game[:8] + (winner,) + game[9:]
                else:
                    row = game
                csv_out.writerow(row)
    else:
        print("Missing lol-results.csv")    
            
if __name__ == "__main__":
    clean_up_academy_games();