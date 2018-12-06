#!/usr/bin/env python

import numpy
from freediscovery.cluster import Birch, birch_hierarchy_wrapper
import json
import os

fileFile = open("walks_fileNames.txt", 'r')
inFileName = "/media/gentry/DATA/cs7311/data_sets/walks/"
street = "red_river"

thisFileName = inFileName + fileFile.readline()
thisFileName = thisFileName[:-1]
inFile = open(thisFileName, 'r')

line = inFile.readline()
item = json.loads(line)

fileCounter = 0
walkCounter = 0

X = numpy.array([int(item["Num_Devices"]), int(item["Walk_Length"]), float(item["Speed at Origin"]), float(item["Speed at Destination"])])

while(fileFile):
    try:
        thisFileName = inFileName + fileFile.readline()
        thisFileName = thisFileName[:-1]
        inFile = open(thisFileName, 'r')
        fileCounter += 1
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
        if (street in origin and street in destination):
            walkCounter += 1
            if (int(item["Num_Devices"]) > 1 and int(item["Walk_Length"]) > 1):

                item_array = numpy.array([int(item["Num_Devices"]), int(item["Walk_Length"]), float(item["Speed at Origin"]), float(item["Speed at Destination"])])
                X = numpy.vstack((X, item_array))

    print ("File ", fileCounter, " processed.")

cluster_model = Birch(threshold=0.1, branching_factor=20, compute_sample_indices=True, n_clusters=3)

cluster_model.fit(X)

htree, _ = birch_hierarchy_wrapper(cluster_model)
print("******************Wals on ", street, "***************\n\n")
print("Total number of walks on ", street, ": ", walkCounter)
print('Total number of subclusters:', htree.tree_size)

htree.display_tree()

os.system('spd-say "All done"')

