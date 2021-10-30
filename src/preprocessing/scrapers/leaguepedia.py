from bs4 import BeautifulSoup
import csv
import mwclient
from datetime import timedelta, datetime

TEAM_NAME_MAPPINGS = {
    'Schalke 04 Evolution': 'FC Schalke 04 Evolution',
    'Schalke 04': 'FC Schalke 04 Esports',
    'SuppUp eSports': 'SAIM SE SuppUp',
    'K1CK Neosurf': 'K1CK',
    'AGO Rogue': 'AGO ROGUE',
    'Cream Real Betis': 'Cream Real Betis.EU',
    'Mousesports': 'mousesports',
    'HMA Fnatic Rising': 'Fnatic Rising',
    'C9 Academy': 'Cloud9 Academy',
    'DIG Academy': 'Dignitas Academy',
    'FLY Academy': 'FlyQuest Academy',
    'Edward Gaming': 'EDward Gaming',
    'GG Academy': 'Golden Guardians Academy',
    'IMT Academy': 'Immortals Academy',
    'EG Academy': 'Evil Geniuses Academy',
    'TL Academy': 'Team Liquid Academy',
    'EXCEL': 'Excel Esports',
    'Rogue': 'Rogue (European Team)'  
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

def get_game_winner(team_a, team_b, game_number, datetime_utc):
    site = mwclient.Site('lol.fandom.com', path='/')

    team_a_dot = ".".join([team_a[:-1], team_a[-1:]])
    team_b_dot = ".".join([team_b[:-1], team_b[-1:]])
    # Remove this if no longer useful 
    # team_a_query = TEAM_NAME_MAPPINGS[team_a] if team_a in TEAM_NAME_MAPPINGS else team_a
    # team_b_query = TEAM_NAME_MAPPINGS[team_b] if team_b in TEAM_NAME_MAPPINGS else team_b
    
    # Go back 45 minutes to catch earlier responses
    start = (datetime_utc - timedelta(minutes=59)).isoformat(' ')
    # Go ahead 45 minutes to prevent catching later ones
    end = (datetime_utc + timedelta(minutes=30)).isoformat(' ')
    query = "((TA.Short IN ('%s', '%s') AND TB.Short IN ('%s', '%s')) OR (TA.Short IN ('%s', '%s') AND TB.Short IN ('%s', '%s')))" % (team_a, team_a_dot, team_b, team_b_dot, team_b, team_b_dot, team_a, team_a_dot) + " AND SG.N_GameInMatch = %s" % (str)(game_number) + " AND (SG.DateTime_UTC between '%s' and '%s')" % (start, end),
    print(query)
    response = site.api('cargoquery',
        limit = '1',
        tables = "ScoreboardGames=SG, Teams=TA, Teams=TB, Teams=TW",
        fields = "SG.Tournament, SG.DateTime_UTC, TA.Short=Team1Short, TB.Short=Team2Short, TW.Short=WinTeamShort, SG.N_GameInMatch",
        where = query,
        join_on = "SG.Team1=TA.OverviewPage, SG.Team2=TB.OverviewPage, SG.WinTeam=TW.OverviewPage"
    )
    def get_winner(win_team):
        winner = ''
        if win_team in [team_a, team_a_dot]:
            winner = team_a
        elif win_team in [team_b, team_b_dot]:
            winner = team_b
        return winner
    results = [(get_winner(q['title']['WinTeamShort']), q['title']['N GameInMatch'], q['title']['DateTime UTC']) for q in response['cargoquery']]
    return results[0][0] if len(results) > 0 else ''
    # print(response)
    # breakpoint()
    # ((Team1 "Cloud9" AND Team2="Gen.G") OR (Team1="Gen.G" AND Team2="Cloud9")) AND (DateTime_UTC >= ;"2021-10-25")

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