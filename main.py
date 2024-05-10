import collectData

# Change, depending on whether we need to scrape and refresh data
refresh = True

data = collectData.Data()

data.collectPlayerData() if refresh else None
data.collectScheduleData() if refresh else None

data.printBatterDataToCSV()




