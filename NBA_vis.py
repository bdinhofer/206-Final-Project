import sqlite3
import matplotlib.pyplot as plt 

def grab_data(cur, conn):
    cur.execute("SELECT nba_players.name, nba_players.threes, nba_teams.team, nba_teams.city, nba_teams.winpct FROM nba_players JOIN nba_teams ON nba_players.team_id = nba_teams.id")
    return cur.fetchall()

def process_data(stats):
    team_tot_3s = {}
    teams_by_winpct = {}
    for player in stats:
        team_tot_3s[player[2]] = team_tot_3s.get(player[2], 0) + player[1]
        teams_by_winpct[player[2]] = player[4]
    
    teams_by_winpct = sorted(teams_by_winpct.items(), key=lambda x: x[1])
    teams = []
    for team in teams_by_winpct:
        teams.append(team[0])
    threes = []
    for team in teams:
        threes.append(team_tot_3s[team])
    return teams, threes

def bar_graph(x, y):
    plt.style.use('seaborn-pastel')
    fig = plt.figure(figsize=(30,7.5))
    ax = fig.add_subplot(111)
    ax.barh(x, y)
    ax.set_xlabel('3 Point FG Made')
    ax.set_ylabel('Team Ranked by Win % (Top to Bottom)')
    ax.set_title('Total 3 Point FG Made 2019-2020')
    ax.grid('True', linewidth=.1)
    plt.show()
    


def main():
    conn = sqlite3.connect('Final-Data.db')
    cur = conn.cursor()
    lst = grab_data(cur, conn)
    x, y = process_data(lst)
    bar_graph(x, y)
    conn.close()

    

main()
