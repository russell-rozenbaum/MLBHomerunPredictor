import sys
import requests
import selenium
from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Not sure I want Data to be a class... only need one instance
class Data :
    def __init__(self) :
        # Indexed by team; holds indices to players
        self.teamData = {}
        self.schedule = {}
    


    def private_makeSoupFrom(self, url) :
         # Access baseball-reference.com
        service = Service('/Users/russellrozenbaum/Downloads/chromedriver-mac-arm64/chromedriver')
        driver = webdriver.Chrome(service=service)
        driver.get(url)
        driver.implicitly_wait(10)
        html = driver.page_source

        # We collect/scrape data from given url
        soup = BeautifulSoup(html, 'html.parser') 
        return soup
    


    def collectPlayerData(self) :

        url = 'https://www.baseball-reference.com/leagues/majors/2024-standard-batting.shtml'
        soup = self.private_makeSoupFrom(url)
       
        player_batting = soup.find('div', {'id' : 'all_players_standard_batting'})

        table = player_batting.find('table')

        player_name = player_batting.find_all('td', {'data-stat': 'player'})
        player_team = player_batting.find_all('td', {'data-stat': 'team_ID'})
        player_gp = player_batting.find_all('td', {'data-stat': 'G'})
        player_pa = player_batting.find_all('td', {'data-stat': 'PA'})
        player_ab = player_batting.find_all('td', {'data-stat': 'AB'})
        player_hits = player_batting.find_all('td', {'data-stat': 'H'})
        player_hr = player_batting.find_all('td', {'data-stat': 'HR'})

        # Define a hash table / dictionary for player data
        # We index by team, as we ultimately try to calculate team's
        # expected homeruns hit in *given* game
        playerData = {}

        for i in range(len(player_name)) :
            team = player_team[i].text.strip()
            name = player_name[i].text.strip().replace('*','')
            player_info = {
            'gp' : int(player_gp[i].text.strip()),
            'pa' : int(player_pa[i].text.strip()),
            'ba' : int(player_ab[i].text.strip()),
            'hits' : int(player_hits[i].text.strip()),
            'hr' : int(player_hr[i].text.strip())
            }
            if team not in self.teamData:
                self.teamData[team] = {'batterData': {}, 'pitcherData': {}}
            self.teamData[team]['batterData'][name] = player_info



    def printBatterDataToCSV(self) :
        c = ','
        i = 0

        # We write scraped data to playerData.csv file
        orig_out = sys.stdout
        fout = open('playerData.csv', 'w')
        sys.stdout = fout

        print('playerName,team,gamesPlayed,plateApp,atBats,hits,homeRuns')
        for team_name, team_data in self.teamData.items():
            for player_name, player in team_data['batterData'].items():
                print(player_name, c, team_name, c, player['gp'],
                       c, player['pa'], c, player['pa'], c, player['hits'],
                         c, player['hr'], sep='')
        # Close altered stdout
        sys.stdout = orig_out
        fout.close()



    def collectScheduleData(self) :
        None


