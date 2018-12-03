#!/usr/bin/env python3

import json

fileFile = open("walks_fileNames.txt", 'r')

inFileName = "/home/user/Desktop/cs7311_data/walks/"

counter = 0

while(fileFile):
    try:
        thisFileName = inFileName + fileFile.readline()
        print(thisFileName)
        inFile = open("/home/user/Desktop/cs7311_data/walks/walk_ITMF_2015-12-31.json", 'r')
        counter += 1
        wait = input("Press something")
    except:
        print ("End of File")
        break

    #item = inFile.readline()
    #print(item)
#end of while(fileFile)

print(counter, " total files read.")
