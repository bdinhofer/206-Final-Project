import sqlite3
import matplotlib.pyplot as plt
import re

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

def get_average_net_worths(lst, conn, cur):
    cur.execute("SELECT city_name FROM Cities")
    cities = cur.fetchall()
    net_worth_d = {}
    for city in cities:
        for tup in lst:
            if city[0] in tup[0]:
                if city not in net_worth_d:
                    net_worth_d[city[0]] = tup[1]
                net_worth_d[city[0]] += tup[1]
    return net_worth_d

def find_not_city(lst):
    for i in lst:
        


def main():
    conn = sqlite3.connect('Final-Data.db')
    cur = conn.cursor()
    clean_lst = convert_str(conn, cur)
    print(clean_lst)
    #get_average_net_worths(clean_lst, conn, cur)
    find_not_city(clean_lst)
    conn.close()

main()