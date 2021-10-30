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
    '100 Academy': '100 Thieves Academy',
    'EG Prodigies': 'Evil Geniuses Prodigies',
    'Vodafone Giants': 'Vodafone Giants.Spain', 
    'EXCEL': 'Excel Esports',
    'Unicorns of Love': 'Unicorns Of Love.CIS',
    '1907 Fenerbahçe Espor Akademi': '1907 Fenerbahçe Academy',
    'NASR eSports Turkey Academy': 'NASR eSports Turkey Academy',
    'Rogue': 'Rogue (European Team)',
    'kt Challengers': 'KT Rolster Challengers',
    'HLE Challengers': 'Hanwha Life Esports Challengers',
    'GEN Challengers': 'Gen.G Challengers',
    'NS Challengers': 'Nongshim RedForce Challengers',
    'LSB Challengers': 'Liiv SANDBOX Challengers',
    'AF Challengers': 'Afreeca Freecs Challengers',
    'BRO Challengers': 'Fredit BRION Challengers',
    'Vorax Liberty': 'Vorax',
    'Netshoes Miners': 'Cruzeiro eSports',

}

def get_game_winner(team_a, team_b, game_number, datetime_utc):
    

    # Go back 75 minutes to catch earlier responses
    start = (datetime_utc - timedelta(minutes=85)).isoformat(' ')
    # Go ahead 30 minutes to prevent catching later ones
    end = (datetime_utc + timedelta(minutes=45)).isoformat(' ')

    # Extract Code and name from both teams
    code_a, code_b = team_a['code'], team_b['code']
    name_a, name_b = team_a['name'], team_b['name']

    site = mwclient.Site('lol.fandom.com', path='/')

    # Step 1: Query by Code
    # Most reliable way, since most codes in Riot API match
    # With the ones in leaguepedia. but 20% of them may not match
    
    # Converts the codes from TSMA to TSM.A
    code_a_dot = ".".join([code_a[:-1], code_a[-1:]])
    code_b_dot = ".".join([code_b[:-1], code_b[-1:]])
    
    # Normalize the names to search (if needed)
    name_a = TEAM_NAME_MAPPINGS[name_a] if name_a in TEAM_NAME_MAPPINGS else name_a
    name_b = TEAM_NAME_MAPPINGS[name_b] if name_b in TEAM_NAME_MAPPINGS else name_b

    code_query = "((TA.Short IN ('%s', '%s') AND TB.Short IN ('%s', '%s')) OR (TA.Short IN ('%s', '%s') AND TB.Short IN ('%s', '%s')))" % (code_a, code_a_dot, code_b, code_b_dot, code_b, code_b_dot, code_a, code_a_dot) + " AND SG.N_GameInMatch = %s" % (str)(game_number) + " AND (SG.DateTime_UTC between '%s' and '%s')" % (start, end),
    
    response = site.api('cargoquery',
        limit = '1',
        tables = "ScoreboardGames=SG, Teams=TA, Teams=TB, Teams=TW",
        fields = "SG.Tournament, SG.DateTime_UTC, TA.Short=Team1Short, TB.Short=Team2Short, TW.Short=WinTeamShort, SG.N_GameInMatch",
        where = code_query,
        join_on = "SG.Team1=TA.OverviewPage, SG.Team2=TB.OverviewPage, SG.WinTeam=TW.OverviewPage"
    )
    def get_winner(win_team):
        winner = ''
        if win_team in [name_a, code_a, code_a_dot]:
            winner = code_a
        elif win_team in [name_b, code_b, code_b_dot]:
            winner = code_b
        return winner
    
    # Extract the results from the first response
    results = [(get_winner(q['title']['WinTeamShort']), q['title']['N GameInMatch'], q['title']['DateTime UTC']) for q in response['cargoquery']]

    # Remove this if no longer useful 
    # team_a_query = TEAM_NAME_MAPPINGS[team_a] if team_a in TEAM_NAME_MAPPINGS else team_a
    # team_b_query = TEAM_NAME_MAPPINGS[team_b] if team_b in TEAM_NAME_MAPPINGS else team_b
    
    if len(results) > 0:
        # We got a match; send back the first team returned
        return results[0][0]
    else:
        name_query = "((LOWER(SG.Team1)='%s' AND LOWER(SG.Team2)='%s') OR (LOWER(SG.Team1)='%s' AND LOWER(SG.Team2)='%s'))" % (name_a.lower(), name_b.lower(), name_b.lower(), name_a.lower()) + " AND SG.N_GameInMatch = %s" % (str)(game_number) + " AND (SG.DateTime_UTC between '%s' and '%s')" % (start, end),

        # No match, retry a query using the name of the team
        response = site.api('cargoquery',
            limit = '1',
            tables = "ScoreboardGames=SG",
            fields = "SG.Tournament, SG.DateTime_UTC, SG.Team1, SG.Team2, SG.WinTeam",
            where = name_query
        )
        results = [(get_winner(q['title']['WinTeam']), q['title']['DateTime UTC']) for q in response['cargoquery']]
        if len(results) > 0:
            # We got a match; send back the first team returned
            return results[0][0]
        else:
            print(name_query)
            print("============")
    # print(response)
    # breakpoint()
    # ((Team1 "Cloud9" AND Team2="Gen.G") OR (Team1="Gen.G" AND Team2="Cloud9")) AND (DateTime_UTC >= ;"2021-10-25")
  
if __name__ == "__main__":
    print(get_game('AGO ROGUE','SuppUp eSports',1,datetime.fromisoformat('2021-04-14 18:18:10')))