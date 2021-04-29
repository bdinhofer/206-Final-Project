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
    winpcts = []
    for team in teams_by_winpct:
        teams.append(team[0])
        winpcts.append(team[1])
    threes = []
    for team in teams:
        threes.append(team_tot_3s[team])
    return teams, threes, winpcts

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

def write_data_to_csv(filename, x, y, wins):
    f = open(filename, 'w')
    f.write('team,total3s,win%\n')
    for i in range(len(x)):
        f.write(str(x[i]) + ',' + str(y[i]) + ',' + str(wins[i]) + '\n')
    f.write('\n')
    f.close()
    return None
    
    


def main():
    conn = sqlite3.connect('Final-Data.db')
    cur = conn.cursor()
    lst = grab_data(cur, conn)
    x, y, wins = process_data(lst)
    bar_graph(x, y) #uncomment to create bar graph
    conn.close()
    write_data_to_csv('nba_vis_data.csv', x, y, wins) #uncomment to create csv file


    

main()
