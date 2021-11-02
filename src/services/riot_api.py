import requests
from time import sleep

# Region Analyzed. Must stay consistent throughout the client use
REGION = 'EUROPE'
SERVER = 'euw1'

# URL used in the api
BASE_URL = 'https://%s.api.riotgames.com'

# API Token to use
RIOT_TOKEN = 'RGAPI-772b30bf-937c-4853-987e-6bd5e0e8145f'
HEADERS = {
  'X-Riot-Token': RIOT_TOKEN
}


def check_limits(headers):
    # TODO: make sure we dont go over the limit
    if 'X-App-Rate-Limit' in headers:
        limits = headers['X-App-Rate-Limit'].split(',')
        counts = headers['X-App-Rate-Limit-Count'].split(',')
        for i in range(len(limits)):
            limit, time = limits[i].split(':')
            count = (int)(counts[i].split(':')[0])
            
            if (int)(limit) - count < 3:
                print('limit reached, sleeping for %i seconds') % time
                sleep(time)
    # if 'X-Method-Rate-Limit' in headers:
        # print(headers['X-Method-Rate-Limit'])
        # print(headers['X-Method-Rate-Limit-Count'])
    
def fetch(url, prefix=SERVER):
    response = requests.request("GET", (BASE_URL % prefix) + url, headers=HEADERS)
    check_limits(response.headers)
    return response.json()

def get_players_for_elo(tier, division=None, page=1):
    url = "/lol/league/v4/entries/RANKED_SOLO_5x5/%s/%s?page=%s" % (tier, division, page)
    return fetch(url)

def get_summoner_by_id(summonerId):
    url = "/lol/summoner/v4/summoners/%s" % summonerId
    return fetch(url)

def get_matches_by_puuid(puuid, count=25, type='ranked', start=0, ):
    url = "/lol/match/v5/matches/by-puuid/%s/ids?type=%s&start=%i&count=%i" % (puuid, type, start, count) 
    return fetch(url, prefix=REGION)
