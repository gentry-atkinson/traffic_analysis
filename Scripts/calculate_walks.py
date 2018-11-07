#!/usr/bin/env python3

import json
import itertools
import sys


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


def findWalk(devices, sTime, sLocation, cTime, cLocation, length, outfile, date):
    #print(devices, " sent to findWalk for ", cLocation)
    investigate = True
    try:
        nextNodes = graph[cTime][cLocation]["adjList"]
    except:
        #print ("No next node")
        investigate = False
    if (investigate):
        try:
            for node in nextNodes:
                nextTime = node.split('/', 2)[0]
                if (cTime == nextTime):
                    return
                nextLoc = node.split('/', 2)[1]
                #print ("Checking walk from ", cLocation, " to ", nextLoc, " at ", nextTime)
                if (compareList(devices, graph[nextTime][nextLoc]["devices"])):
                    length += 1
                    findWalk(devices, sTime, sLocation, nextTime, nextLoc, length, outFile, date)
        except:
            print ("Could not check walk becasue ", sys.exc_info()[0])
    try:
        if (length > 0):
            #print ("***Walk found over ", length, " nodes.************")
            outString = ""
            outString = outString +"{\"Num_Devices\" : \"" + str(len(devices)) + "\", "
            outString = outString + "\"Walk_Length\" : \"" + str(length) + "\", "
            outString = outString + "\"Date\" : \"" + str(date) + "\", "
            outString = outString + "\"Start Time\" : \"" + str(sTime) + "\", "
            outString = outString + "\"End Time\" : \"" + str(cTime) + "\", "
            outString = outString + "\"Origin\" : \"" + str(sLocation) + "\", "
            outString = outString + "\"Destination\" : \"" + str(cLocation)  + "\", "
            outString = outString + "\"Speed at Origin\" : \"" + str(graph[sTime][sLocation]["speed"]) + "\", "
            outString = outString + "\"Speed at Destination\" : \"" + str(graph[cTime][cLocation]["speed"])+ "\"}\n"
            outFile.write((outString))
    except:
        outFile.write("Couldnt write walk to file\n")


def compareList (list1, list2):
    #print ("comparing ", list1, " to ", list2)
    return set(list1).issubset(set(list2))

fileFile = open('files.txt')
outFile = open("/media/gentry/DATA/cs7311/data_sets/walks_over_Austin.json", 'a+')

while(fileFile):
    fileName = fileFile.readline()
    fileName = fileName[:-1]
    #fileName = "ITMF_2016-01-20"
    inFile = open('/media/gentry/DATA/cs7311/data_sets/split_traffic_files/' + fileName)

    print("******************************")
    print("Processing: ", fileName)

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
    date = ""
    latestTime = ""

    line = inFile.readline()


    while(inFile):
        #print ("processing number ", counter + 1)
        line = inFile.readline()
        try:
            item = json.loads(line)

            sTime = item["Start Time"]
            if (date == ""):
                date = sTime.split('T', 2)[0]
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
                    oNode = sTime + "/" + oLocation
                    if (oNode != dNode):
                        graph[sTime][oLocation]["adjList"].append(dNode)
                except:
                    #print ("Cant add ", dNode, " to oNode")
                    dNode = ""

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

    try:
        #print (len(allTimes), " times to check")

        for time in allTimes:
            #print (len(graph[time].keys()), " locations to check")
            latestTime = time
            for loc in graph[time].keys():
                #print ("Check ", loc, " at ", time)
                if (len(graph[time][loc]["devices"]) > 25):
                    raise Exception("Device list too long")
                deviceList = powerset(graph[time][loc]["devices"])
                #print (deviceList)
                #print (len(deviceList), " devices to check")
                for devices in deviceList:
                    #print (devices)
                    if (len(devices) > 0):
                        walkCounter += 1
                        #print ("Checking walk number ", walkCounter)
                        findWalk(devices, time, loc, time, loc, 0, outFile, date)
                        #print ("Finished checking walk number ", walkCounter)
                        #if (walkCounter % 1000000 == 0):
                            #print (walkCounter)

    except:
        print ("Halted in walk taking")

    inFile.close()

    print (counter, " items processed")
    print (nodeCounter, " nodes created in ", timeCounter, " times", )
    print ("Highest order node: ", highestOrderNode)
    print (walkCounter, " possible walks investigated.")
    print ("Last check started at ", latestTime)

print("All done")


