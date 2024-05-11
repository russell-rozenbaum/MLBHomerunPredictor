import collectData
import threading

# Change, depending on whether we need to scrape and refresh data
refreshData = True
refreshSchedule = True

data = collectData.Data()

# We simultaneously collect data from the web and create data structures
player_data_thread = threading.Thread(target=data.collectBatterData)
lineup_data_thread = threading.Thread(target=data.collectStartingLineups)
schedule_data_thread = threading.Thread(target=data.collectScheduleData)

lineup_data_thread.start()
player_data_thread.start()
schedule_data_thread.start()

schedule_data_thread.join()
lineup_data_thread.join()
player_data_thread.join()

data.printStartingLineupsToCSV()
data.printBatterDataToCSV()
data.printScheduleToCSV()




