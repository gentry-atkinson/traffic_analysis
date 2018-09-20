#!/usr/bin/env python3

import json

incidentFile = open("/media/gentry/My Drive/cs7311/Real-Time_Traffic_Incident_Reports.json", 'rt')
incidentData = []

sensorFile = open("/media/gentry/My Drive/cs7311/Travel_Sensors.json", 'rt')
sensorData = []

agroFile = open("closest_sensors.json", 'wt')

item = {}


def howClose(lon1, lat1, lon2, lat2):
    try:
        lonDiff = float(lon1) * 55 - float(lon2) * 55
        latDiff = float(lat1) * 55 - float(lat2) * 55
        return (lonDiff * lonDiff) + (latDiff * latDiff)
    except:
        #print("Your data is crap")
        return 999999999

print("Loading Incident Data")

incidentFile.readline()


while (incidentFile):
    line = incidentFile.readline()
    try:
        item = json.loads(line)
        incidentData.append(item)
    except:
        break

print("Loading Sensor Data ")

sensorFile.readline()

while (sensorFile):
    line = sensorFile.readline()
    try:
        item = json.loads(line)
        sensorData.append(item)
    except:
        break

print("Printing Incident Locations")

#for entry in incidentData:
#    print(entry["Location"])

print("Printing Sensor Locations")

#for entry in sensorData:
#    print(entry["Location"])

print("Finding Closest Sensors")

x = 0

for incidentEntry in incidentData:
    closestDist = 999999999
    closestSensor = {}
    for sensorEntry in sensorData:
        if (sensorEntry["READER_ID"] == ""):
            continue
        thisDist = howClose(incidentEntry["Longitude"], incidentEntry["Latitude"], sensorEntry["LOCATION_LONGITUDE"], sensorEntry["LOCATION_LATITUDE"])
        if (thisDist < closestDist):
            closestSensor = sensorEntry
            closestDist = thisDist
    if (closestSensor != {}):
        if (closestSensor["READER_ID"] == ""):
            print(closestSensor)
            print("\n")
            print("\n")
        newLine = "{\"Incident ID\" : \""
        newLine += incidentEntry["Traffic Report ID"]
        newLine += "\", \"Reader ID\" : \""
        newLine += closestSensor["READER_ID"]
        newLine += "\", \"Distance\" : \""
        newLine += str(closestDist)
        newLine += "\"}"

        agroFile.write(newLine)
        agroFile.write("\n")
        x += 1
print(x)


incidentFile.close()
sensorFile.close()