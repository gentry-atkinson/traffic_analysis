#!/usr/bin/env python3

import json



def timeInGraph(item):
    for key in graph.keys():
        if (item == key):
            return True
    return False

def locInTime(item, time):
    for key in graph[time].keys():
        if(item == key):
            return True
    return False

inFile = open('/media/gentry/DATA/cs7311/data_sets/split_traffic_files/ITMF_2015-12-31')

counter = 0
graph = {}
time = ""
timeCounter = 0
nodeCounter = 0

line = inFile.readline()


while(inFile):
    #print ("processing number ", counter + 1)
    line = inFile.readline()
    try:
        item = json.loads(line)
        time = item["Start Time"]
        #print (time)
        time = time.split('T', 2)[1]
        time = time.split('-', 2)[0]
        time = time.split(':', 3)[0] + ':' + time.split(':', 3)[1]
        #print (time)

        counter += 1
        if (not timeInGraph(time)):
            print ("New Time ", time)
            graph[time] = {}
            timeCounter += 1

        location = item["Origin Reader Identifier"]
        #print (location)

        if (not locInTime(location, time)):
            print ("New Location ", location)
            graph[time][location] = {}
            graph[time][location]["device_count"] = 0
            graph[time][location]["speed"] = 0
            graph[time][location]["devices"] = list()
            nodeCounter += 1

        #print("Updating Node")
        graph[time][location]["device_count"] += 1
        increment = float(item["Speed (Miles Per Hour)"])
        increment -= graph[time][location]["speed"]
        increment /= graph[time][location]["device_count"]
        graph[time][location]["speed"] += increment
        graph[time][location]["devices"].append(item["Device Address"])
        print ("Devices at this location and time: ", graph[time][location]["device_count"])

        location = item["Destination Reader Identifier"]
        #print (location)

        if (not locInTime(location, time)):
            print ("New Location ", location)
            graph[time][location] = {}
            graph[time][location]["device_count"] = 0
            graph[time][location]["speed"] = 0
            graph[time][location]["devices"] = list()
            nodeCounter += 1

        #print("Updating Node")
        graph[time][location]["device_count"] += 1
        increment = float(item["Speed (Miles Per Hour)"])
        increment -= graph[time][location]["speed"]
        increment /= graph[time][location]["device_count"]
        graph[time][location]["speed"] += increment
        graph[time][location]["devices"].append(item["Device Address"])
        print ("Devices at this location and time: ", graph[time][location]["device_count"])
    except:
        break

print (counter, " items processed")
print (nodeCounter, " nodes created in ", timeCounter, " times")

