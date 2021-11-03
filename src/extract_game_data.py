import json
import os
import csv
from services import riot_api
from parsers.match_parser import parse_match
from parsers.timeline_parser import parse_frame
import time
from datetime import datetime

TEAM_ID_BLUE = 100
TEAM_ID_RED = 200

MATCH_DATA_HEADERS = [
    'tier',
    'division',
    'match_id',
    'patch',
    'game_duration',
    'region',
    'winning_team',
    'first_champion',
    'first_tower',
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
    csv_matches = []
    with os.scandir(os.path.join(os.path.dirname(__file__), '../data/csv')) as it:
        for entry in it:
            if entry.is_file() and entry.name.endswith('.csv'):
                with open(entry.path, 'r', newline='') as f:
                    print(entry.path)
                    reader = csv.reader(f)
                    next(reader, None)
                    csv_matches.extend([tuple(row) for row in reader])
                    print(len(csv_matches))
    
    # Now open two files:
    # - The first, lol-data-matches.csv, holds every info of the match itself
    # - The second, lol-data-timeseries.csv, holds every snapshot of the match its related to
    version = datetime.now().strftime('%Y-%m-%d-%H-%M-%S') 
    matches_filepath = os.path.join(
        os.path.dirname(__file__),
        '../output/csv/lol-data-matches-%s.csv' % version
    )
    match_frames_filepath = os.path.join(
        os.path.dirname(__file__), 
        '../output/csv/lol-data-match-frames-%s.csv' % version
    )
    error_filepath = os.path.join(
        os.path.dirname(__file__), 
        '../output/csv/lol-data-error-%s.csv' % version
    )

    cache_matches_filepath = os.path.join(os.path.dirname(__file__), '../output/csv/lol-data-matches.csv')
    cache_match_frames_filepath = os.path.join(os.path.dirname(__file__), '../output/csv/lol-data-match-frames.csv')

    # Then get the existing matches already built
    cache_matches = {}
    cache_match_frames = {}
    with open(cache_matches_filepath, 'r', newline='') as f1, open(cache_match_frames_filepath, 'r', newline='') as f2:
        reader = csv.reader(f1)
        for row in reader:
            t = tuple(row)
            cache_matches[t[0]] = t
        
        reader = csv.reader(f2)
        for row in reader:
            t = tuple(row)
            if t[0] in cache_match_frames:
                cache_match_frames[t[0]].append(t)
            else:
                cache_match_frames[t[0]] = [t]
    with open(matches_filepath, 'w', newline='') as (out1
        ), open(match_frames_filepath, 'w', newline='') as (out2
        ), open(error_filepath, 'w', newline='') as out3:
        csv_match_out = csv.writer(out1)
        csv_match_out.writerow(MATCH_DATA_HEADERS)
        csv_frame_out = csv.writer(out2)
        csv_frame_out.writerow(FRAME_DATA_HEADERS)
        error_out = csv.writer(out3)
        error_out.writerow(['error'])

        # Step 2
        i = 1
        for csv_match in csv_matches:
            print("%i/%i" % (i, len(csv_matches)))

            if csv_match[2] in cache_matches and csv_match[2] in cache_match_frames:
                match_row = csv_match[:2] + cache_matches[csv_match[2]]
                frame_rows = cache_match_frames[csv_match[2]]
                csv_match_out.writerow(match_row)
                csv_frame_out.writerows(frame_rows)
            else:
                try:
                    # if i % 100 == 0:    
                    match = riot_api.get_match_by_matchid(csv_match[2])
                    timeline = riot_api.get_match_timeline_by_matchid(csv_match[2])

                    # Sometimes, the value of the match is empty. 
                    # When this happens, skip the value.
                    if match['info']['gameMode'] == '' or 'info' not in timeline:
                        i += 1   
                        continue
                    match_row = parse_match(match)
                    csv_match_out.writerow(csv_match[:2] + match_row)

                    for frame_num in range(len(timeline['info']['frames'])):
                        frame_row = parse_frame(csv_match[2], timeline['info']['frames'], frame_num)
                        csv_frame_out.writerow(frame_row)
                except Exception as e:
                    error_out.writerow([csv_match[2]])
                    continue
            # next
            i += 1


if __name__ == "__main__":
    main()