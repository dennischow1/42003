from datetime import date, datetime, timedelta
import re


fileName = 'crude.csv'


datetime_object = datetime.strptime('01/08/2016 21:46:01', '%d/%m/%Y %H:%M:%S')

dateTimeList = []
priceList = []

with open(fileName) as f:
    for line in f:
        keyItems = line.split(',')
        dateTimeList.append(datetime.strptime(keyItems[0], '%d/%m/%Y'))
        priceList.append(keyItems[1]);
f.closed

tempStartDateTime = dateTimeList[0]

tempMorningDateTime = tempStartDateTime.replace(hour=0, minute=0, second=0)
tempNoonDateTime = tempStartDateTime.replace(hour=12, minute=0, second=0)
tempNightDateTime = tempStartDateTime.replace(hour=23, minute=59, second=59)

tempMorningDateTime = tempMorningDateTime + timedelta(days=1)

startDate = datetime(2016,8,1,0,0,0)
endDate = datetime(2018,4,30,23,59,59)
totalDays = (endDate - startDate).days
Final_TS = [0]*totalDays*2

tempStart = startDate
tempEnd = tempStart + timedelta(hours=12)
lastPrice = 0;
theDay = []
for i in range(0, len(Final_TS)):

    price_in_same_time_intervel = 0
    price_in_same_time_intervel_counter = 0
    theDay.append(tempStart.weekday())
    for datetime_i in range(0, len(dateTimeList)):
        if tempStart <= dateTimeList[datetime_i] and dateTimeList[datetime_i] < tempEnd:
            price_in_same_time_intervel += float(priceList[datetime_i])
            price_in_same_time_intervel_counter += 1

    tempStart = tempStart + timedelta(hours=12)
    tempEnd = tempStart + timedelta(hours=12)

    if price_in_same_time_intervel_counter > 0:
        Final_TS[i] = price_in_same_time_intervel/price_in_same_time_intervel_counter
        lastPrice = Final_TS[i]
    else:
        if lastPrice > 0:
            Final_TS[i] = lastPrice
        else:
            Final_TS[i] = 0

counter = 0
with open('crude', "w") as output_file:
    for price in Final_TS:
        output_file.write(str(theDay[counter]) + ',' + str(price) + '\n')
        counter += 1
output_file.closed

































