# COMP 432

## Data Fields Explanation

- `tournament_slug`: Shortcode of the tournament. It's composed of the tournament's region and the year it has been held

- `game_id`: lolesports.com unique identifier for the game. It can be used alongside `getWindow` to get a game's snapshot information
- `match_id `: lolesports.com unique identifier for a match. A match can hold anywhere between 1 and 5 games. Can be used to fetch event detail information
- `patch `: The patch version, formatted as `##.##`.
- `starting_time`: Time of the first frame in which all players are loaded into the game. use it alongside the `game_id` in `getWindow` to get a particular snapshot of the match. e.g the 20th-minute mark's snapshot would be `starting_time + 20 minutes`
- `game_number`: Number of the game within a match. (note that this was estimated, and may not reflect the exact game at times)
- `blue_team`: ShortCode for the team playing on the blue (bottom-left) side of the map. Use it with `get_teams` to get more team information.
- `red_team`:  ShortCode for the team playing on the red (top-left) side of the map. Use it with `get_teams` to get more team information
- `winner`: ShortCode of the winning team. This value may be null at times due to the script's inability to fetch the information from the Leaguepedia API.
- `blue_total_gold`: Blue side's total gold accumulated amongst the five players.
- `blue_inhibitors`: Amount of inhibitors destroyed by the blue team. Inhibitors are inner base objectives that protect the Nexus, the primary win condition, from taking damage from the opponent.
- `blue_towers`: Amount of towers destroyed by the blue team. Towers are main objectives serving obstacles between an opposing team and the Nexus.
- `blue_barons`: Amount of Baron Nashors killed by the blue team. Baron Nashor is an Epic Monster that gives additional power ups to a team if it is slain. It spawns for the first time at 20 minutes, and respawns every 5 minutes after being slain. Its buff lasts for 2 minutes
- `blue_total_kills`: Cumulative amount of champion kills obtained by the blue team.
- `blue_dragons`: Amount of dragons slain by the blue team. Dragons are epic monsters that, when slain, give to the team a buff according to the type of dragon slain. It spawns for the first time at 5 minutes, and a new one respawns every 5 minutes after being slain. Once a team slays 4 dragons, no more dragon spawn again and that team is awarded an additional buff.
- `blue_total_cs`: Cumulative amount of creep killed amongst the five team members. Creeps, or minions, are small monsters that fight alongside a team that offer a small amount of gold when slain; they are a main source of income for players especially at the early stages of the game.
- `red_total_gold`: Red side's total gold accumulated amongst the five players.
- `red_inhibitors`: Amount of inhibitors destroyed by the red team. Inhibitors are inner base objectives that protect the Nexus, the primary win condition, from taking damage from the opponent.
- `red_towers`: Amount of towers destroyed by the red team. Towers are main objectives serving obstacles between an opposing team and the Nexus.
- `red_barons`: Amount of Baron Nashors killed by the red team. Baron Nashor is an Epic Monster that gives additional power ups to a team if it is slain. It spawns for the first time at 20 minutes, and respawns every 5 minutes after being slain. Its buff lasts for 2 minutes
- `red_total_kills`: Cumulative amount of champion kills obtained by the red team.
- `red_dragons`: Amount of dragons slain by the red team. Dragons are epic monsters that, when slain, give to the team a buff according to the type of dragon slain. It spawns for the first time at 5 minutes, and a new one respawns every 5 minutes after being slain. Once a team slays 4 dragons, no more dragon spawn again and that team is awarded an additional buff.
- `red_total_cs`: Cumulative amount of creep killed amongst the five team members. Creeps, or minions, are small monsters that fight alongside a team that offer a small amount of gold when slain; they are a main source of income for players especially at the early stages of the game.