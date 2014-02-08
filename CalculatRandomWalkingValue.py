'''
Created on Sep 13, 2013

@author: Xuebin Wei
weixuebin@gmail.com
Dept of GGY, UGA

Calculate the random walking value of a given network
'''

import Graphy
import arcpy
from arcpy import env
#import pickle
import cPickle as pickle
import random
import sys
import traceback
import math

# '''
# Debug parameters
# '''
# 
# Netfile = r'D:\project\UGA\Research\randomwalking\RandomWalkingPy\data\Network\Clayton.net'
# OutputFolder = r'D:\project\UGA\Research\randomwalking\RandomWalkingPy\data\WalkingResult\Atlanta\CityCenter\Clayton'
# # PointTable = "NaturePwrPoint"
# # LinkTable = "NaturePwrLink"
# # WalkPathName = "NaturePwr"
# RField = "SpePwr"
# PPermit = "0.000001"
# SelectionType = "weight"
# # threshold of 
# # SimulateMethod = "Normal Distribution"
# SimulateMethod = "Power Law"
# MeanLength = "5000"
# # expected walking length
# StdLength = "1000"
# # stand deviation of walking length
# PointTable = RField+"_Point"
# LinkTable = RField+"_Link"
# WalkPathName = RField +"_Walk"
 
Netfile = arcpy.GetParameterAsText(0)
OutputFolder = arcpy.GetParameterAsText(1)
# PointTable = arcpy.GetParameterAsText(2)
# LinkTable = arcpy.GetParameterAsText(3)
# WalkPathName = arcpy.GetParameterAsText(4)
RField = arcpy.GetParameterAsText(2)
# field name of random walking
PointTable = RField+"_Point"
LinkTable = RField+"_Link"
WalkPathName = RField +"_Walk"
PPermit = arcpy.GetParameterAsText(3)
# threshold of walking length
SelectionType = arcpy.GetParameterAsText(4)
# select next link based on weight, connect or nature street
SimulateMethod = arcpy.GetParameterAsText(5)
MeanLength = arcpy.GetParameterAsText(6)
# expected walking length
StdLength = arcpy.GetParameterAsText(7)
# stand deviation of walking length

unpicklefile = open(Netfile, 'rb')
Net = pickle.load(unpicklefile)
alpha=2.5
# parameter for power-law simulation


#Net = pickle.Unpickler(unpicklefile).load()
#arcpy.AddMessage(len(Net.NodeList))
random.seed()

def Contain(checklist,element):
    '''
    Check whether list contains this element
    '''
    if element in checklist and element<>None:
        return True
    else:
        return False 

    
def GetPoint(net,pointnumber):
    '''
    Get the point based on point ID
    '''
    
    for p in net.NodeList:
        if p.ID == pointnumber:
            return p
            
def GetNextRandomLink(point,selecttype,lins):
    '''
    Random selection of next link based on weight, connect or nature street
    point: current point
    selecttype: next link selection type, based on weight, connect or nature street
    lins: the links in current walking
    '''
    try:    
        totalweight = 0
        # calculate the total weight of potential links
        linknumber = 0
        # index of potential links of current random point
        if selecttype == "weight":
            # select random walking link based on weight
            for pl in point.EdgeList:
                totalweight =totalweight + pl.weight
        
            # generate judge value for next link selection
            judgelinkvalue  = random.randint(0,totalweight)
            # the link with greater weight will more likely be selected
            while ((judgelinkvalue - point.EdgeList[linknumber].weight) >0):
                judgelinkvalue = judgelinkvalue - point.EdgeList[linknumber].weight
                linknumber = linknumber+1
            randomlink=point.EdgeList[linknumber]
        if selecttype == "connect":
            # select random walking link based on connect
            for pl in point.EdgeList:
                totalweight =totalweight + pl.connect
        
            # generate judge value for next link selection
            judgelinkvalue  = random.randint(0,totalweight)
            # the link with greater weight will more likely be selected
            while ((judgelinkvalue - point.EdgeList[linknumber].connect) >0):
                judgelinkvalue = judgelinkvalue - point.EdgeList[linknumber].connect
                linknumber = linknumber+1
            randomlink=point.EdgeList[linknumber]
        if selecttype == "nature street":
            
            '''
            Initialize nature weight
            If the link belongs to the same nature street as the previous link, it will get higher weight
            '''
            if len(lins)==0:
                # 1st link selection, no nature link preference
                for pl in point.EdgeList:
                    pl.Nweight = 1
            if len(lins)<>0:
                # set the nature street link twice weight than other links
                for pl in point.EdgeList:
                    if pl.NID==lins[len(lins)-1].NID:
                        pl.Nweight = 2
                    else:
                        pl.Nweight = 1
            '''
            Random select next link based nature weight
            '''            
            for pl in point.EdgeList:
                totalweight =totalweight + pl.Nweight
        
            # generate judge value for next link selection
            judgelinkvalue  = random.randint(0,totalweight)
            # the link with greater weight will more likely be selected
            while ((judgelinkvalue - point.EdgeList[linknumber].Nweight) >0):
                judgelinkvalue = judgelinkvalue - point.EdgeList[linknumber].Nweight
                linknumber = linknumber+1
            randomlink=point.EdgeList[linknumber]
            '''
            Set the nature weight of each link to 0
            '''
            for pl in point.EdgeList:
                pl.Nweight = 0            
        return randomlink
    except:
        # Get the trace back object
        #
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
    
        # Concatenate information together concerning the error into a message string
        #
        pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
        #
        arcpy.AddError(pymsg) 
        arcpy.AddError("PointID "+ str(point.ID))
        arcpy.AddError("RandomlinkID "+str(randomlink.ID)) 
        arcpy.AddError("link number "+str(linknumber)) 
        
def EndWalking(pntlist,pnIDlist,lnklist,lnIDlist,ttlen,lenpmt,nlcnt):
    '''
    Terminate the current walking
    '''
    pntlist = None
    pnIDlist= None
    lnklist = None
    lnIDlist = None
    ttlen = lenpmt + 1
    # to end current journal, set the current total length greater than current length permit
    nlcnt = nlcnt +1
    arcpy.AddWarning("\t Terminate current walking!") 
    return pntlist,pnIDlist,lnklist,lnIDlist,ttlen,nlcnt


def IncreaseRvalue(walkingpath):
    '''
    Increase the random walking of current walking path
    '''
    for g in walkingpath:
        g.rvalue = g.rvalue +1
    
def GetTotalRvalue():
    '''
    Get the total random walking value of current walking path
    '''
    totalrvalue = 0
    for g in Net.NodeList:
        if g.rvalue >=1:
            totalrvalue = totalrvalue + g.rvalue
    return totalrvalue

def GetTotalLength(lnklist):
    '''
    Get the total length of current walking
    '''
    totallength=0.0
    for l in lnklist:
        totallength = totallength + l.length
    return totallength

def GetConnectedElements(point):
    '''
    Get the connected points ID and edges of a selected point
    '''
    try:
        connectedlinks=[]## connected link list
        connectedpointsid=[]## connected point ID list
        for lcon in point.EdgeList:
            connectedlinks.append(lcon)
            if point.ID==lcon.FirstPoint.ID:
                nextpoint=lcon.LastPoint
            else:
                nextpoint=lcon.FirstPoint
            connectedpointsid.append(nextpoint.ID)
        return connectedpointsid,connectedlinks
    except:
        # Get the trace back object
        #
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
    
        # Concatenate information together concerning the error into a message string
        #
        pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
        #
        arcpy.AddError(pymsg)

def GetLengthPermit(simmethod,lengthmean,stlength,a):
    '''
    Get the length permit
    power law: simulate the length permit in power-law distribution
    normal distribution: simulate the length permit in normal distribution
    wuhan: simulate the length permit from survey data
    '''
    try:
        if simmethod == "Power Law":
            xmin = float(lengthmean)*((a-2.0)/(a-1.0))
            lengthpermit = float(xmin)*math.pow(1.-random.random(),-1./(a-1.))
    #                 LengthPermit = random.expovariate(float(MeanLength))
        if simmethod == "Normal Distribution":
            lengthpermit = random.normalvariate(float(lengthmean),float(stlength))
        if simmethod == "Wuhan":
            judgevalue  = random.randint(0,937)
            i = 0
            TripRang=[43,206,206,146,336]
            while (judgevalue - TripRang[i]>0):
                judgevalue = judgevalue - TripRang[i]
                i = i +1
            if i ==0:
                lengthpermit= random.uniform(0.0,1000)
            elif i ==1:
                lengthpermit= random.uniform(1000.0,3000.0)
            elif i ==2:
                lengthpermit= random.uniform(3000.0,5000.0)
            elif i ==3:
                lengthpermit= random.uniform(5000.0,8000.0)
            elif i ==4:
                lengthpermit= float(8000.0)*math.pow(1.-random.random(),-1./(2.5-1.))
        return lengthpermit
    except:
        # Get the trace back object
        #
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
    
        # Concatenate information together concerning the error into a message string
        #
        pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
        #
        arcpy.AddError(pymsg)

def CalculateRandomWalkingValue():
    '''
    Calculate the random walking values of a network
    '''
    try:
    
        ## parameters
        ThisTotalRvalue=1.0
        PreTotalRvalue=0.0
        loopvalue=1.0
        i=0
        # count of walking
        countnullloop=0
        # count of null walking
        WalkPath = Graphy.WalkPath()
        # record walking paths
        Walk = False
        #record whether the random laking is success
        '''
        Random walking loop
        '''
        arcpy.SetProgressor("step", "Random Walking...", 0,int(1/float(PPermit)), 2) 
        while loopvalue >= float(PPermit): # p threshold, default is 0.000001
            # if the random walking values of the entire nodes are stable, the random walking will terminate
            preloopvalue = loopvalue
            # python requires float number in devision
            loopvalue = (float(ThisTotalRvalue) - float(PreTotalRvalue))/float(ThisTotalRvalue)
            arcpy.SetProgressorLabel("Current loop value is " + str(loopvalue) + "...") 
            PreTotalRvalue = ThisTotalRvalue
            ThisPointNumber = random.choice(Net.NodeIDList)
            # index of point ID
            # 1st point ID is randomly selected
            i=i+1
            points=[]
            # contain points in current walking 
            pointsID=[]
            links=[]
            # contain edges in current walking 
            linksID=[]
            TotalLength=0.0
            # generate length permit for current walking
            LengthPermit = GetLengthPermit(SimulateMethod,MeanLength,StdLength,alpha)
            DeadEnd=False
            # record whether the current point is dead end
            DeadStart=False
            # record whether the first point is dead end
            DeadEndSelect=False
            # record whether the end selection is dead
            OtherWay=False
            # record whether start from the other side of the 1st point
  
            while TotalLength <= LengthPermit:
                
                # select the start point based on the ThisPointNumber
                RandomPoints=GetPoint(Net,ThisPointNumber)
    
                '''
                Check previous points
                '''
                while Contain(points,RandomPoints):
                    if DeadEnd:
                        if DeadEndSelect:
                            arcpy.AddWarning("\t Fail to find the next point because of DeadEnd point and Dead End selection, the current point is "+str(RandomPoints.ID)+"!") 
#                             arcpy.AddWarning(pointsID) 
#                             arcpy.AddWarning(linksID) 
                            points, pointsID,links,linksID,TotalLength,countnullloop=EndWalking(points,pointsID,links,linksID,TotalLength,LengthPermit,countnullloop)
                            break
                        else:                            
                            # start the walk from the other side of walk path
                            PreviousPoints = points[0] ## set the previous point as the 1st point
                    elif DeadEndSelect:
                        if OtherWay:
                            arcpy.AddWarning("\t Fail to find an Other Side walking, the current point is "+str(RandomPoints.ID)+"!") 
#                             arcpy.AddWarning(pointsID)
#                             arcpy.AddWarning(linksID) 
                            points, pointsID,links,linksID,TotalLength,countnullloop=EndWalking(points,pointsID,links,linksID,TotalLength,LengthPermit,countnullloop)
                            break
                        else:   
                            OtherWay=True
                            PreviousPoints = points[0] ## set the previous point as the 1st point
                    elif (not DeadEndSelect) and (not OtherWay):
                        PreviousPoints = points[len(points)-1] ## set the previous point as the 2nd last point
                    else:
                        arcpy.AddError("Unknown error") 
                        arcpy.AddError(pointsID) 
                        arcpy.AddError(linksID) 
                        arcpy.AddError(ThisPointNumber) 
                        arcpy.AddError(RandomPoints.ID) 
                        break
                    ConnectedPointsID,ConnectedLinks = GetConnectedElements(PreviousPoints)
                    NextPointID = random.choice(ConnectedPointsID)
                    # select the next points from the connected points of previous point
                    while (Contain(pointsID, NextPointID)):
                        ConnectedPointsID.remove(NextPointID)
                        if len(ConnectedPointsID)>0:
                            NextPointID= random.choice(ConnectedPointsID)
                        elif not DeadEndSelect:
                            # 1st time of dead end
                            DeadEndSelect = True
                            arcpy.AddWarning("\t Fail to select a next point in this side!") 
                            if (not DeadStart):
                                # dead start is false, there are other chances to start the walking from other side of the 1st point
                                # start the walk from another side of the first point
                                NextPointID = None
                                break
                            else:
                                # dead start is  true
                                # end current walking
                                arcpy.AddWarning("\t Fail to find the next point because of DeadStart point and Dead End selection, the current point is "+str(RandomPoints.ID)+"!") 
#                                 arcpy.AddWarning(pointsID) 
#                                 arcpy.AddWarning(linksID) 
                                points, pointsID,links,linksID,TotalLength,countnullloop=EndWalking(points,pointsID,links,linksID,TotalLength,LengthPermit,countnullloop)
                                break
                        elif OtherWay:
                            break
                        else:
                            arcpy.AddError("Unknown error") 
                            arcpy.AddError(pointsID) 
                            arcpy.AddError(linksID) 
                            arcpy.AddError(ThisPointNumber) 
                            arcpy.AddError(RandomPoints.ID) 
                            break

                    if len(ConnectedPointsID)>0 and NextPointID<>None:
                        RandomPoints=GetPoint(Net,NextPointID)
                        ThisPointNumber=NextPointID
                        # replace the last edge in walking path
                        for cl in ConnectedLinks:
                            if (cl.FirstPoint.ID == NextPointID and cl.LastPoint.ID==PreviousPoints.ID)or (cl.LastPoint.ID == NextPointID and cl.FirstPoint.ID==PreviousPoints.ID):
                                if DeadEnd:
                                    # add new edge directly in the walking path
                                    links.append(cl)
                                    linksID.append(cl.ID)
                                else:
                                    # replace the last edge with the new edge in the walking path
                                    links[len(links)-1]=cl
                                    linksID[len(linksID)-1]=cl.ID
                                # re-calculate the total length
                                TotalLength= GetTotalLength(links)
                        
                    elif DeadEndSelect:
                        if DeadStart:
                            break
                        else:
                            RandomPoints = points[0]
                            arcpy.AddWarning("\t Start walking from the other side of the 1st point."    ) 
                    else:
                        arcpy.AddError("Unknown error") 
                        arcpy.AddError(pointsID) 
                        arcpy.AddError(linksID) 
                        arcpy.AddError(ThisPointNumber) 


                # select the connected link based on weight
                if points<>None and links <> None:
                    RandomLinks=GetNextRandomLink(RandomPoints,SelectionType,links)
                    
                '''
                Check whether new link has already been walked through
                '''
                if len(RandomPoints.EdgeList)>1 and points <> None:
                
                    while (Contain(linksID, RandomLinks.ID)):
                        if DeadEnd or DeadStart:
                            LoopFirstPointID=RandomLinks.FirstPoint.ID
                            LoopLastPointID=RandomLinks.LastPoint.ID                               
                            if LoopFirstPointID == pointsID[0] or LoopLastPointID==pointsID[0]:
                                
                                arcpy.AddWarning("\t Fail to find the next point because of loop with dead point "+str(RandomPoints.ID)+"!") 
                                points, pointsID,links,linksID,TotalLength,countnullloop=EndWalking(points,pointsID,links,linksID,TotalLength,LengthPermit,countnullloop)
                                break
                            else:
                                RandomLinks=GetNextRandomLink(RandomPoints,SelectionType,links)
                    # if current link has already been walked, select another link
                        else:
                            RandomLinks=GetNextRandomLink(RandomPoints,SelectionType,links)

                    if RandomLinks.FirstPoint.ID == ThisPointNumber:
                        ThisPointNumber = RandomLinks.LastPoint.ID
                    else:
                        ThisPointNumber =  RandomLinks.FirstPoint.ID
                else:
                    if points <> None and len(RandomPoints.EdgeList)==1: 
                        if len(points)==0:
                            ## the isolated point is selected as 1st point
                            DeadStart = True
                            arcpy.AddWarning("\t Dead start point of "+str(RandomPoints.ID)+" has been selected!") 
                            RandomLinks = RandomPoints.EdgeList[0]
                            if RandomLinks.FirstPoint.ID == ThisPointNumber:
                                ThisPointNumber = RandomLinks.LastPoint.ID
                            else:
                                ThisPointNumber = RandomLinks.FirstPoint.ID
                        else: 
                            ## the isolated point is selected as the internal point
                            DeadEnd = True
                            arcpy.AddWarning("\t Dead end point of "+str(RandomPoints.ID)+" has been selected!") 
                            if DeadStart:
                                arcpy.AddWarning("\t Dead walk from "+str(points[0].ID)+"to "+str(RandomPoints.ID)+"!") 
                                points, pointsID,links,linksID,TotalLength,countnullloop=EndWalking(points,pointsID,links,linksID,TotalLength,LengthPermit,countnullloop)
                                
                            else:
                                # start the next walk from the 1st point
                                ThisPointNumber=points[0].ID
                ## end of check new edge
                                  
                if (points<>None and links <>None):
                    if (not Contain(pointsID,RandomPoints.ID)):
#                     RandomPoints.ID not in pointsID:
                        pointsID.append(RandomPoints.ID)
                        points.append(RandomPoints)
                    if (not Contain(linksID,RandomLinks.ID)):
#                     RandomLinks.ID not in linksID:
                        linksID.append(RandomLinks.ID)
                        links.append(RandomLinks)
                    
                    TotalLength= GetTotalLength(links)

            '''
            Add the terminal point to walk
            '''
            if points<> None and links <> None:
                ## get terminal point
                if points[len(points)-1].ID == links[len(links)-1].FirstPoint.ID:
                    TerminalPoint = links[len(links)-1].LastPoint
                else:
                    TerminalPoint = links[len(links)-1].FirstPoint
    
                ## check whether the terminal point has already been walked
                if(not Contain(points, TerminalPoint)) and (not Contain(pointsID, TerminalPoint.ID)):
                    # not been walked
                    # add to points
                    points.append(TerminalPoint)
                    pointsID.append(TerminalPoint.ID)
                else:
                    # has already been walked
                    # remove the corresponding link
                    links.remove(links[len(links)-1]) 
                    linksID.remove(linksID[len(linksID)-1])
                '''
                Increase the random walking value of points and edges in the current walk journal
                '''
                IncreaseRvalue(points)
                IncreaseRvalue(links)
                '''
                Record the points and links of the current walk journal
                '''
                SingleWalk=Graphy.SingleWalk(i,TotalLength,LengthPermit,pointsID,linksID)
                WalkPath.walks.append(SingleWalk)

                ThisTotalRvalue = GetTotalRvalue()

            ## check loop value in case that points and links are null
            if ThisTotalRvalue ==0:
                ThisTotalRvalue =1
                PreTotalRvalue = 0
            if loopvalue ==0:
                loopvalue = preloopvalue
            ## end of check loop value
            arcpy.SetProgressorPosition()
       
        arcpy.ResetProgressor()
        Walk = True
        # this random walking is successful
        if Walk:
            arcpy.AddMessage("Random walking calculation is finished!") 
            arcpy.AddMessage("Total number of walking is "+str(i)+"!")
            arcpy.AddWarning("Total number of invalid walking is "+str(countnullloop)+"!")
            arcpy.AddMessage("Final loop value is "+str(loopvalue)+"!")
            arcpy.AddMessage("Total Random Walking value is "+str(ThisTotalRvalue)+"!")
            WalkPath.i = i
            WalkPath.loopvalue = loopvalue
            WalkPath.countnullloop = countnullloop
            WalkPath.totalrvalue = ThisTotalRvalue
            return Walk,WalkPath

    except:
        # Get the trace back object
        #
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
    
        # Concatenate information together concerning the error into a message string
        #
        pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    
        # Return python error messages for use in script tool or Python Window
        #
        # Print Python error messages for use in Python / Python Window
        #
        Walk = False
        arcpy.AddError(pymsg)
        arcpy.AddError(pointsID) 
        arcpy.AddError(linksID) 
        arcpy.AddError("Random point: "+ str(RandomPoints.ID)) 
         

    
walk,walkpath=CalculateRandomWalkingValue()

def WriteToFile(Walk,WalkPath):
    '''
    Write the random walking result to file
    '''
    try:
        if Walk:
            arcpy.AddMessage("Start to write result into files.") 

            env.workspace=(OutputFolder)
            arcpy.env.overwriteOutput = True
            
            '''
            Insert point rvalue to point table
            '''
            arcpy.CreateTable_management(OutputFolder,str(PointTable)+".dbf")
            arcpy.AddField_management(str(PointTable)+".dbf","NodeFID" , "SHORT")
            arcpy.AddField_management(str(PointTable)+".dbf","Degree" , "SHORT")            
            arcpy.AddField_management(str(PointTable)+".dbf",RField , "Long")
            pointrows = arcpy.InsertCursor(str(OutputFolder)+"\\"+str(PointTable)+".dbf")
            for p in Net.NodeList:
                pointrow = pointrows.newRow()
                pointrow.setValue("NodeFID",p.ID)
                pointrow.setValue("Degree",p.degree)
                pointrow.setValue(RField,p.rvalue)
                pointrows.insertRow(pointrow)
            
            '''
            Insert link rvalue to link table
            '''    
            
            arcpy.CreateTable_management(OutputFolder,str(LinkTable)+".dbf")
            
            arcpy.AddField_management(str(LinkTable)+".dbf","LinkFID" , "SHORT")
            arcpy.AddField_management(str(LinkTable)+".dbf","Connect" , "SHORT")
            arcpy.AddField_management(str(LinkTable)+".dbf",RField , "Long")
            linkrows = arcpy.InsertCursor(str(OutputFolder)+"\\"+str(LinkTable)+".dbf")
            for l in Net.EdgeList:
                linkrow = linkrows.newRow()
                linkrow.setValue("LinkFID",l.ID)
                linkrow.setValue("Connect",l.connect)
                linkrow.setValue(RField,l.rvalue)
                linkrows.insertRow(linkrow)
                
            '''
            Export the walking path to a file
            '''
            
            sys.setrecursionlimit(1000000)
            ## enlarge the cursive limit
            # dump walking path to a file
            OutPutFiel = open(OutputFolder+"\\"+WalkPathName+".wlk","wb")
            ## Export the point path to a file

            pickle.dump(WalkPath,OutPutFiel,2)
            ## dump the class into binary
            OutPutFiel.close()

            arcpy.AddMessage("Done!")
        else:
            arcpy.AddWarning("The walking calculation is failed." )   
    except:

        # Get the traceback object
        #
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
    
        # Concatenate information together concerning the error into a message string
        #
        pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
        msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
    
        # Return python error messages for use in script tool or Python Window
        #
        arcpy.AddError(pymsg)
        arcpy.AddError(msgs)

WriteToFile(walk,walkpath)