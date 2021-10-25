import json

def main():
    match = json.load(open('../../lol/json/LOLmatchTimeline.json'))
    events = [event for frame in match['info']['frames'] for event in frame['events']]
    print(list(set([event['type'] for event in events])))
    