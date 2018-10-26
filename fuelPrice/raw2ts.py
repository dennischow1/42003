from datetime import date, datetime, timedelta
import re


fileList = ['2016_08.csv',
            '2016_09.csv',
            '2016_10.csv',
            '2016_11.csv',
            '2016_12.csv',
            '2017_01.csv',
            '2017_02.csv',
            '2017_03.csv',
            '2017_04.csv',
            '2017_05.csv',
            '2017_06.csv',
            '2017_07.csv',
            '2017_08.csv',
            '2017_09.csv',
            '2017_10.csv',
            '2017_11.csv',
            '2017_12.csv',
            '2018_01.csv',
            '2018_02.csv',
            '2018_03.csv',
            '2018_04.csv'
            
            ]

fuelTypeList = ['E10',
                'P95',
                'P98'
                ]

fuelType = 'P98'
postCode = '2007'

datetime_object = datetime.strptime('01/08/2016 21:46:01', '%d/%m/%Y %H:%M:%S')

#print(datetime_object)
prog1 = re.compile('\d*/\d*/\d* *\d*:\d*:\d*')
prog2 = re.compile('\d*/\d*/\d* *\d*:\d*')
prog3 = re.compile('\d*-\d*-\d* *\d*:\d*:\d*')
prog3 = re.compile('\d*-\d*-\d* *\d*:\d*')
#matchObj = prog.match('01/08/2016 21:46:01')
#if matchObj:
#    print('true')
#else:
#    print('false')
    
dateTimeList = []
priceList = []
for fileName in fileList:
    with open(fileName) as f:
        for line in f:
            if postCode in line and fuelType in line:
                keyItems = line.split(',')
                #print(keyItems[7])
                if prog1.match(keyItems[7]):
                    dateTimeList.append(datetime.strptime(keyItems[7], '%d/%m/%Y %H:%M:%S'))
                elif prog2.match(keyItems[7]):
                    dateTimeList.append(datetime.strptime(keyItems[7], '%d/%m/%Y %H:%M'))
                elif prog3.match(keyItems[7]):
                    dateTimeList.append(datetime.strptime(keyItems[7], '%Y-%m-%d %H:%M:%S'))
                elif prog4.match(keyItems[7]):
                    dateTimeList.append(datetime.strptime(keyItems[7], '%Y-%m-%d %H:%M'))

                priceList.append(keyItems[8].replace('\n', ''));
                
                #print(keyItems[7], ' ', keyItems[8].replace('\n', ''))
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
with open(postCode+'_'+fuelType, "w") as output_file:
    for price in Final_TS:
        output_file.write(str(theDay[counter]) + ',' + str(price) + '\n')
        counter += 1
output_file.closed

































