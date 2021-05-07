# =============================================================================
# Filename GDP.py
# Author  Hunter Stiles
# Date 3/3/2021
# This program reads GDP data for the US and China.  It figures out the
# average yearly growth for each country and use it to prodict the growth
# until 2030 
# =============================================================================
 
import csv
from matplotlib import pyplot as plt

# =============================================================================
# loadColumn reads a csv file loads the specified column into a list
#   filename--the name of the csv file
#   column--the column number to be loaded 
#   columnList--the list to receive the data
# =============================================================================
def loadColumn(filename, column, columnList):
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            output= row[column];
            columnList.append(float(output.translate({ord(i): None for i in 'DeIncrease,'})))
            
# =============================================================================
# getGDPChange calculates the annual percent change
#   GDPList--the list containing the GDP data
#   DeltaList--the list to hold the calculated percent change
# Excluded the first year from the calculation since 2020 was an outlier  
# =============================================================================
def getGDPChange(GDPList, DeltaList):
    for i in range (1, len(GDPList)):
        DeltaList.append((GDPList[i - 1]-GDPList[i])/GDPList[i])


#create lists to hold the data
Year = []
AmericaGDP = []
ChinaGDP = []
AmericaDelta = []
ChinaDelta = []

#populate the lists
loadColumn('China.csv', 0, Year)
loadColumn('America.csv', 1, AmericaGDP)
loadColumn('China.csv', 2, ChinaGDP)
getGDPChange(AmericaGDP, AmericaDelta)
getGDPChange(ChinaGDP, ChinaDelta)

#the number of records for each country is expected to be the same
if (len(AmericaGDP) != len(ChinaGDP)):
    print("Error program expects same number of years for both countries")
    exit()

# Convert GDP from Billions to Trillions so they are easier to read
for i in range(0, len(AmericaGDP)):
    AmericaGDP[i] = AmericaGDP[i]/1000 

for i in range(0, len(ChinaGDP)):
    ChinaGDP[i] = ChinaGDP[i]/1000

#find the average annual change not including 2020 since it was an anomaly
AmericaAveDelta = sum(AmericaDelta[1:]) / (len(AmericaDelta)-1)
ChinaAveDelta = sum(ChinaDelta[1:])/ (len(ChinaDelta)-1)

#calculate the values for the future years
for i in range(0, 10):
    Year.insert(0, Year[0] + 1)
    AmericaGDP.insert(0, AmericaGDP[0] *(1 + AmericaAveDelta ))
    ChinaGDP.insert(0, ChinaGDP[0] *(1 + ChinaAveDelta ))
    AmericaDelta.insert(0, AmericaAveDelta)
    ChinaDelta.insert(0, ChinaAveDelta)
  
#print out the data
print ("\nYear      USA GDP    USA %     China GDP  China %")
print ("           (Tn $)    Change    (Tn $)     Change")
print ("------------------------------------------------")
for i in range(0, len(ChinaGDP)-1):
    print("{:.0f}".format(Year[i]),
          "{:10.2f}".format(AmericaGDP[i]),
          "{:10.2%}".format(AmericaDelta[i]),
          "{:10.2f}".format(ChinaGDP[i]),
          "{:10.2%}".format(ChinaDelta[i]))

#print out the answer to the question "Will China's GDP be larger by 2030?"
if (ChinaGDP[0] > AmericaGDP[0]):
    print("\nChina's GDP will be more than America's by 2030")
else:
    print("\nChina's GDP will not be more than America's by 2030")
    
#plot the results
plt.plot(Year,AmericaGDP,'b',label="USA")
plt.plot(Year,ChinaGDP,'r',label="China")
plt.ylabel('GDP in trillions of dollars')
plt.xlabel('Year')
plt.legend()
plt.show()

