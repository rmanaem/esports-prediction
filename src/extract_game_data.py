import json
import os

TEAM_ID_BLUE = 100
TEAM_ID_RED = 200
BLUE_PARTICIPANTS = ['1','2','3','4','5']
RED_PARTICIPANTS = ['6','7','8','9','10']

def main():    
    with open('../data/json/match-by-match-id.json') as f:
        match = json.load(f)
    with open('../data/json/match-timeline-by-match-id.json') as f:
        timeline = json.load(f)
    # breakpoint()
    
    objectives = {
        'baron': None,
        'champion': None,
        'dragon': None,
        'inhibitor': None,
        'riftHerald': None,
        'tower': None
    }
    win = None
    for t in match['info']['teams']:
        for objective, info in t['objectives'].items():
            # Get firsts
            if info['first']:
                objectives[objective] = t['teamId']
            # Get the winner
            if t['win']:
                win = t['teamId']
    
    for minute_mark in [15]:
        frame = timeline['info']['frames'][minute_mark]
        # NOTE: id may not always be the same as `participantId`
        blue = [p for (id, p) in frame['participantFrames'].items() if (str)(p['participantId']) in BLUE_PARTICIPANTS]
        red = [p for (id, p) in frame['participantFrames'].items() if (str)(p['participantId']) in RED_PARTICIPANTS]

        # total gold
        red_gold = sum([p['totalGold'] for p in red])
        blue_gold = sum([p['totalGold'] for p in blue])

        # total damage to champions
        red_damage = sum([p['damageStats']['totalDamageDoneToChampions'] for p in red])
        blue_damage = sum([p['damageStats']['totalDamageDoneToChampions'] for p in blue])

        # champion kills
        all_kills = [e['killerId'] for f in timeline['info']['frames'][:minute_mark] for e in f['events'] if e['type'] == 'CHAMPION_KILL']
        blue_kills = len([k for k in all_kills if k <= 5])
        red_kills = len([k for k in all_kills if k > 5])


        breakpoint()

    print(win)
    print(objectives)
    print(blue_gold, red_gold)
    print(blue_damage, red_damage)
    print(blue_kills, red_kills)

    
if __name__ == "__main__":
    main()