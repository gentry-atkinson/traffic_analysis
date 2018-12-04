#!/usr/bin/env python3

import json
import os

fileFile = open("walks_fileNames.txt", 'r')

inFileName = "/home/user/Desktop/cs7311_data/walks/"

counter = 0

speeds = dict()
speeds["0to10"] = 0;
speeds["10to20"] = 0;
speeds["20to30"] = 0;
speeds["30to40"] = 0;
speeds["40to50"] = 0;
speeds["50to60"] = 0;
speeds["60plus"] = 0;

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

        origin = item["Origin"]
        destination = item["Destination"]

        if ("riverside" in origin and "riverside" in destination):
            oSpeed = float(item["Speed at Origin"])
            dSpeed = float(item["Speed at Destination"])
            aSpeed = (oSpeed + dSpeed) / 2

            if (aSpeed < 10):
                speeds["0to10"] += 1
            elif (aSpeed < 20):
                speeds["10to20"] += 1
            elif (aSpeed < 30):
                speeds["20to30"] += 1
            elif (aSpeed < 40):
                speeds["30to40"] += 1
            elif (aSpeed < 50):
                speeds["40to50"] += 1
            elif (aSpeed < 60):
                speeds["50to60"] += 1
            elif (aSpeed >= 60):
                speeds["60plus"] += 1
            else:
                print("Bad Value for speed.")
    #end of while(inFile)

#end of while(fileFile)
print("**********Speeds on Riverside****************\n\n")
print("***********Speeds of Ranges******************")
print("Lower bound inclusive.")
print("0 to 10 mph: ", speeds["0to10"])
print("10 to 20 mph: ", speeds["10to20"])
print("20 to 30 mph: ", speeds["20to30"])
print("30 to 40 mph: ", speeds["30to40"])
print("40 to 50 mph: ", speeds["40to50"])
print("50 to 60 mph: ", speeds["50to60"])
print("60+ mph: ", speeds["60plus"])

print(counter, " total files read.")

os.system('spd-say "All done"')
