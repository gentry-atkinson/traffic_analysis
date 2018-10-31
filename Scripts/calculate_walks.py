#!/usr/bin/env python3

import json
import itertools


def timeInGraph(item):
    #print ("timeInGraph called for ", item)
    for key in graph.keys():
        if (item == key):
            return True
    return False


def locInTime(item, time):
    for key in graph[time].keys():
        if(item == key):
            return True
    return False


def powerset(iterable):
    #print (iterable)
    #"powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    #print (s)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))


def findWalk(devices, time, sLocation, cLocation, length, outfile, graph):
    #print(devices, " sent to findWalk for ", cLocation)
    investigate = True
    try:
        nextNodes = graph[time][cLocation]["adjList"]
    except:
        #print ("No next node")
        investigate = False
    if (investigate):
        try:
            for node in nextNodes:
                nextTime = node.split('/', 2)[0]
                nextLoc = node.split('/', 2)[1]
                #print ("Checking walk from ", cLocation, " to ", nextLoc, " at ", nextTime)
                if (compareList(devices, graph[nextTime][nextLoc]["devices"])):
                    length += 1
                    findWalk(devices, nextTime, sLocation, nextLoc, length, outFile, graph)
        except:
            print ("Could not check walk for ... some reason")
    try:
        if (length > 0):
            #print ("***Walk found over ", length, " nodes.************")
            outString = ""
            outString = outString +"{\"Num_Devices\" : \"" + str(len(devices)) + "\", "
            outString = outString + "\"Walk_Length\" : \"" + str(length) + "\", "
            outString = outString + "\"Origin\" : \"" + sLocation + "\", "
            outString = outString + "\"Destination\" : \"" + cLocation + "\"}\n"
            outFile.write((outString))
    except:
        outFile.write("Couldnt write walk to file\n")


def compareList (list1, list2):
    #print ("comparing ", list1, " to ", list2)
    return set(list1) == set(list2)
    return False


inFile = open('/media/gentry/DATA/cs7311/data_sets/split_traffic_files/ITMF_2017-03-11')

counter = 0
graph = {}
sTime = ""
eTime = ""
timeCounter = 0
nodeCounter = 0
highestOrderNode = 0
oNode = ""
dNode = ""
oLocation = ""
dLocation = ""
allTimes = list()
walkCounter = 0

line = inFile.readline()


while(inFile):
    #print ("processing number ", counter + 1)
    line = inFile.readline()
    try:
        item = json.loads(line)

        sTime = item["Start Time"]
        sTime = sTime.split('T', 2)[1]
        sTime = sTime.split('-', 2)[0]
        sTime = sTime.split(':', 3)[0] + ':' + sTime.split(':', 3)[1]

        eTime = item["End Time"]
        eTime = eTime.split('T', 2)[1]
        eTime = eTime.split('-', 2)[0]
        eTime = eTime.split(':', 3)[0] + ':' + eTime.split(':', 3)[1]

        counter += 1
        if (not timeInGraph(sTime)):
            #print ("New Time ", sTime)
            graph[sTime] = dict()
            timeCounter += 1
            allTimes.append(sTime)

        counter += 1
        if (not timeInGraph(eTime)):
            #print ("New Time ", eTime)
            graph[eTime] = dict()
            timeCounter += 1
            allTimes.append(eTime)

        oLocation = item["Origin Reader Identifier"]

        if (not locInTime(oLocation, sTime)):
            #print ("New Location ", location)
            graph[sTime][oLocation] = {}
            graph[sTime][oLocation]["device_count"] = 0
            graph[sTime][oLocation]["speed"] = 0
            graph[sTime][oLocation]["devices"] = list()
            nodeCounter += 1
            graph[sTime][oLocation]["adjList"] = list()

        #print("Updating Node")
        graph[sTime][oLocation]["device_count"] += 1
        if (graph[sTime][oLocation]["device_count"] > highestOrderNode):
            highestOrderNode = graph[sTime][oLocation]["device_count"]
        increment = float(item["Speed (Miles Per Hour)"])
        increment -= graph[sTime][oLocation]["speed"]
        increment /= graph[sTime][oLocation]["device_count"]
        graph[sTime][oLocation]["speed"] += increment
        graph[sTime][oLocation]["devices"].append(item["Device Address"])
        #print ("Devices at this location and time: ", graph[time][location]["device_count"])

        dLocation = item["Destination Reader Identifier"]

        if (not locInTime(dLocation, eTime)):
            #print ("New Location ", location)
            graph[eTime][dLocation] = {}
            graph[eTime][dLocation]["device_count"] = 0
            graph[eTime][dLocation]["speed"] = 0
            graph[eTime][dLocation]["devices"] = list()
            nodeCounter += 1
            try:
                dNode = eTime + "/" + dLocation
                #oNode = sTime + "/" + oLocation
                graph[sTime][oLocation]["adjList"].append(dNode)
            except:
                print ("Cant add ", dNode, " to oNode")

        #print("Updating Node")
        graph[eTime][dLocation]["device_count"] += 1
        if (graph[eTime][dLocation]["device_count"] > highestOrderNode):
            highestOrderNode = graph[eTime][dLocation]["device_count"]
        increment = float(item["Speed (Miles Per Hour)"])
        increment -= graph[eTime][dLocation]["speed"]
        increment /= graph[eTime][dLocation]["device_count"]
        graph[eTime][dLocation]["speed"] += increment
        graph[eTime][dLocation]["devices"].append(item["Device Address"])
        #print ("Devices at this location and time: ", graph[time][location]["device_count"])
    except:
        print ("Halted graph making with sTime: ", sTime, " eTime: ", eTime)
        break

outFile = open("walks_over_Austin.json", 'a+')

try:
    #print (len(allTimes), " times to check")

    for time in allTimes:
        #print (len(graph[time].keys()), " locations to check")
        for loc in graph[time].keys():
            #print ("Check ", loc, " at ", time)
            deviceList = powerset(graph[time][loc]["devices"])
            #print (deviceList)
            #print (len(deviceList), " devices to check")
            for devices in deviceList:
                #print (devices)
                if (devices):
                    walkCounter += 1
                    #print ("Checking walk number ", walkCounter)
                    findWalk(devices, time, loc, loc, 0, outFile, graph)
                    #print ("Finished checking walk number ", walkCounter)

except:
    print ("Halted in walk taking")

print (counter, " items processed")
print (nodeCounter, " nodes created in ", timeCounter, " times", )
print ("Highest order node: ", highestOrderNode)
print (walkCounter, " possible walks investigated.")


