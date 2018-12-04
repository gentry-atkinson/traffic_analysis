#!/usr/bin/env python3

import json
import os

fileFile = open("walks_fileNames.txt", 'r')

inFileName = "/home/user/Desktop/cs7311_data/walks/"

counter = 0

times = dict()
times["0to1"] = 0
times["1to2"] = 0
times["2to3"] = 0
times["3to4"] = 0
times["4to5"] = 0
times["5to6"] = 0
times["6to7"] = 0
times["7to8"] = 0
times["8to9"] = 0
times["9to10"] = 0
times["10to11"] = 0
times["11to12"] = 0
times["12to13"] = 0
times["13to14"] = 0
times["14to15"] = 0
times["15to16"] = 0
times["16to17"] = 0
times["17to18"] = 0
times["18to19"] = 0
times["19to20"] = 0
times["20to21"] = 0
times["21to22"] = 0
times["22to23"] = 0
times["23to24"] = 0

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

        if ("lamar" in origin and "lamar" in destination):
            timeString = item["Start Time"]
            timeString = timeString.split(':', 2)[0]
            time = int(timeString)

            if (time < 1):
                times["0to1"] += 1
            elif (time < 2):
                times["1to2"] += 1
            elif (time < 3):
                times["2to3"] += 1
            elif (time < 4):
                times["3to4"] += 1
            elif (time < 5):
                times["4to5"] += 1
            elif (time < 6):
                times["5to6"] += 1
            elif (time < 7):
                times["6to7"] += 1
            elif (time < 8):
                times["7to8"] += 1
            elif (time < 9):
                times["8to9"] += 1
            elif (time < 10):
                times["9to10"] += 1
            elif (time < 11):
                times["10to11"] += 1
            elif (time < 12):
                times["11to12"] += 1
            elif (time < 13):
                times["12to13"] += 1
            elif (time < 14):
                times["13to14"] += 1
            elif (time < 15):
                times["14to15"] += 1
            elif (time < 16):
                times["15to16"] += 1
            elif (time < 17):
                times["16to17"] += 1
            elif (time < 18):
                times["17to18"] += 1
            elif (time < 19):
                times["18to19"] += 1
            elif (time < 20):
                times["19to20"] += 1
            elif (time < 21):
                times["20to21"] += 1
            elif (time < 22):
                times["21to22"] += 1
            elif (time < 23):
                times["22to23"] += 1
            elif (time < 24):
                times["23to24"] += 1
            else:
                print("Bad value for time")

    #end of while(inFile)

#end of while(fileFile)
print ("***************Times on Lamar****************\n\n")
print ("***************Start times of Walks****************")
print("In 24 hour time")
print("0 to 1: ", times["0to1"])
print("1 to 2: ", times["1to2"])
print("2 to 3: ", times["2to3"])
print("3 to 4: ", times["3to4"])
print("4 to 5: ", times["4to5"])
print("5 to 6: ", times["5to6"])
print("6 to 7: ", times["6to7"])
print("7 to 8: ", times["7to8"])
print("8 to 9: ", times["8to9"])
print("9 to 10: ", times["9to10"])
print("10 to 11: ", times["10to11"])
print("11 to 12: ", times["11to12"])
print("12 to 13: ", times["12to13"])
print("13 to 14: ", times["13to14"])
print("14 to 15: ", times["14to15"])
print("15 to 16: ", times["15to16"])
print("16 to 17: ", times["16to17"])
print("17 to 18: ", times["17to18"])
print("18 to 19: ", times["18to19"])
print("19 to 20: ", times["19to20"])
print("20 to 21: ", times["20to21"])
print("21 to 22: ", times["21to22"])
print("22 to 23: ", times["22to23"])
print("23 to 24: ", times["23to24"])



print(counter, " total files read.")

os.system('spd-say "All done"')
