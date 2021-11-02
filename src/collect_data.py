from services import riot_api
import csv

def main():
    # First is setting up the api for a specific region
    # TODO: not gonna deal with this for now

    # STAGE 1: Games collection
    matchIds = []
    # Pick up the players to look at
    # TODO Loop the tier and divisions 
    tier, division, thres = 'DIAMOND', 'I', 200
    players = riot_api.get_players_for_elo(tier=tier, division=division)
    # Shuffle the players to get a randomized choice of players

    # Use this to see whether we reach the desired
    # amount of matches for a particular tier.
    carry = 0
    for summonerId in [p['summonerId'] for p in players][:50]:
        # Get the player's PUUID from his summoner record
        summoner = riot_api.get_summoner_by_id(summonerId)
        matches = riot_api.get_matches_by_puuid(summoner['puuid'])
        # breakpoint()
        matchIds.extend([(tier, division, m) for m in matches])
        carry += len(matches)
        if carry >= thres:
            break
    with open(('lol-matches-%s-%s.csv' % (tier, division)), 'w', newline='') as out:
        csv_out=csv.writer(out)
        csv_out.writerows(matchIds)

    
if __name__ == "__main__":
    main()