import sys
import CollectData
import Calculate
import threading


# Change, depending on whether we need to scrape and refresh data
refreshData = True
refreshSchedule = True

data = CollectData.Data()

# We simultaneously collect data from the web and create data structures
player_data_thread = threading.Thread(target=data.collectBatterData)
lineup_data_thread = threading.Thread(target=data.collectStartingLineups)
schedule_data_thread = threading.Thread(target=data.collectScheduleData)

player_data_thread.start()
lineup_data_thread.start()
schedule_data_thread.start()

schedule_data_thread.join()
lineup_data_thread.join()
player_data_thread.join()


data.printStartingLineupsToCSV()
data.printStartingPitchersToCSV()
data.printBatterDataToCSV()
data.printScheduleToCSV()


expectedHomeruns = Calculate.teamHomerunsPerGame(data)


c = ','
orig_out = sys.stdout
fout = open('expectedHomeruns.csv', 'w')
sys.stdout = fout

print('team,expectedHomeruns')
for team, hr in expectedHomeruns.items():
    print(team, c, expectedHomeruns[team], sep='')
# Close altered stdout
sys.stdout = orig_out
fout.close()
