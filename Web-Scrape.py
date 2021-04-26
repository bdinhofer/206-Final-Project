import requests
import json
from bs4 import BeautifulSoup

def most_valuable_NBA(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    h3 = soup.find_all('h3')
    nba_teams = []
    for tag in h3:
       #print(tag)
        h4 = tag.find_next('h4').text
        #print(h4)
        nba_teams.append((tag.text[3:].strip(), h4[9:]))
    real_list = []
    for tup in nba_teams:
        if tup[0] != '':
            real_list.append(tup)
    return real_list

def most_valuable_NFL(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    h2 = soup.find_all('h2')
    #print(h2)
    nfl_teams = []
    for tag in h2:
        name = tag.text
        value = tag.find_next('p').text
        #print(value)
        nfl_teams.append((name[3:].strip(), value[9:]))
    nfl_teams = nfl_teams[1:]
    nfl_teams_sorted = sorted(nfl_teams, key = lambda x: x[1]) 
    return nfl_teams_sorted[1:]

def most_valuable_NHL(url):
    nhl_teams = []
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    rows = soup.find_all('tr')
    for row in rows:
        name = row.find('td')
        value = name.find_next('td')
        tup = (name.text[3:].strip(), value.text)
        nhl_teams.append(tup)
    return nhl_teams[1:]

def most_valuable_MLB(url):
    mlb_teams = []
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    tags = soup.find_all('li')
    for tag in tags:
        name = tag.text.split(',')
        if len(name) > 1:
            mlb_teams.append((name[0], name[1]))
    print(mlb_teams.index(('New York Yankees', ' $5.250 billion')))
    return mlb_teams[2:]

def create_list(list1, list2, list3, list4):
    sports = [list1, list2, list3, list4]
    teams_list = []
    for lst in sports:
        #print(lst)
        teams_list.extend(lst)
    return teams_list

def write_to_file():        
    NBA_teams = most_valuable_NBA('https://www.forbes.com/sites/kurtbadenhausen/2021/02/10/nba-team-values-2021-knicks-keep-top-spot-at-5-billion-warriors-bump-lakers-for-second-place/?sh=37469da645b7')
    NFL_teams = most_valuable_NFL('https://www.forbes.com/sites/mikeozanian/2020/09/10/the-nfls-most-valuable-teams-2020-how-much-is-your-favorite-team-worth/?sh=57f46abe2ba4')
    NHL_teams = most_valuable_NHL('https://dailyhive.com/vancouver/nhl-team-values-forbes-2019')
    MLB_teams = most_valuable_MLB('https://brobible.com/sports/article/most-valuable-mlb-teams-2021-yankees-redsox/')
    teams_list = create_list(NBA_teams, NFL_teams, NHL_teams, MLB_teams)
    f = open('NetWorths.csv', 'w')
    for i in teams_list:
        f.write(i[0] + ',' + str(i[1]))
        f.write('\n')
    f.close()

write_to_file()









    