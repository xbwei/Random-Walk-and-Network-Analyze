'''
Created on Sep 23, 2013
@author: Xuebin Wei
weixuebin@gmail.com
Dept of GGY, UGA

Change the weight of network
'''

# import Graphy
import arcpy
# from arcpy import env
#import pickle
import cPickle as pickle
# import random
import sys
# import traceback

Netfile = arcpy.GetParameterAsText(0)
# load the network class file
ChangeType = arcpy.GetParameterAsText(1)
 
NetworkLayer = arcpy.GetParameterAsText(2)
# get the shp file layer
WeightField =  arcpy.GetParameterAsText(3)
# weight field of shp file
OutputFoder =  arcpy.GetParameterAsText(4)
# folder of new network class
NewNetworkName = arcpy.GetParameterAsText(5)
# name of weight changed network
NetField = arcpy.GetParameterAsText(6)

# '''
# Debug only
# '''
# Netfile = r"D:\project\UGA\Research\randomwalking\RandomWalkingPy\data\Network\ManhattanStreetsNetwork.net"
# # load the network class file
# ChangeType = r"network"
# 
# NetworkLayer = ""
# # get the shp file layer
# WeightField =  ""
# # weight field of shp file
# OutputFoder =  r"D:\project\UGA\Research\randomwalking\RandomWalkingPy\data\Network"
# # folder of new network class
# NewNetworkName = r"ManhattanConnect"
# # name of weight changed network
# NetField = r"connect"

unpicklefile = open(Netfile, 'rb')
Net = pickle.load(unpicklefile)

def ChangeWeightFromShp(net,networklayer,weightfield):
    '''
    Change the weight of edges from shapefile attribute
    '''
    rows = arcpy.SearchCursor(NetworkLayer)
    rowcount = arcpy.GetCount_management(networklayer)
    arcpy.SetProgressor("step","Start reading rows ",0,int(rowcount.getOutput(0)), 1) 
    for row in rows:
        arcpy.SetProgressorLabel("Changing the Edge with FID of " + str(row.getValue("FID")) + " ...") 
        for l in net.EdgeList:
            if l.ID == int(row.getValue("FID")):
                l.weight = int(row.getValue(weightfield))
        arcpy.SetProgressorPosition()
    return net

def ChangeWeightFromGrapy(net,netfield):
    '''
    Change the weight of edge to number of connection
    '''
    arcpy.SetProgressor("step","Start reading rows ",0,int(len(net.EdgeList)), 1) 
    for l in net.EdgeList:
        arcpy.SetProgressorLabel("Changing the Edge with FID of " + str(l.ID) + " ...")
        if netfield=="connect":
            l.weight=l.connect
        elif netfield=="length":
            l.weight=l.length
        else:
            arcpy.AddError("Invalid command.")
                
        arcpy.SetProgressorPosition()
    return net
                
if ChangeType=="shapefile":
    NewNet = ChangeWeightFromShp(Net,NetworkLayer,WeightField)
if ChangeType =="network":
    NewNet = ChangeWeightFromGrapy(Net,NetField)
    
'''
Updating nodes and edges in network
'''
    
for node in Net.NodeList:
    for l in node.EdgeList:
        for edge in Net.EdgeList:
            if l.ID == edge.ID:
                l=edge
for edge in Net.EdgeList:
    for n in Net.NodeList:
        if edge.FirstPoint.ID == n.ID:
            edge.FirstPoint = n
        if edge.LastPoint.ID == n.ID:
            edge.LastPoint = n

'''
Write the new network class to another file
'''
                
OutPutFiel = open(OutputFoder+"\\"+NewNetworkName+".net","wb")
## Export the graph to a file
sys.setrecursionlimit(1000000)
## enlarge the cursive limit
pickle.dump(NewNet,OutPutFiel,2)
## dump the class into binary
OutPutFiel.close()
arcpy.AddMessage("The graph of "+str(NewNetworkName)+".net has been constructed in "+str(OutputFoder))  