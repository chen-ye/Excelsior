from numpy import *
from xml.dom import minidom
import pandas as pd
import numpy.core
import csv
import os

#Setup + Class Definitions
#frameArray = array([], dtype=[('Rack', numpy.int32), ('Rep', numpy.int32), ('Frame', numpy.ndraray)])
frameArray = []
metadataMap = {}

global spaceUnits
global frameInterval
global timeUnits

class Track:
    def __init__(self, id, spots):
        self.id = id
        self.spots = numpy.core.records.fromarrays(array(spots).transpose(), names = 't, x, y') # Assigns spots data structure to track
        #self.meanDC
        #self.metadata

    def calculate(self):
        self.meanX = average(self.spots['x'])
        self.meanDY = average(diff(self.spots['y']))
        #print('Calculated Mean X of ' + str(self.meanX) + ' and Mean Y Velocity of ' + str(self.meanDY))

    def __str__( self ):
        return str('ID: ' + str(self.id) + ' Mean X:' + str(self.meanX) + ' Mean Y Velocity: ' + str(self.meanDY) + 'Spots: ' + str(self.spots))

class Metadata:
    def __init__(self, age, nucleotype, mitotype, diet, replicate, repetition, recordDateTime):
        self.age = age
        self.nucleotype = nucleotype
        self.mitotype = mitotype
        self.diet = diet
        self.replicate = replicate
        self.repetition = repetition
        self.recordDateTime = recordDateTime

def filterXML(filename):
    if filename.startswith('Tracked_Batch_Preprocessed') and filename.endswith('.xml'):
        return True
    else:
        return False

def findXML(path, age):
    print('Recursively finding xmls in ' + path)
    for dirpath, dirs, files in os.walk(path):
        print('In directory ' + dirpath)
        for xml in filter(filterXML,files):
            print('Found xml: ' + xml + '.  Processing...')
            importXML(dirpath, xml, age)
    print('Completed!')

def importXML(dirpath, filename, age):
    trackArray = []
    xml = minidom.parse(dirpath + '/' + filename)
    #Extract the rack and repetition numbers
    fileMeta = filename.split('_')
    rack = int(fileMeta[4].replace('Rack',''))
    rep = int(fileMeta[5].replace('Rep',''))
    id = 0
    metadata = xml.getElementsByTagName('Tracks')[0]
    spaceUnits = metadata.attributes['spaceUnits'].value
    frameInterval = float(metadata.attributes['frameInterval'].value)
    timeUnits = metadata.attributes['timeUnits'].value
    #Get all tracks
    for track in xml.getElementsByTagName('particle'):
        #print('Importing Track ' + str(id) + ' from ' + filename)
        spotList = []
        #Get all spots within a track        
        for spot in track.getElementsByTagName('detection'):
            spotList.append((int(spot.attributes['t'].value), float(spot.attributes['x'].value), float(spot.attributes['y'].value)))
        trackStruct = Track(id, spotList)
        trackArray.append(trackStruct)
        trackStruct.calculate()
        id += 1
    print(str(id) + ' tracks imported from ' + filename)
    frameArray.append((age, rack, rep, trackArray))

def importMetadataCSV(path):
    #Imports a csv that maps Age, Rack, Bin to Nucleotype('Nuclear'), Mitotype('Mito'), Diet, Replicate.  As such, it must contain those columns
    metaArray = genfromtxt(path, delimiter=',', dtype=None, names=True)
    for entry in metaArray:
        for repetition in range (1,3):
            metadataMap[(entry['age'],entry['Rack'],entry['Bin'],repetition)] = Metadata(entry['age'],entry['Nuclear'],entry['Mito'],entry['Diet'],entry['Replicate'],repetition,'Null')

def bin(age, rack, rep, trackArray):
    meanXArray = [track.meanX for track in trackArray]
    min = min(meanXArray)
    max = max(meanXArray)
    range = max - min
    bins = 6
    interval = range / bins
    
    for track in trackArray:
        bin = int(math.ceil((track.meanX - min) / interval))
        metadata = metadataMap[(age,rack,rep,bin)]
        track.metadata = metadata

def exportToPandas(frameArray):
    pandasNumArray = []
    for frame in frameArray:
        age = frame[0]
        rep = frame[2]
        trackArray = frame[3]
        metadata = trackArray.metadata

        bin(age,frame[1],rep,trackArray)
        pandasNumArray.append((age,rack,rep,metadata.replicate,0,metadata.nucleotype,metadata.mitotype,metadata.diet,trackArray.meanDY))
    dataframe = pd.DataFrame(array(pandasNumArray),index=None,columns=['Age','Rack','Repetition','Replicate','Tube','Nucleotype','Mitotype','Diet','Mean Vertical Velocity'])
    return dataframe

#Read XMLs from disk into memory
findXML('D:\Chen Ye\Documents\GitHub\Excelsior\HHMI_tracked_files\young_flies_csv', 'young')
findXML('D:\Chen Ye\Documents\GitHub\Excelsior\HHMI_tracked_files\young_flies_csv', 'old')
#importMetadataCSV(path)
dataframe = exportToPandas(frameArray)