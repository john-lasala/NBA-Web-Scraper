import sys
import getpass
import requests
import datetime
import pandas as pd
import texttable as ttable
from operator import itemgetter
from collections import OrderedDict
from bs4 import BeautifulSoup

# Bring up menu screen
def menu():
    print('\nMain Menu - NBA Web Scraper')
    print('1: League Leaders\n2: Current Standings\n3: Past Champions\n4: Exit')

    # Read input as password for cleaner output
    user_input = int(getpass.getpass(prompt = ''))
    selection_dictionary = {
        '1' : 'League Leaders',
        '2' : 'Current Standings',
        '3' : 'Past Champions',
        '4' : 'Exit'
    }
    
    # Error Handling
    if user_input > 4 or user_input < 1:
        print('Error, redo selection')
        menu()
        return
    # Match user input with dictionary and call the correlating function
    print('You selected: ' + selection_dictionary[str(user_input)]  + '\n')
    print('=' * 80 + '\n')
    if user_input == 1:
        leagueLeaders()
    if user_input == 2:
        currentStandings()
    if user_input == 3:
        pastChampions()
    if user_input == 4:
        return
    menu()
    return

def leagueLeaders():
    # User selects which data to access
    print('''Select which league leader to display:\n1. Points Per Game\n2. Rebounds Per Game\n3. Assists Per Game
4. Steals Per Game\n5. Blocks Per Game\n6. Free Throw Percentage\n7. Main Menu''')
    
    user_input = int(getpass.getpass(prompt = ''))
    selection_dictionary = {
        '1' : 'Points Per Game',
        '2' : 'Rebounds Per Game',
        '3' : 'Assists Per Game',
        '4' : 'Steals Per Game',
        '5' : 'Blocks Per Game',
        '6' : 'Free Throw Percentage',
        '7' : 'Main Menu'
    }

    print('You selected: ' + selection_dictionary[str(user_input)] + '\n')
    print('=' * 80)
    # Check for valid and invalid inputs
    if user_input == 7:
        return
    elif user_input > 7 or user_input <= 0:
        print('Error: false input')
        leagueLeaders()
        return
    else:
        pointsPerGame(user_input, 'https://www.basketball-reference.com/leagues/NBA_2020_per_game.html')
        leagueLeaders()
    return

def pointsPerGame(selection, URL):
    headers = {'User-Agent': 'Mozilla/5.0'}
    result = requests.get(URL, headers = headers)
    # Error handling for invalid URLs
    try:
        result.raise_for_status()
    except requests.exceptions.RequestException as e:
        print (e)
        sys.exit()

    # Get HTML from webpage
    soup = BeautifulSoup(result.content, 'html.parser')
    stat_list = []
    player_list = []

    # Download the user-requested data based on their input
    if selection == 1:
        for Points in soup.find_all('td', {'data-stat' : 'pts_per_g'}):
            stat_list.append(Points.text)
    if selection == 2:
        for Rebounds in soup.find_all('td', {'data-stat' : 'trb_per_g'}):
            stat_list.append(Rebounds.text)
    if selection == 3:
        for Assists in soup.find_all('td', {'data-stat' : 'ast_per_g'}):
            stat_list.append(Assists.text)
    if selection == 4:
        for Steals in soup.find_all('td', {'data-stat' : 'stl_per_g'}):
            stat_list.append(Steals.text)
    if selection == 5:
        for Blocks in soup.find_all('td', {'data-stat' : 'blk_per_g'}):
            stat_list.append(Blocks.text)
    if selection == 6:
        for player in soup.find_all('td', {'data-stat' : 'player'}):
            player_list.append(player.text)
        for freeThrow in soup.find_all('td', {'data-stat' : 'ft_pct'}):
            stat_list.append(freeThrow.text)
        for i in range(0, len(stat_list)):
            if stat_list[i]:
                stat_list[i] = float(stat_list[i]) * 100.0
            else:
                stat_list[i] = 0.0

        # Making a sorted and ordered dictonary for free throw percentages
        dictionary = {player_list[i]: stat_list[i] for i in range(len(player_list))}

        sortedList = OrderedDict(sorted(dictionary.items(), key=itemgetter(1), reverse=True))
        names = []
        stats = []
        for index,value in sortedList.items():
            names.append(index)
            stats.append(value)

        tab = ttable.Texttable()
        headers = ['Player', 'Percentage']
        tab.header(headers)
        r = list(map('{:.2f}%'.format, stats))
        for row in zip(names, r):
            tab.add_row(row)

        chart = tab.draw()
        print(chart)
        print('\n' + '=' * 80 + '\n')
        return


    for player in soup.find_all('td', {'data-stat' : 'player'}):
        player_list.append(player.text)

    for i in range(0, len(stat_list)):
        if stat_list[i]:
            stat_list[i] = float(stat_list[i])
        else:
            stat_list[i] = 0
    
    # Making a sorted and ordered dictionary for any other data reuqested
    dictionary = {player_list[i]: stat_list[i] for i in range(len(player_list))}

    sortedList = OrderedDict(sorted(dictionary.items(), key=itemgetter(1), reverse=True))
    names = []
    stats = []
    stats_dictionary = {
        '1' : 'Points',
        '2' : 'Rebounds',
        '3' : 'Assists',
        '4' : 'Steals',
        '5' : 'Blocks'
    }
    for index,value in sortedList.items():
        names.append(index)
        stats.append(value)
    
    # Set up the text table for the data
    tab = ttable.Texttable()
    headers = ['Players', stats_dictionary[str(selection)]]
    tab.header(headers)
    my_formatted_list = [ '%.2f' % elem for elem in stats ]
    for row in zip(names, my_formatted_list):
        tab.add_row(row)

    chart = tab.draw()
    print(chart)
    print('\n' + '=' * 80 + '\n')
    return None

def currentStandings():
    # Initialize webpage we are trying to access
    URL = 'https://www.basketball-reference.com/leagues/NBA_2020_standings.html'
    headers = {'User-Agent': 'Mozilla/5.0'}
    result = requests.get(URL, headers = headers)

    # Error handling for invalid URL
    try:
        result.raise_for_status()
    except requests.exceptions.RequestException as e:
        print (e)
        sys.exit()

    # Convert HTML data to list of tables
    soup = BeautifulSoup(result.content, 'html.parser')
    table = pd.read_html(result.text)

    # Print out current Eastern and Western Conference standings
    print(table[0].to_string(index=False) + '\n')
    print('=' * 80 + '\n')
    print(table[1].to_string(index=False))
    print('\n' + '=' * 80)
    return None

def pastChampions():
    URL = 'https://www.basketball-reference.com/playoffs/'
    headers = {'User-Agent': 'Mozilla/5.0'}
    result = requests.get(URL, headers = headers)

    # Error handling for invalid URL
    try:
        result.raise_for_status()
    except requests.exceptions.RequestException as e:
        print (e)
        sys.exit()

    soup = BeautifulSoup(result.content, 'html.parser')
    teams = []
    years = []
    time = datetime.datetime.now()
    limit = time.year - 1976 + 1
    attempts = 0
    
    # Getting data from teams since the NBA-ABA Merger that took place in 1976
    for team in soup.find_all('td', {'data-stat': 'champion'}):
        attempts += 1
        if attempts == limit:
            break
        teams.append(team.text)
    attempts = 0
    for year in soup.find_all('th', {'data-stat': 'year_id'}):
        attempts += 1
        if attempts == limit+1:
            break
        years.append(year.text)

    for i in range(1, len(years)):
        years[i-1] = years[i]

    # Set up table for all of the past champions
    tab = ttable.Texttable()
    headers = ['Team', 'Year']
    tab.header(headers)

    for row in zip(teams, years):
        tab.add_row(row)

    chart = tab.draw()
    print(chart)
    print('\n' + '=' * 80)
    return None

if __name__ == '__main__':
    menu()
