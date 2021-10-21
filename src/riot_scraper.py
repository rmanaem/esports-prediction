from bs4 import BeautifulSoup
import csv
import json

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
    match = json.load(open('./LOLmatchTimeline.json'))
    events = [event for frame in match['info']['frames'] for event in frame['events']]
    print(list(set([event['type'] for event in events])))
    
if __name__ == "__main__":
    main();