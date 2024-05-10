import collectData

# Change, depending on whether we need to scrape and refresh data
refreshData = False
refreshSchedule = True

data = collectData.Data()

data.collectPlayerData() if refreshData else None
data.collectScheduleData() if refreshSchedule else None

data.printScheduleToCSV()




