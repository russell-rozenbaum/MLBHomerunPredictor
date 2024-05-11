import sys
import requests
import selenium
from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class Data :

    def __init__(self) :
        # Indexed by team; holds indices to players
        self.teamData = {}
        self.schedule = []


    def private_makeSoupFrom(self, url) :
         # Launch chrome driver
        service = Service('/Users/russellrozenbaum/Downloads/chromedriver-mac-arm64/chromedriver')
        driver = webdriver.Chrome(service=service)
        driver.get(url)
        driver.implicitly_wait(10)
        html = driver.page_source

        # We collect/scrape data from given url
        soup = BeautifulSoup(html, 'html.parser')

        driver.quit()

        return soup
    
    
    def private_map(self, team) :
        match team :
            case 'WSH':
                return 'WSN'
            case 'CWS' :
                return 'CHW'
            case 'SF' :
                return 'SFG'
            case 'TB' :
                return 'TBR'
            case 'SD' :
                return 'SDP'
            case 'KC' :
                return 'KCR'
            case _ :
                return team


    def collectTeamData(self) :

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
            if name != 'LgAvg per 600 PA' :
                if team not in self.teamData :
                    self.teamData[team] = {'batterData': {}, 'pitcherData': {}, 'pitcher': str, 'startingLineup': []}
                self.teamData[team]['batterData'][name] = player_info
        self.collectStartingLineups()


    def collectScheduleData(self) :
        url = 'https://baseballsavant.mlb.com/probable-pitchers'
        soup = self.private_makeSoupFrom(url)
        matchup_blocks = soup.find_all('div', class_='game-info')

        matchups = []
        for m in matchup_blocks :
            matchups.append(m.find('h2').text.strip())

        for game in matchups :
            teams = game.split(' @ ')
            self.schedule.append({'away': teams[0], 'home': teams[1]})
        


    def collectStartingLineups(self) :
        url = 'https://www.rotowire.com/baseball/daily-lineups.php'
        soup = self.private_makeSoupFrom(url)   

        # This line actually fails to grab a lineup if the game has started
        boxes = soup.find_all('div', class_='lineup is-mlb')
        for box in boxes :
            away_team = box.find('div', class_='lineup__team is-visit')
            away_team = away_team.find('div', class_='lineup__abbr').text.strip()         
            home_team = box.find('div', class_='lineup__team is-home')  
            home_team = home_team.find('div', class_='lineup__abbr').text.strip() 
            # This just matches abbreviations where the 2 websites differ
            away_team = self.private_map(away_team)
            home_team = self.private_map(home_team)

            away_lineup = box.find('ul', class_='lineup__list is-visit')
            away_lineup = away_lineup.find_all('li', class_='lineup__player')
            for chunk in away_lineup :
                away_lineup_player = chunk.find('a').text.strip().replace('*','').replace('#','')
                self.teamData[away_team]['startingLineup'].append(away_lineup_player)
            home_lineup = box.find('ul', class_='lineup__list is-home')
            home_lineup = home_lineup.find_all('li', class_='lineup__player')
            for chunk in home_lineup :
                home_lineup_player = chunk.find('a').text.strip().replace('*','').replace('#','')
                self.teamData[home_team]['startingLineup'].append(home_lineup_player)
            


    def printTeamDataToCSV(self) :
        c = ','
        # We write scraped data to playerData.csv file
        orig_out = sys.stdout
        fout = open('teamData.csv', 'w')
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

        
    def printScheduleToCSV(self) :
        c = ','
        # We write scraped data to playerData.csv file
        orig_out = sys.stdout
        fout = open('schedule.csv', 'w')
        sys.stdout = fout

        print('awayTeam,homeTeam')
        for game in self.schedule :
            print(game['away'], c, game['home'], sep='')

        # Close altered stdout
        sys.stdout = orig_out
        fout.close()


    def printStartingLineupsToCSV(self) :
        c = ','
        # We write scraped data to playerData.csv file
        orig_out = sys.stdout
        fout = open('startingLineups.csv', 'w')
        sys.stdout = fout
        lineupSize = 9

        print('team,1st,2nd,3rd,4th,5th,6th,7th,8th,9th')
        for team_name, team in self.teamData.items():
            print(team_name, sep='', end='')
            if len(team['startingLineup']) < lineupSize :
                for i in range(lineupSize) :
                    print(c, '', sep='', end='')
            else :
                for player in team['startingLineup'] :
                    print(c, player, sep='', end='')
            print('')
        # Close altered stdout
        sys.stdout = orig_out
        fout.close()



