from bs4 import BeautifulSoup
import csv

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

def main():
    match_list = []

    for page in [1,2,3,4]:
        file_name = './lolesportsdata' + ('' if page == 1 else ('_' + str(page))) + '.html'    
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
    with open("lolesportsdata_2021.csv", "w", encoding="UTF8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_MATCH_FIELD_NAMES)
        writer.writeheader()
        writer.writerows(match_list)
    print(len(match_list))
    
if __name__ == "__main__":
    main();