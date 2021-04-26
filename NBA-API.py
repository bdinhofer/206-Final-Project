import sqlite3
import requests
import json
import time

#calls to the API and returns a dictionary in which the keys are players 
# and the values are dictionaries of their regular season statistics 
def get_player_stats():
    from nba_api.stats.static import players
    from nba_api.stats.endpoints import playerprofilev2
    
    player_dict = players.get_active_players()
    season_stats_2019 = []
    for player in player_dict:
        print('sleeping')
        time.sleep(2)
        player_id = player['id']
        season_stats = playerprofilev2.PlayerProfileV2(player_id=player_id)
        print('Retrieved')
        r = json.loads(season_stats.get_normalized_json())
        for stats in r["SeasonTotalsRegularSeason"]:
            if stats['SEASON_ID'] == "2019-20":
                season_stats_2019.append([player['full_name'],stats])
    f = open('PLAYER_STATS.txt', 'w')
    f.write(str(season_stats_2019))
    f.close()
    return season_stats_2019

#calls to the API and returns a dictionary in which the keys are teams 
#and the values are dictionaries of their  regular season statistics 
def get_team_stats():
    from nba_api.stats.static import teams
    from nba_api.stats.endpoints import teamyearbyyearstats
    team_dict = teams.get_teams()
    team_stats_2019 = []
    for team in team_dict:
        print('Sleeping')
        time.sleep(2)
        team_id = team['id']
        team_stats = teamyearbyyearstats.TeamYearByYearStats(team_id=team_id,league_id='00',per_mode_simple='Totals',
                                                             season_type_all_star='Regular Season')
        r = json.loads(team_stats.get_normalized_json())
        for season in r['TeamStats']:
            if season['YEAR'] == '2019-20':
                team_stats_2019.append(season)
    f = open("TEAM_STATS.txt", 'w')
    f.write(str(team_stats_2019))
    f.close()
    return team_stats_2019




def main():
    get_player_stats()

main()





    





