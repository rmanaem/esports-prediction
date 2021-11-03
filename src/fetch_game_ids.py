from services import riot_api
import csv

DIVISIONS = ['I','II','III','IV']
TIERS = {
    'BRONZE': (DIVISIONS,1250),
    'GOLD': (DIVISIONS,1250),
    'DIAMOND': (DIVISIONS,1250),
    'GRANDMASTERS': (['GR'],5000)
}

# Get a list of game ids for the tiers specified above.
# Each tier holds a division. The algorithm is set
# such that an equal amount of match ids are 
# collected across each divisions equally.
#
def main():
    # First is setting up the api for a specific region
    # TODO: not gonna deal with this for now
    # api = new RiotAPI(REGION)

    # Loop through the tiers from which 
    # we want to extract the games
    for tier, (divisions, thres) in list(TIERS.items()):
        for division in divisions:
            print("Completing %s %s matches" % (tier, division))
            # STAGE 1: Games collection for the tier
            matchIds = []
            # Pick up the players to look at
            # TODO Loop the tier and divisions 
            players = riot_api.get_players_for_elo(tier=tier, division=division)
            # Shuffle the players to get a randomized choice of players

            # Use this to see whether we reach the desired
            # amount of matches for a particular tier.
            carry = 0
            for summonerId in [p['summonerId'] for p in players]:
                # Get the player's PUUID from his summoner record
                summoner = riot_api.get_summoner_by_id(summonerId)
                matches = riot_api.get_matches_by_puuid(summoner['puuid'])
                matchIds.extend([(tier, division, m) for m in matches])
                carry += len(matches)
                print("Completed %i out of %i matches" % (carry, thres)) 
                if carry >= thres:
                    break

            # Matches are saved on an all-or-nothing basis. Hence, if the script 
            # fails, the script must be restarted. Each tier and division is
            # saved separately; for DIAMOND I, the games will be saved
            # inside (lol-matches-DIAMOND-I.csv)
            with open(('lol-matches-%s-%s.csv' % (tier, division)), 'w', newline='') as out:
                csv_out=csv.writer(out)
                csv_out.writerows(matchIds)

    
if __name__ == "__main__":
    main()