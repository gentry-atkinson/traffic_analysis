#!/usr/bin/env python

import json
import os

inFile = open("Individual_Traffic_Match_Files__ITMF_Test_Data.json", 'r')

try:
    os.system('mkdir split_traffic_files')
except:
    print("Output directory already exists")


oldDate = ""
counter = 0
fileCounter = 0

line = inFile.readline()

while(inFile):
    line = inFile.readline()
    try:
        item = json.loads(line)
        #print (item["Day of Week"])
        date = item['Start Time']
        date = date.split('T', 1)[0]
        #print (date)
        if (date != oldDate):
            oldDate = date
            filename = "split_traffic_files/ITMF_" + date
            outFile = open(filename, 'w')
            #outFile.write("New file")
            item = json.dumps(item)
            outFile.write(item)
            fileCounter += 1
        else:
            item = json.dumps(item)
            outFile.write(item)
        counter += 1
    except:
        print ("error in converter loop")
        break

print(counter, " entries written into ", fileCounter, " files")

