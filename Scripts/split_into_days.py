#!/usr/bin/env python

import json
import os

inFile = open("/media/gentry/My Drive/cs7311/Individual_Traffic_Match_Files__ITMF_.json", 'r')

try:
    os.system('mkdir /media/gentry/DATA/cs7311/data_sets/split_traffic_files')
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
            filename = "/media/gentry/DATA/cs7311/data_sets/split_traffic_files/ITMF_" + date
            outFile = open(filename, 'a+')
            #outFile.write("New file")
            item = json.dumps(item)
            outFile.write(item)
            outFile.write('\n')
            fileCounter += 1
        else:
            item = json.dumps(item)
            outFile.write(item)
            outFile.write('\n')
        counter += 1
    except:
        print ("error in converter loop")
        break

print(counter, " entries written into ", fileCounter, " files")

