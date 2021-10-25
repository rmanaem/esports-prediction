

def scrape():
    # ok

    # Step 0: Connect to the unofficial league of legends api
    # https://vickz84259.github.io/lolesports-api-docs/#tag/events
    
    # Step 1: Get All Possible Leagues
    # use /getLeagues

    # Step 2: For every league, get the schedule of events. 
    # use /getSchedule or /getCompletedEvents
    # Stick to data from Jan 01, 2021 and later

    # Step 3: For each event in a schedule, find the event details and collect all of their games and start times
    # use /getEventDetails

    # Step 4: For each game, collect the live game details, and collect all relevant information on team and players
    #         At a given point of the game time
    # use /window for this
    # To get results, you must use the gameStartTime and the offset in order to add them up and find the time at which point there is information
