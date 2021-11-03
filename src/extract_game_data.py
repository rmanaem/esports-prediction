import json
import os
import csv
from services import riot_api
from parsers.match_parser import parse_match
from parsers.timeline_parser import parse_frame
import time

TEAM_ID_BLUE = 100
TEAM_ID_RED = 200

MATCH_DATA_HEADERS = [
    'match_id',
    'patch',
    'game_duration',
    'region',
    'winning_team',
    'first_champion',
    'first_tower'
    'first_inhibitor',
    'first_baron',
    'first_dragon',
    'first_rift_herald',
    
]

FRAME_DATA_HEADERS = [
    'match_id',  
    'frame', # Done
    'blue_total_kills', # Done
    'blue_total_gold', # Done
    'blue_total_cs', # Done
    'blue_total_damage', # Done
    'blue_towers', # Done
    'blue_plates', # Done
    'blue_inhibitors', # Done
    'blue_barons', # Done
    'blue_dragons', # Done
    'blue_rift_heralds', # Done
    'red_total_kills', # Done
    'red_total_gold', # Done
    'red_total_cs', # Done
    'red_total_damage', # Done
    'red_towers', # Done
    'red_plates', # Done
    'red_inhibitors', # Done
    'red_barons', # Done
    'red_dragons', # Done
    'red_rift_heralds', # Done
]

def main():    
    # Scan for every csv in the `data/csv` folder
    # NOTE: for now, just open one to test
    with open(os.path.join(os.path.dirname(__file__), '../data/csv/lol-matches-GRANDMASTERS-GR.csv'), 'r', newline='') as f:
        reader = csv.reader(f)
        next(reader, None)
        csv_matches = [tuple(row) for row in reader]
    
    # Now open two files:
    # - The first, lol-data-matches.csv, holds every info of the match itself
    # - The second, lol-data-timeseries.csv, holds every snapshot of the match its related to
    version = (int)(time.time()) 
    matches_filepath = os.path.join(
        os.path.dirname(__file__),
        '../output/csv/lol-data-matches-%i.csv' % version
    )
    match_frames_filepath = os.path.join(
        os.path.dirname(__file__), 
        '../output/csv/lol-data-match-frames-%i.csv' % version
    )
    with open(matches_filepath, 'w', newline='') as (out1
        ),  open(match_frames_filepath, 'w', newline='') as out2:
        csv_match_out = csv.writer(out1)
        csv_match_out.writerow(MATCH_DATA_HEADERS)
        csv_frame_out = csv.writer(out2)
        csv_frame_out.writerow(FRAME_DATA_HEADERS)

        # Step 2
        i = 1
        for csv_match in csv_matches[1059:]:
            print("%i/%i" % (i, len(csv_matches)))
            match = riot_api.get_match_by_matchid(csv_match[2])
            # Sometimes, the value of the match is empty. 
            # When this happens, skip the value.
            if match['info']['gameMode'] == '':
                print("oups")
                breakpoint()
                continue
            breakpoint()
            match_row = parse_match(match)
            csv_match_out.writerow(match_row)

            timeline = riot_api.get_match_timeline_by_matchid(csv_match[2])
            for frame_num in range(len(timeline['info']['frames'])):
                frame_row = parse_frame(csv_match[2], timeline['info']['frames'], frame_num)
                csv_frame_out.writerow(frame_row)
            i += 1
    
if __name__ == "__main__":
    main()