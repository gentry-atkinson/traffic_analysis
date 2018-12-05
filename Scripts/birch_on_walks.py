#!/usr/bin/env python

import numpy
from freediscovery.cluster import Birch, birch_hierarchy_wrapper
import json
import os

fileFile = open("walks_fileNames.txt", 'r')
inFileName = "/home/user/Desktop/cs7311_data/walks/"

thisFileName = inFileName + fileFile.readline()
thisFileName = thisFileName[:-1]
inFile = open(thisFileName, 'r')

line = inFile.readline()
item = json.loads(line)

counter = 1
X = numpy.array([int(item["Num_Devices"]), int(item["Walk_Length"]), float(item["Speed at Origin"]), float(item["Speed at Destination"])])

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

        item_array = numpy.array([int(item["Num_Devices"]), int(item["Walk_Length"]), float(item["Speed at Origin"]), float(item["Speed at Destination"])])
        X = numpy.vstack((X, item_array))
    print ("File ", counter, " processed.")

cluster_model = Birch(threshold=0.1, branching_factor=20, compute_sample_indices=True, n_clusters=3)

cluster_model.fit(X)

htree, _ = birch_hierarchy_wrapper(cluster_model)
print('Total number of subclusters:', htree.tree_size)

htree.display_tree()

os.system('spd-say "All done"')

