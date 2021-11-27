
# To find the team, we loop through each team object
# to find the boolean property win being toggled.
# If it is a tie, the function returns nothing
def get_winning_team(teams):
    for t in teams:
        if t['win']:
            return t['teamId']

# Prepares the objective arrays, similar to how
# `get_winning_team` operates. a first objective
# represents which team got the first one. For
# example, if Blue side killed another champion
# for first blood, objectives['champion'] 
# would equal to 100, so on so forth.
def get_objectives(teams):
    objectives = {
        'baron': None,
        'champion': None,
        'dragon': None,
        'inhibitor': None,
        'riftHerald': None,
        'tower': None
    }
    for t in teams:
        for objective, info in t['objectives'].items():
            # Get firsts
            if info['first']:
                objectives[objective] = t['teamId']
    # breakpoint()
    return objectives

def get_patch_version(patch):
    return ".".join(patch.split('.')[:2])

# Accepts a match DTO, and extracts relevant information regarding overall game statistics
def parse_match(match_dto):
    match_id = match_dto['metadata']['matchId']
    patch = get_patch_version(match_dto['info']['gameVersion'])
    game_duration = match_dto['info']['gameDuration']
    region = match_dto['info']['platformId']
    
    # Get the winning team
    winning_team = get_winning_team(match_dto['info']['teams'])
    objectives = get_objectives(match_dto['info']['teams'])
    
    return (
        match_id,
        patch,
        game_duration,
        region,
        winning_team,
        objectives['champion'],
        objectives['tower'],
        objectives['inhibitor'],
        objectives['baron'],
        objectives['dragon'],
        objectives['riftHerald'],
    )