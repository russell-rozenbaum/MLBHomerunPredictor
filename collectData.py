import sys
import requests
from bs4 import BeautifulSoup 

# Making a GET request
r = requests.get('https://www.baseball-reference.com/leagues/majors/2024-standard-batting.shtml')
if r.status_code != 200 :
    print(r)
    print("Unable to access website data")
    sys.exit()
print("Successful data access")

soup = BeautifulSoup(r.content, 'html.parser') 

#split teams and players standard batting
team_batting = soup.find('div', {'id' : 'all_teams_standard_batting'})
player_batting = soup.find('div', {'id' : 'all_players_standard_batting'})

team_hr = team_batting.find_all('td', {'data-stat': 'HR'})
player_hr = player_batting.find_all('td', {'data-stat': 'HR'})

print(player_batting)
