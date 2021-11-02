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
            remaining = (int)(limit) - count
            if (remaining < 10):
                print("%i left for %s seconds" % (remaining, time))    
            if remaining <= 1:
                print('limit reached, sleeping for %s seconds' % time)
                sleep((int)(time))
    if 'X-Method-Rate-Limit' in headers:
        print(headers['X-Method-Rate-Limit'])
        print(headers['X-Method-Rate-Limit-Count'])
    
def fetch(url, prefix=SERVER):
    response = requests.request("GET", (BASE_URL % prefix) + url, headers=HEADERS)

    # If we reach a rate-limit, use the Retry-After header with
    # some padded time before requesting the same resource again
    if response.status_code == requests.codes.too_many_requests:
        wait = (int)(response.headers['Retry-After']) + 5
        print("Too many requests detected. Sleeping for %i seconds")
        sleep(wait + 5)
        # Retry the request
        response = requests.request("GET", (BASE_URL % prefix) + url, headers=HEADERS)

    return response.json()

def get_players_for_elo(tier, division=None, page=1):
    if tier == 'GRANDMASTERS':
        url = "/lol/league/v4/grandmasterleagues/by-queue/RANKED_SOLO_5x5"
        return fetch(url)['entries']
    else:
        url = "/lol/league/v4/entries/RANKED_SOLO_5x5/%s/%s?page=%s" % (tier, division, page)
    return fetch(url)

def get_summoner_by_id(summonerId):
    url = "/lol/summoner/v4/summoners/%s" % summonerId
    return fetch(url)

def get_matches_by_puuid(puuid, count=25, type='ranked', start=0, ):
    url = "/lol/match/v5/matches/by-puuid/%s/ids?type=%s&start=%i&count=%i" % (puuid, type, start, count) 
    return fetch(url, prefix=REGION)
