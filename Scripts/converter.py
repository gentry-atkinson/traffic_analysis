#!/usr/bin/env python

import csv
import json

csvfile = open('Traffic_Match_Summary_Records__TMSR_.csv', 'r')
jsonfile = open('Traffic_Match_Summary_Records__TMSR_.json', 'w')

fieldnames = ("record_id","origin_reader_identifier", "destination_reader_identifier", "origin_roadway", "origin_cross_street", "origin_direction", "destination_roadway", "destination_cross_street", "destination_direction", "segment_length_miles", "timestamp", "average_travel_time_seconds", "average_speed_mph", "summary_interval_minutes", "number_samples", "standard_deviation")
reader = csv.DictReader(csvfile, fieldnames)
#x = 0
for row in reader:
    json.dump(row, jsonfile)
    jsonfile.write('\n')
    #if x == 1000:
        #break
    #x = x + 1