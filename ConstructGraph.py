'''
Created on Sep 10, 2013
@author: Xuebin Wei
weixuebin@gmail.com
Dept of GGY, UGA

Construct the network 

'''

import Graphy
import arcpy
#import pickle
import cPickle as pickle
import sys
import traceback
 
EdgeLayer = arcpy.GetParameterAsText(0)
EdgeWeight = arcpy.GetParameterAsText(1)
Nature = arcpy.GetParameterAsText(2)
NatureID = arcpy.GetParameterAsText(3)
NodeLayer = arcpy.GetParameterAsText(4)
NodeX = arcpy.GetParameterAsText(5)
# coordination x of point
NodeY = arcpy.GetParameterAsText(6)
# coordination y of point
OutputFoder = arcpy.GetParameterAsText(7)
NetworkName = arcpy.GetParameterAsText(8)

  
# '''
# Debug parameters
# '''
# EdgeLayer = r'D:\project\UGA\Research\randomwalking\RandomWalkingPy\data\WalkingResult\Atlanta\CityCenter\Clayton_Road_NoDangle.shp'
# EdgeWeight = r'SPEED'
# Nature = False
# NatureID = '#'
# NodeLayer = r'D:\project\UGA\Research\randomwalking\RandomWalkingPy\data\WalkingResult\Atlanta\CityCenter\Clayton_Road_NoDangle_ND_Junctions.shp'
# OutputFoder = r'D:\project\UGA\Research\randomwalking\RandomWalkingPy\data\Network'
# NetworkName = r'Clayton'
# NodeX = "X"
# NodeY = "Y"

def ConstructGraph(edge,node):
    ## Create graph class
    try:    
        Network = Graphy.Graphy()
        ## Create node and edge cursor
        EdgeRows = arcpy.SearchCursor(edge)
        rowcount = arcpy.GetCount_management(edge)
        
        arcpy.SetProgressor("step","Start reading edges and nodes",0,int(rowcount.getOutput(0)), 1) 
        # set a progress bar
        
        arcpy.AddMessage("There are "+str(rowcount)+" edges in this dataset")
        
        for EdgeRow in EdgeRows:
            shape = EdgeRow.shape
            ## get geometry object of edge
            
            arcpy.SetProgressorLabel("Reading the Edge with FID of " + str(EdgeRow.getValue("FID")) + " ...") 
            print ("Reading the Edge with FID of " + str(EdgeRow.getValue("FID")) + " ...") 
              
            
            ## set the first node of the edge as a node
            FirstNode= Graphy.Node(shape.firstPoint.X,shape.firstPoint.Y,NodeLayer,NodeX,NodeY)
            
               
            ## set the last node of the edge as a node
            LastNode=Graphy.Node(shape.lastPoint.X,shape.lastPoint.Y,NodeLayer,NodeX,NodeY)
            
        
            ## create a edge
            Edge=Graphy.Edge(FirstNode,LastNode)
            Edge.ID=EdgeRow.getValue("FID")
            Edge.weight=EdgeRow.getValue(EdgeWeight)
            Edge.length=shape.length
            if Nature:
                Edge.NID = EdgeRow.getValue(NatureID)
            
            
            ## add edge to network class
            if Edge.ID not in Network.EdgeIDList:
                Network.EdgeIDList.append(Edge.ID)
                Network.EdgeList.append(Edge)
                
            ## add first and last point in network node list    
                 
            if FirstNode.ID not in Network.NodeIDList:
                Network.NodeIDList.append(FirstNode.ID)
                Network.NodeList.append(FirstNode)
            if LastNode.ID not in Network.NodeIDList:
                Network.NodeIDList.append(LastNode.ID)
                Network.NodeList.append(LastNode)

                
            arcpy.SetProgressorPosition()
        
        arcpy.AddMessage("\t"+str(len(Network.EdgeList)) +" edges have been created in Network." )
        arcpy.AddMessage("\t"+str(len(Network.NodeList)) +" points have been created in Network." )
        
        del EdgeRow, EdgeRows, rowcount
        del FirstNode,LastNode,shape
        arcpy.ResetProgressor()
    
        
        ## clear variables
        
        arcpy.AddMessage("Checking duplicated edges")
        # check whether ID is duplicate
        arcpy.SetProgressor("step","Start checking duplicated edges",0,int(len(Network.EdgeList)), 1) 
        for EdgeCheck1 in Network.EdgeList:
            arcpy.SetProgressorLabel("Checking the Edge with FID of " + str(EdgeCheck1.ID) + " ...") 
        
            for EdgeCheck2 in Network.EdgeList:
                if EdgeCheck1.FirstPoint.ID == EdgeCheck2.FirstPoint.ID and EdgeCheck1.LastPoint.ID == EdgeCheck2.LastPoint.ID and EdgeCheck1.length==EdgeCheck2.length:
                    if EdgeCheck1.ID <> EdgeCheck2.ID:
                        arcpy.AddWarning("\t"+str(EdgeCheck1.ID) +" and "+ str(EdgeCheck2.ID)+" are same edges")
            arcpy.SetProgressorPosition()
                        
        del EdgeCheck1,EdgeCheck2              
        arcpy.ResetProgressor()
        
        arcpy.AddMessage("Constructing connected edge list for each node")
        # construct EdgeList of each node
        arcpy.SetProgressor("step","Start constructing connected edge list",0,int(len(Network.EdgeList)), 1) 
        for Node in Network.NodeList:
            arcpy.SetProgressorLabel("Constructing the Edge list for the Node with FID of " + str(Node.ID) + " ...") 
            for Edge in Network.EdgeList:
                ''' wrong method because some edge.point.edgelist can not update
#                if Edge.FirstPoint.ID == Node.ID or Edge.LastPoint.ID == Node.ID:
#                    Node.EdgeList.append(Edge)
#                    Node.EdgeIDList.append(Edge.ID)
                '''
                if Edge.FirstPoint.ID == Node.ID:
                    if Edge.ID not in Node.EdgeIDList:
                        Node.EdgeList.append(Edge)
                        Node.EdgeIDList.append(Edge.ID)
                        Node.degree=len(Node.EdgeList)
                        Edge.FirstPoint.EdgeList=Node.EdgeList
                        Edge.FirstPoint.EdgeIDList=Node.EdgeIDList
                if Edge.LastPoint.ID == Node.ID:
                    if Edge.ID not in Node.EdgeIDList:
                        Node.EdgeList.append(Edge)
                        Node.EdgeIDList.append(Edge.ID)
                        Node.degree=len(Node.EdgeList)
                        Edge.LastPoint.EdgeList=Node.EdgeList
                        Edge.LastPoint.EdgeIDList=Node.EdgeIDList
                '''wrong method because some edge.point.edgelist can not update
#                if Edge.ID not in Edge.FirstPoint.EdgeIDList:
#                    Edge.FirstPoint.EdgeList.append(Edge)
#                    Edge.FirstPoint.EdgeIDList.append(Edge.ID)
#                if Edge.ID not in Edge.LastPoint.EdgeIDList:
#                    Edge.LastPoint.EdgeList.append(Edge)
#                    Edge.LastPoint.EdgeIDList.append(Edge.ID)
                '''
            arcpy.SetProgressorPosition()
        arcpy.AddMessage("Node connection list has been constructed")

        arcpy.ResetProgressor()
        ## clear variables
                
        arcpy.AddMessage("Checking duplicated nodes")
        # check whether ID is duplicate
        arcpy.SetProgressor("step","Start checking duplicated nodes",0,int(len(Network.NodeList)), 1) 
        for NodeCheck1 in Network.NodeList:
            arcpy.SetProgressorLabel("Checking the Node with FID of " + str(NodeCheck1.ID) + " ...") 
        
            for NodeCheck2 in Network.NodeList:
                if NodeCheck1.x == NodeCheck2.x and NodeCheck1.y == NodeCheck2.y:
                    if NodeCheck1.ID <> NodeCheck2.ID:
                        arcpy.AddWarning("\t"+str(NodeCheck1.ID) +" and "+ str(NodeCheck2.ID)+" are same nodes")
            arcpy.SetProgressorPosition()
        del NodeCheck1,NodeCheck2    
        arcpy.ResetProgressor()        

        
        arcpy.AddMessage("Calculating connect for each edge")
        arcpy.SetProgressor("step","Start calculating connect for the Edge ",0,int(len(Network.EdgeList)), 1) 
        for Edge in Network.EdgeList:
            arcpy.SetProgressorLabel("Constructing the Node list for the Edge with FID of " + str(Edge.ID) + " ...") 
            if len(Edge.FirstPoint.EdgeList)==0 or len(Edge.LastPoint.EdgeList)==0:
                arcpy.AddWarning("\t"+str(Edge.ID)+" 's connected points have empty edge list!")
            Edge.connect= len(Edge.FirstPoint.EdgeList) + len(Edge.LastPoint.EdgeList)-2
            arcpy.SetProgressorPosition()
        arcpy.AddMessage("Connect of each edge has been calculated")
        arcpy.ResetProgressor() 
        
        return Network

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

Net = ConstructGraph(EdgeLayer,NodeLayer)
## Construct the graph

try:   
    '''
    Write the network to a file
    '''
    OutPutFiel = open(OutputFoder+"\\"+NetworkName+".net","wb")
    ## Export the graph to a file
    sys.setrecursionlimit(10000000)
    ## enlarge the cursive limit
    pickle.dump(Net,OutPutFiel,2)
    ## dump the class into binary
    OutPutFiel.close()
    arcpy.AddMessage("The graph of "+str(NetworkName)+".net has been constructed in "+str(OutputFoder))
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
