import collectData
import threading

# Change, depending on whether we need to scrape and refresh data
refreshData = True
refreshSchedule = True

data = collectData.Data()


# We simultaneously collect data from the web and create data structures
player_data_thread = threading.Thread(target=data.collectTeamData)
schedule_data_thread = threading.Thread(target=data.collectScheduleData)

player_data_thread.start()
schedule_data_thread.start()

schedule_data_thread.join()
player_data_thread.join()

data.printTeamDataToCSV()
data.printScheduleToCSV()
data.printStartingLineupsToCSV()







