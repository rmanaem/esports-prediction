

def get_winning_team(teams):
    for t in teams:
        if t['win']:
            return t['teamId']
    
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