import gpxParse
import gpxpy
from array import *
import json
from datetime import datetime
import time

class GpxRecord:

    def __init__(self, user):
        print('object created')
        self.user = user
        self.pointsArray = []
        self.elevationArray = []
        self.hrArray = []
        self.serializedPointsArray = []
        self.serializedHrArray = []
        self.serializedElevationArray = []
        self.distance = None
        self.rideDate = None
        self.rideTime = None
        self.avgSpeed = None
        self.avgHr = 0.0



    def parseFile(self,filePath):
        print('DEBUG:' + filePath)
        gpx_file = open(filePath, 'r')
        gpx_parsed_file = gpxpy.parse(gpx_file)
        i = 0
        for track in gpx_parsed_file.tracks:
            for segment in track.segments:
                for point in segment.points:
                    if i == 0:
                        startTime=point.time
                    if segment.points[-1]:
                        endTime = point.time
                    self.pointsArray.append([])
                    self.pointsArray[-1].append(point.latitude)
                    self.pointsArray[-1].append(point.longitude)
                    self.elevationArray.append(float(point.elevation)/100)
                    self.hrArray.append(float(point.description))
                    i = i+1
        #DEBUG:
        # print(len(self.pointsArray))
        # print(len(self.elevationArray))
        # print(self.pointsArray[60])
        # print(self.hrArray[33])

        self.distance = (gpx_parsed_file.length_2d() / 1000)
        print(self.distance)

        self.serializedPointsArray = json.dumps(self.pointsArray)
        self.serializedHrArray = json.dumps(self.hrArray)
        self.serializedElevationArray = json.dumps(self.elevationArray)

        self.rideDate = startTime
        time_delta = (endTime - startTime)
        total_seconds = time_delta.total_seconds()
        self.rideTime = time.strftime('%H:%M:%S', time.gmtime(total_seconds))

        self.avgSpeed = ((self.distance)/total_seconds)*3600

        hrSum = sum(self.hrArray)
        hrLen = len(self.hrArray)
        self.avgHr = hrSum/hrLen
        print(self.elevationArray)





