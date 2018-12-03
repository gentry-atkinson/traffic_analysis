#!/usr/bin/env python3

import json

fileFile = open("walks_fileNames.txt", 'r')

inFileName = "/home/user/Desktop/cs7311_data/walks/"

counter = 0

totalsForDevices = dict()
totalsForDistance = dict()
totalsForDevOverDis = dict()

while(fileFile):
    try:
        thisFileName = inFileName + fileFile.readline()
        thisFileName = thisFileName[:-1]
        inFile = open(thisFileName, 'r')
        counter += 1
        #wait = input("Press something")
    except:
        print ("End of File")
        break

    while(inFile):
        try:
            line = inFile.readline()
            item = json.loads(line)
        except:
            #print("File ", counter, " has processed.")
            break
        try:
            totalsForDevices[item["Num_Devices"]] += 1
        except KeyError:
            totalsForDevices[item["Num_Devices"]] = 1

        try:
            totalsForDistance[item["Walk_Length"]] += 1
        except KeyError:
            totalsForDistance[item["Walk_Length"]] = 1

        try:
            totalsForDevOverDis[item["Num_Devices"]][item["Walk_Length"]] += 1
        except KeyError:
            try:
                totalsForDevOverDis[item["Num_Devices"]][item["Walk_Length"]] = 1
            except KeyError:
                #print("Creating dict for totalsForDevOverDis[item[", item["Num_Devices"], "]]")
                totalsForDevOverDis[item["Num_Devices"]] = dict()
                totalsForDevOverDis[item["Num_Devices"]][item["Walk_Length"]] = 1
    #end of while(inFile)

#end of while(fileFile)

print ("*************Number of Devices*************")

for value in (totalsForDevices.keys()):
    print ("Number of walks with ", value, " devices: ", totalsForDevices[value])

print ("*************Total Distance****************")

for value in (totalsForDistance.keys()):
    print ("Number of walks with ", value, " distance covered: ", totalsForDistance[value])

print ("********Devices Over Distance**************")

for numDev in totalsForDevOverDis.keys():
    for walkLength in totalsForDevOverDis[numDev].keys():
        print ("Devices: ", numDev, "\tLength: ", walkLength, "\tTotal Walks: ", totalsForDevOverDis[numDev][walkLength])

print(counter, " total files read.")
