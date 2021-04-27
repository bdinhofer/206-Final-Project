import sqlite3
import json
import os



def set_up_db(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def read_Data_From_File(filename):
    full_path = os.path.join(os.path.dirname(__file__), filename)
    f = open(full_path)
    file_data = f.read()
    f.close()
    file_data = file_data.replace("\'", "\"")
    json_data = json.loads(file_data)
    return json_data

def read_list_from_file(filename):
    full_path = os.path.join(os.path.dirname(__file__), filename)
    f = open(full_path)
    file_data = f.readlines()
    f.close()
    lines = []
    for line in file_data:
        line = line.split(',')
        new_line = []
        for j in line:
            j = j.strip()
            new_line.append(j)
        lines.append(new_line)
    return lines


def create_team_table(data, cur, conn, i):
    cur.execute("CREATE TABLE IF NOT EXISTS nba_teams (id INTEGER PRIMARY KEY, team TEXT, city TEXT, winpct INTEGER)")
    while True:
        try:
            cur.execute("INSERT INTO nba_teams (id,team,city,winpct) VALUES (?,?,?,?)", (data[i]['TEAM_ID'], data[i]['TEAM_NAME'], data[i]['TEAM_CITY'], data[i]['WIN_PCT'],))
        except:
            break
        i += 1
        if i % 25 == 0 or i > len(data):
            break
    conn.commit()
    return None 

def create_player_table(data, cur, conn, i):
    for player in data:
        if player[1]['TEAM_ABBREVIATION'] == 'TOT':
            data.remove(player)

    cur.execute("CREATE TABLE IF NOT EXISTS nba_players (team_id INTEGER, name TEXT, threes INTEGER)")
    cur.execute("SELECT id FROM nba_teams")
    lst = []
    for j in cur:
        lst.append(int(j[0]))

    while True:
        try:
            for id_ in lst:
                player = data[i]
                if id_ == data[i][1]['TEAM_ID']:
                    team_id = id_ 
            cur.execute("INSERT INTO nba_players (team_id,name,threes) VALUES (?,?,?)", (team_id, data[i][0], data[i][1]['FG3M'],))
        except:
            break
        i += 1
        if i % 25 == 0 or i > len(data):
            break
    conn.commit()
    return None

def create_city_table(lines, cur, conn, i):
    cur.execute("CREATE TABLE IF NOT EXISTS cities (city_name TEXT, population INTEGER)")
    while True:
        try:
            cur.execute("INSERT INTO cities (city_name, population) VALUES (?,?)", (lines[i][0].strip(), int(lines[i][2])))
        except:
            break
        i += 1
        if i % 25 == 0 or i > len(lines):
            break
    conn.commit()
    return None

def create_Net_worth_table(lines, cur, conn, i):
    cur.execute("CREATE TABLE IF NOT EXISTS Net_Worths (team_name TEXT, net_worth text)")
    while True:
        try:
            cur.execute("INSERT INTO Net_worths (team_name, net_worth) VALUES (?,?)", (lines[i][0].strip(), (lines[i][1])))
        except:
            break
        i += 1
        if i % 25 == 0 or i > len(lines):
            break
    conn.commit()
    return None
                                                          
def main():
    cur, conn = set_up_db('Final-Data.db')
    d = read_Data_From_File('PLAYER_STATS.txt')
    d2 = read_Data_From_File('TEAM_STATS.txt')
    city_lines = read_list_from_file('Cities.csv')
    value_lines = read_list_from_file('NetWorths.csv')
    #create_player_table(d, cur, conn, 550) #Each time this code runs increase i by 25
    #create_team_table(d2, cur, conn, 25) #Each time this code runs increase i by 25
    #create_city_table(city_lines, cur, conn, 125)
    create_Net_worth_table(value_lines, cur, conn, 100)
    conn.close()

main()



    