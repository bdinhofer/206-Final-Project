import sqlite3
import matplotlib.pyplot as plt
import re
import numpy as np

def convert_str(conn, cur):
    cur.execute("SELECT team_name, net_worth FROM Net_Worths")
    lst = cur.fetchall()
    int_lst = []
    for tup in lst:
        if 'billion' in tup[1]:
            num = ''
            for char in tup[1]:
                if char.isnumeric():
                    num += char
            while len(num) < 10:
                num = num + '0'
            num = int(num)
        elif 'million' in tup[1]:
            num = ''
            for char in tup[1]:
                if char.isnumeric():
                    num += char
            while len(num) < 9:
                num = num + '0'
            num = int(num)
        int_lst.append((tup[0], num))
    return int_lst

def get_in_city_dict(lst, conn, cur):
    cur.execute("SELECT city_name FROM Cities")
    cities = cur.fetchall()
    d = {}
    for city in cities:
        for tup in lst:
            if city[0] in tup[0]:
                if city[0] not in d:
                    d[city[0]] = []
                d[city[0]].append(tup)
    return d

def find_not_city(clean_lst, teams_in_city):
    not_in_cities = []
    in_cities = []
    teams = []
    for teams in teams_in_city.values():
        in_cities.extend(teams)
    for tup in clean_lst:
        teams.append(tup[0])
        if tup[0] not in in_cities:
            not_in_cities.append(tup)
    return not_in_cities

def change_team_name(not_in_cities, teams_in_city):
    for team in not_in_cities:
        if 'Minnesota' in team[0]:
            if 'Minneapolis' not in teams_in_city:
                teams_in_city['Minneapolis'] = []
            teams_in_city['Minneapolis'].append(team)
        elif 'Indiana' in team[0]:
            if 'Indianapolis' not in teams_in_city:
                teams_in_city['Indianapolis'] = []
            teams_in_city['Indianapolis'].append(team)
        elif 'Utah' in team[0]:
            if 'Salt Lake City' not in teams_in_city:
                teams_in_city['Salt Lake City'] = []
            teams_in_city['Salt Lake City'].append(team)
        elif 'Brooklyn' in team[0]:
            teams_in_city['New York'].append(team)
        elif 'Golden State' in team[0]:
            teams_in_city['Oakland'].append(team)
        elif 'Tennessee' in team[0] or 'Nashville' in team[0]:
            if 'Nashville' not in teams_in_city:
                teams_in_city['Nashville'] = []
            teams_in_city['Nashville'].append(team)
        elif 'Arizona' in team[0]:
            teams_in_city['Phoenix'].append(team)
        elif 'Carolina' in team[0]:
            teams_in_city['Charlotte'].append(team)
        elif 'New England' in team[0]:
            teams_in_city['Boston'].append(team)
        elif 'Vegas' in team[0]:
            teams_in_city['Las Vegas'].append(team)
        elif 'New Jersey' in team[0]:
            teams_in_city['Newark'] = []
            teams_in_city['Newark'].append(team)
        elif 'Colorado' in team[0]:
            teams_in_city['Denver'].append(team)
        elif 'Texas' in team[0]:
            teams_in_city['Dallas'].append(team)
    del teams_in_city['Vancouver']
    return teams_in_city

def get_population(conn, cur):
    cur.execute("SELECT city_name, population FROM cities")
    return cur.fetchall()

def get_average_population(lst):
    total = 0
    for place in lst:
        total += place[1]
    return total / len(lst)     

def get_average_net(teams_in_city):
    net_worths = {}
    for city in teams_in_city:
        total = 0
        for team in teams_in_city[city]:
            total += team[1]
        avg = total/len(teams_in_city[city])
        net_worths[city] = [avg]
    return net_worths

def add_pop(pop_lst, d):
    for city in pop_lst:
        if city[0] in d:
            d[city[0]].append(city[1])
        if city[0] == 'Indianapolis city (balance)':
            d['Indianapolis'].append(city[1])
        elif city[0] == 'Nashville-Davidson metropolitan government (balance)':
            d['Nashville'].append(city[1])
    return d

def get_viz_lists(d):
    pop_lst = []
    net_worth_lst = []
    city_lst = []
    for city in d:
        pop_lst.append(d[city][1])
        net_worth_lst.append(d[city][0])
        city_lst.append(city)
    return pop_lst, net_worth_lst, city_lst

def scatter_plt(x, y, z, lst):
    average_pop = get_average_population(lst)
    plt.style.use('seaborn-pastel')
    fig = plt.figure(figsize=(20,5))
    ax = fig.add_subplot(111)
    x1 = np.array(y)
    y1 = np.array(x)
    m, b = np.polyfit(x1, y1, 1)
    ax.set_xlabel('Average Net Worth')
    ax.set_ylabel('City Population (dashed line represents average)')
    ax.set_title('Average Net Worth by City Population')
    ax.plot(x1, m*x1 + b, 'black')
    plt.hlines(average_pop, xmin = 0, xmax = 4000000000, label='Average City Population', linestyles = 'dashed')
    ax.scatter(y, x)
    plt.show()

def get_win(conn, cur):
    cities = []
    win_pcts = []
    cur.execute("SELECT winpct, city FROM nba_teams")
    lst = cur.fetchall()
    lst = sorted(lst, key = lambda x: x[0])
    for i in lst:
        cities.append(i[1])
        win_pcts.append(i[0])
    return cities, win_pcts

def bar_graph(x, y):
    plt.style.use('seaborn-pastel')
    fig = plt.figure(figsize=(30,7.5))
    ax = fig.add_subplot(111)
    ax.set_xlabel('Win Percentage')
    ax.set_ylabel('City')
    ax.set_title('Win Percentage by City')
    ax.barh(x, y)
    plt.show()

def write_data_to_csv(filename, x, y, z, x2, y2, num):
    f = open(filename, 'w')
    f.write('city,population,avgNetWorth\n')
    for i in range(len(x)):
        f.write(str(z[i]) + ',' + str(x[i]) + ',' + str(y[i]) + '\n')
    f.write('Average City Population: ' + str(num) + '\n\n')

    f.write('city,winpct\n')
    for j in range(len(x2)):
        f.write(str(x2[j]) + ',' + str(y2[j]) + '\n')
    f.close()
    return None






def main():
    conn = sqlite3.connect('Final-Data.db')
    cur = conn.cursor()
    clean_lst = convert_str(conn, cur) #creates list with Value strings changed to integers for calculations
    teams_in_city = get_in_city_dict(clean_lst, conn, cur) #creates dictionary where cities are keys and values are list of teams that play in the city
    not_in_cities = find_not_city(clean_lst, teams_in_city) #list of teams that don't include city where they play in their name. For Example "Arizona Coyotes"
    teams_in_city = change_team_name(not_in_cities, teams_in_city)#updates the dictionary to now include the teams from not_in_cities
    pop_lst = get_population(conn, cur)#list of tuples with city name as first element and population as second element
    first_viz_dict = get_average_net(teams_in_city)#dictionary of cities with sports teams and the average value of those sports teams
    first_viz_dict = add_pop(pop_lst, first_viz_dict)#adds city's population to the value list
    x, y, z = get_viz_lists(first_viz_dict)#sets list of populations equal to x, list of populations equal to y and list of cities equal to z
    #scatter_plt(x, y, z, pop_lst) #uncomment to create scatter plot
    x2, y2, = get_win(conn, cur) # sets x2 equal to list of citites and y2 equal to that cities nba team win percentage
    #bar_graph(x2, y2)#uncomment to create bar graph
    avg_pop = get_average_population(pop_lst) 
    #write_data_to_csv('cities_vis_data.csv', x, y, z, x2, y2, avg_pop)# uncomment to create csv file
    conn.close()

main()