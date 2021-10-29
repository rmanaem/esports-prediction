from bs4 import BeautifulSoup
import csv
import mwclient
from datetime import timedelta, datetime

TEAM_NAME_MAPPINGS = {
    'Schalke 04 Evolution': 'FC Schalke 04 Evolution',
    'SuppUp eSports': 'SAIM SE SuppUp',
    'K1CK Neosurf': 'K1CK',
    'AGO Rogue': 'AGO ROGUE',
    'Cream Real Betis': 'Cream Real Betis.EU',
    'Mousesports': 'mousesports'
}
CSV_MATCH_FIELD_NAMES = [
    'date',
    'patch',
    'blue_team',
    'red_team',
    'winner',
    'blue_bans',
    'red_bans',
    'blue_picks',
    'red_picks',
    'blue_roster',
    'red_roster',
    'length',
    'blue_gold',
    'blue_kills',
    'blue_towers',
    'blue_dragons',
    'blue_barons',
    'blue_rift_heralds',
    'red_gold',
    'red_kills',
    'red_towers',
    'red_dragons',
    'red_barons',
    'red_rift_heralds'
]

def get_game(team_a, team_b, game_number, datetime_utc):
    site = mwclient.Site('lol.fandom.com', path='/')

    team_a_query = TEAM_NAME_MAPPINGS[team_a] if team_a in TEAM_NAME_MAPPINGS else team_a
    team_b_query = TEAM_NAME_MAPPINGS[team_b] if team_b in TEAM_NAME_MAPPINGS else team_b
    
    # Go back 45 minutes to catch earlier responses
    start = (datetime_utc - timedelta(minutes=59)).isoformat(' ')
    # Go ahead 45 minutes to prevent catching later ones
    end = (datetime_utc + timedelta(minutes=30)).isoformat(' ')
    response = site.api('cargoquery',
        limit = 'max',
        tables = "ScoreboardGames=SG",
        fields = "SG.Tournament, SG.DateTime_UTC, SG.Team1, SG.Team2, SG.WinTeam, SG.N_GameInMatch",
        where = "((Team1='%s' AND Team2='%s') OR (Team1='%s' AND Team2='%s'))" % (team_a_query, team_b_query, team_b_query, team_a_query) + " AND N_GameInMatch = %s" % (str)(game_number) + " AND (DateTime_UTC between '%s' and '%s')" % (start, end)
    )
    
    def get_winner(win_team):
        winner = ''
        if win_team == team_a_query:
            winner = team_a
        elif win_team == team_b_query:
            winner = team_b
        return winner
    return [(get_winner(q['title']['WinTeam']), q['title']['N GameInMatch'], q['title']['DateTime UTC']) for q in response['cargoquery']]

    # print(response)
    # breakpoint()
    # ((Team1="Cloud9" AND Team2="Gen.G") OR (Team1="Gen.G" AND Team2="Cloud9")) AND (DateTime_UTC >= ;"2021-10-25")

def main():
    # NOTE: We may use this to get the information we need: 
    # https://lol.fandom.com/wiki/Help:Leaguepedia_API
    
    match_list = []

    for page in [1,2,3,4]:
        file_name = '../../lol/html/lolesportsdata' + ('' if page == 1 else ('_' + str(page))) + '.html'    
        with open(file_name) as f:
            html_soup = BeautifulSoup(f.read(), features="html.parser")
            matches = html_soup.find_all("tr", class_="multirow-highlighter")
        for match in matches:
            match_data = [i.text for i in match.find_all('td')]
            entry = {
                'date':  match_data[0],
                'patch': match_data[1],
                'blue_team': match_data[2],
                'red_team': match_data[3],
                'winner': match_data[4],
                'blue_bans': match_data[5],
                'red_bans': match_data[6],
                'blue_picks': match_data[7],
                'red_picks': match_data[8],
                'blue_roster': match_data[9],
                'red_roster': match_data[10],
                'length': match_data[11],
                'blue_gold': match_data[12],
                'blue_kills': match_data[13],
                'blue_towers': match_data[14],
                'blue_dragons': match_data[15],
                'blue_barons': match_data[16],
                'blue_rift_heralds': match_data[17],
                'red_gold': match_data[18],
                'red_kills': match_data[19],
                'red_towers': match_data[20],
                'red_dragons': match_data[21],
                'red_barons': match_data[22],
                'red_rift_heralds': match_data[23]
            }
            match_list.append(entry)
    with open("../../lol/csv/lolesportsdata_2021.csv", "w", encoding="UTF8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_MATCH_FIELD_NAMES)
        writer.writeheader()
        writer.writerows(match_list)
    print(len(match_list))
    
if __name__ == "__main__":
    print(get_game('AGO ROGUE','SuppUp eSports',1,datetime.fromisoformat('2021-04-14 18:18:10')))