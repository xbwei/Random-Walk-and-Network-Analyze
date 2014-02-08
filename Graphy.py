'''
Created on Sep 10, 2013

@author: Xuebin Wei
weixuebin@gmail.com
Dept of GGY, UGA
Define the lasses of network
'''

import arcpy
import sys
import traceback

class Node():
    try:
        '''
        Define class of node
        '''
        def __init__(self,PX,PY,NodeLayer,NX,NY):
            '''
            PX,PY: X,Y coordination value of link
            NX,NP: X,Y coordination field name of point
            find the FID of the fist and the last point of the link 
            '''
    
            self.x=PX
            self.y=PY
            self.ID= 0
            self.EdgeList=[]
            self.EdgeIDList=[]
            ## the ID list  ensure that each instance element in the list is unique
    #         self.weight=0
            self.degree=0
            self.rvalue=0
            expression =  str(NX)+" = "+str(PX)+" AND "+str(NY)+" = "+str(PY)
            NodeRows = arcpy.SearchCursor(NodeLayer,where_clause=expression)
            # use search cursor to find the point ID
            for NodeRow in NodeRows:
                ##shape = NodeRow.shape
                ## get geometry object of point
#                 arcpy.AddMessage(NodeRow.getValue("X"))
#                 arcpy.AddMessage(NodeRow.getValue("Y"))
                self.ID=NodeRow.getValue("FID")
                    # self.weight = NodeRow.getValue(Weight)
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
      
class Edge():
    '''
    Define class of edge
    '''
    def __init__(self,P1,P2):
        self.FirstPoint=P1
        self.LastPoint=P2
        self.length=0.0
        self.weight=0
        self.ID=0
        self.connect=0
        self.rvalue=0
        self.NID=0
        # ID of nature street
        self.Nweight=0
        # weight for nature street calculating
        
class Graphy():
    '''
    Define class of graph
    '''
    def __init__(self):
        ## install unique Node object
        self.NodeList=[]
        ## install Node ID 
        self.NodeIDList=[]
        ## the ID list  ensure that each instance element in the list is unique
        ## install unique Edge object
        self.EdgeList=[]
        ## install edge ID
        self.EdgeIDList=[]
        ## the ID list  ensure that each instance element in the list is unique
        
class SingleWalk():
    '''
    Define class of single walk
    '''
    def __init__(self,index,length,lenpermit,pointpath,edgepath):
        self.number=index
        # index of this walking
        self.walklength=length
        # length of this walking
        self.lenthpermit=lenpermit
        # length permit of this walking
        self.points=pointpath
        # points ID in this walking
        self.edges=edgepath
        # edges ID in this walking

class WalkPath():
    '''
    Define class of walk results
    '''
    def __init__(self):
        self.walks=[]
        self.i=0
        self.countnullloop=0
        self.loopvalue=0.0
        self.totalrvalue=0.0
        
        
