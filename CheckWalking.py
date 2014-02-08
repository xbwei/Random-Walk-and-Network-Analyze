'''
Created on Sep 24, 2013
@author: Xuebin Wei
weixuebin@gmail.com
Dept of GGY, UGA

Checking the walking result
'''
import arcpy
#import pickle
import cPickle as pickle
import random

#Wlkfile = r'C:\UGA\Paper\randomwalking\RandomWalkingPy\data\result\nwppath.wlk'
#Netfile = r'C:\UGA\Paper\randomwalking\RandomWalkingPy\data\net\newsimple.net'
#Netfile = r'C:\UGA\Paper\randomwalking\RandomWalkingPy\data\net\randometest.net'

random.seed()


Wlkfile = arcpy.GetParameterAsText(0)
SelectNumber = arcpy.GetParameterAsText(1)
GenerateFeature = arcpy.GetParameterAsText(2)
NodeLayer = arcpy.GetParameterAsText(3)
EdgeLayer = arcpy.GetParameterAsText(4)
OutputFolder = arcpy.GetParameterAsText(5)
# set the number of walking path want to check
unpicklefile = open(Wlkfile, 'rb')
Walks = pickle.load(unpicklefile)


def GeneratePath(pathelement,mubmer,elementtype,layer,folder):
    '''
    Select the points or edges in this path as a single shpfile
    '''
    ini = True
  
    for p in pathelement:
        if ini:
            sqlsentence = "FID =" + str(p)
            ini = False
        else:
            sqlsentence = sqlsentence +" OR FID = "+ str(p)
    selectname = "RandomWalking"+str(elementtype)+str(mubmer)+".shp"
    arcpy.Select_analysis(layer, folder+"\\"+selectname, sqlsentence)


arcpy.SetProgressor("step", "Loading Random Walking...", 0,int(SelectNumber), 1) 
arcpy.AddMessage("Total walking time is "+str(Walks.i))
arcpy.AddMessage("Null walking time is "+str(Walks.countnullloop))
arcpy.AddMessage("Final loop value is "+str(Walks.loopvalue))
arcpy.AddMessage("Final total random walking value is "+str(Walks.totalrvalue))

for n in range (0,int(SelectNumber)):
    walk = random.choice(Walks.walks)
    arcpy.SetProgressorLabel("Current walking is " + str(walk.number) + "...") 
    arcpy.AddMessage("\t ------")
    arcpy.AddMessage("\t The index of this walking is: "+str(walk.number))
    arcpy.AddMessage("\t The total length of this walking is: "+str(walk.walklength)) 
    arcpy.AddMessage("\t The length permit of this walking is: "+str(walk.lenthpermit))
    arcpy.AddMessage("\t The points in this walking are: "+str(walk.points))
    arcpy.AddMessage("\t The edges in this walking are: "+str(walk.edges))
    if GenerateFeature:
        GeneratePath(walk.points,walk.number,"Points",NodeLayer,OutputFolder)
        GeneratePath(walk.edges,walk.number,"Edges",EdgeLayer,OutputFolder)
    arcpy.SetProgressorPosition()

arcpy.ResetProgressor()
    
    
    
    
