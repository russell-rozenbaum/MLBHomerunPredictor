import sys
import requests
import selenium
from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Access baseball-reference.com

service = Service('/Users/russellrozenbaum/Downloads/chromedriver-mac-arm64/chromedriver')
driver = webdriver.Chrome(service=service)

url = 'https://www.baseball-reference.com/leagues/majors/2024-standard-batting.shtml'
driver.get(url)

driver.implicitly_wait(10)
html = driver.page_source

# We collect/scrape data from baseball-reference.com

soup = BeautifulSoup(html, 'html.parser') 

player_batting = soup.find('div', {'id' : 'all_players_standard_batting'})

table = player_batting.find('table')

player_name = player_batting.find_all('td', {'data-stat': 'player'})
player_team = player_batting.find_all('td', {'data-stat': 'team_ID'})
player_gp = player_batting.find_all('td', {'data-stat': 'G'})
player_pa = player_batting.find_all('td', {'data-stat': 'PA'})
player_ab = player_batting.find_all('td', {'data-stat': 'AB'})
player_hits = player_batting.find_all('td', {'data-stat': 'H'})
player_hr = player_batting.find_all('td', {'data-stat': 'HR'})


# Now we write scraped data to playerData.csv file

orig_out = sys.stdout
fout = open('playerData.csv', 'w')
sys.stdout = fout

print('playerName,team,gamesPlayed,plateApp,atBats,hits,homeRuns')

c = ','
i = 0

for player in player_name :
    name = player.text.strip().replace('*', '').replace(' ', '')
    hr = player_hr[i].text.strip()
    team = player_team[i].text.strip()
    gp = player_gp[i].text.strip()
    pa = player_pa[i].text.strip()
    ab = player_ab[i].text.strip()
    hits = player_hits[i].text.strip()
    print(name, c, team, c, gp, c, pa, c, ab, c, hits, c, hr, sep='')
    i += 1
    
sys.stdout = orig_out
fout.close()





