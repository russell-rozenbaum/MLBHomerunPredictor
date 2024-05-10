import sys
import requests
import selenium
from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

service = Service('/Users/russellrozenbaum/Downloads/chromedriver-mac-arm64/chromedriver')
driver = webdriver.Chrome(service=service)

url = 'https://www.baseball-reference.com/leagues/majors/2024-standard-batting.shtml'
driver.get(url)
# Wait for the page to load completely
driver.implicitly_wait(10)
html = driver.page_source

# Making a GET request
# r = requests.get('https://www.baseball-reference.com/leagues/majors/2024-standard-batting.shtml')
# if r.status_code != 200 :
#     print(r)
#     print("Unable to access website data")
#     sys.exit()
# print("Successful data access")

soup = BeautifulSoup(html, 'html.parser') 

#split teams and players standard batting
team_batting = soup.find('div', {'id' : 'all_teams_standard_batting'})
player_batting = soup.find('div', {'id' : 'all_players_standard_batting'})

table = player_batting.find('table')

team_hr = team_batting.find_all('td', {'data-stat': 'HR'})
player_hr = player_batting.find_all('td', {'data-stat': 'HR'})

print(player_hr)
