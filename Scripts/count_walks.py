#!/usr/bin/env python3

import json

fileFile = open("walks_fileNames.txt", 'r')

inFileName = "/home/user/Desktop/cs7311_data/walks/"

counter = 0

totalsForDevices = dict()
totalsForDistance = dict()

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
        except:
            totalsForDevices[item["Num_Devices"]] = 1

        try:
            totalsForDistance[item["Walk_Length"]] += 1
        except:
            totalsForDistance[item["Walk_Length"]] = 1
    #end of while(inFile)

#end of while(fileFile)

for value in sorted(totalsForDevices.keys()):
    print ("Number of walks with ", value, " devices: ", totalsForDevices[value])

for value in sorted(totalsForDistance.keys()):
    print ("Number of walks with ", value, " distance covered: ", totalsForDistance[value])

print(counter, " total files read.")
