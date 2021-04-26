import requests
import json
from bs4 import BeautifulSoup
import sqlite3

#Gets 100 mosrt populous cities from Data USA API.
def get_city_populations():
    pop_list = []
    base_url = 'https://datausa.io/api/data?'
    params = {'drilldowns': 'Place', 'measures': 'Population', 'year':'latest'}
    resp = requests.get(base_url, params)
    resp = json.loads(resp.text)
    for city in resp['data']:
        pop_list.append((city['Place'], city['Population']))
    return pop_list

#Need to use webscraping to find Toronto's popu
def get_pop_toronto():
    r = requests.get('https://en.wikipedia.org/wiki/List_of_the_100_largest_municipalities_in_Canada_by_population')
    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find('tbody')
    row1 = table.find('tr').find_next('tr')
    #print(row1)
    cols = row1.find_all('td')
    pop = cols[8].text
    print(pop)
    name = table.find('td').find_next('td')
    tor = name.find('a').text
    new_pop = ''
    for char in pop.strip():
        if char != ',':
            new_pop += char
    new_pop = int(new_pop)
    tup = (tor + ', ON', new_pop)
    return tup

def sort_pop_list(lst, tup):
    lst.append(tup)
    sorted_lst = sorted(lst, key = lambda x: x[1], reverse = True)
    return sorted_lst[:150]

def write_to_file():
    city_pops = (get_city_populations())
    tor_tuple = (get_pop_toronto())
    full_list = sort_pop_list(city_pops, tor_tuple)
    f = open('Cities.csv', 'w')
    for i in full_list:
        f.write(i[0] + ',' + str(i[1]))
        f.write('\n')
    f.close()

write_to_file()
    



