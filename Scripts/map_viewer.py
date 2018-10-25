#!/usr/bin/env python


# import gmplot package
import gmplot
import json

latitude_list = []
longitude_list = []
sensor_list = {}

sensorFile = open("Travel_Sensors.json")
tripFile = open("Traffic_Match_Summary_Records__TMSR_Test_Data.json")

line = sensorFile.readline()

count = 0
lamarCount = 0
riverCount = 0
readerID = ""

while (sensorFile):
    line = sensorFile.readline()
    try:
        item = json.loads(line)
        #print("long: ", item["LOCATION_LONGITUDE"])
        readerID = item["READER_ID"]
        if (readerID.find("lamar") != -1):
            lamarCount += 1
        if (readerID.find("riverside") != -1):
            riverCount += 1
        sensor_list[item["READER_ID"]] = {}
        sensor_list[item["READER_ID"]]["latitude"] = float(item["LOCATION_LATITUDE"])
        sensor_list[item["READER_ID"]]["longitude"] = float(item["LOCATION_LONGITUDE"])
        latitude_list.append(float(item["LOCATION_LATITUDE"]))
        longitude_list.append(float(item["LOCATION_LONGITUDE"]))
        count += 1
    except:
        break

print (count, " sensors in list")
print (lamarCount, " sensors on Lamar")
print (riverCount, " sensors on Riverside")


# GoogleMapPlotter return Map object
# Pass the center latitude and
# center longitude
gmap1 = gmplot.GoogleMapPlotter(30.2525959, -97.7374269, 11 )

gmap1.scatter( latitude_list, longitude_list, 'purple', size = 120, marker = False )
#gmap1.marker(latitude_list, longitude_list, 'purple')

line = tripFile.readline()

count = 0

while (tripFile):
    plotLat = []
    plotLong = []
    line = tripFile.readline()
    count += 1
    try:
        item = json.loads(line)
        #print ("Plotting ", item["origin_reader_identifier"], " to ", item["destination_reader_identifier"])
        #print ("Origin Lat: ", sensor_list[item["origin_reader_identifier"]]["latitude"])
        #print ("Origin Long: ", sensor_list[item["origin_reader_identifier"]]["longitude"])
        #print ("Dest Lat: ", sensor_list[item["destination_reader_identifier"]]["latitude"])
        #print ("Dest Long: ", sensor_list[item["destination_reader_identifier"]]["longitude"])

        lat = float(sensor_list[item["origin_reader_identifier"]]["latitude"])
        lon = float(sensor_list[item["origin_reader_identifier"]]["longitude"])

        plotLat.append(lat)
        plotLong.append(lon)

        #print ("Origin added to plot list")

        lat = float(sensor_list[item["destination_reader_identifier"]]["latitude"])
        lon = float(sensor_list[item["destination_reader_identifier"]]["longitude"])

        plotLat.append(lat)
        plotLong.append(lon)

        #print ("Lats", plotLat)
        #print ("Longs", plotLong)

        gmap1.plot(plotLat, plotLong, 'cornflowerblue', edge_width=3)
    except EOFError:
        print ("I reached the end")
        break
    except:
        if (item["record_id"] == "1484085600mlk_ih35mlk_red_river"):
            break
        tripFile.readline()
        count -= 1
        continue

print ("Total trips plotted: ", count)


#gmap1.plot(latitude_list, longitude_list, 'cornflowerblue', edge_width = 2.5)

# Pass the absolute path
gmap1.draw( "/home/gentry/Desktop/map11.html" )

#https://medium.com/@stevenvandorpe/gmplot-in-jupyter-installation-guide-and-package-exploration-338756e8f26

