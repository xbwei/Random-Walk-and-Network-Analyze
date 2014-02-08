'''
Created on Oct 6, 2013
@author: Xuebin Wei
weixuebin@gmail.com
Dept of GGY, UGA

Calculate page rank and centrality of network
'''

import networkx as nx
# import Graphy
import arcpy
from arcpy import env
#import pickle
import cPickle as pickle
# import random
import sys
import traceback

try:

    '''
    Debug only parameters
    '''
#     Netfile = r"D:\project\UGA\Research\randomwalking\RandomWalkingPy\data\Network\WuhanConnectNet.net"
#     # load the network class file
#     OutputFolder=r"D:\project\UGA\Research\randomwalking\RandomWalkingPy\data\Centrality"
#     TableName = "WuhanConCentrality"
    Netfile = arcpy.GetParameterAsText(0)
    OutputFolder = arcpy.GetParameterAsText(1)
    TableName = arcpy.GetParameterAsText(2)

    unpicklefile = open(Netfile, 'rb')
    Net = pickle.load(unpicklefile)
    
    '''
    Construct the graph of noteworkx
    '''
    arcpy.AddMessage("Constructing graph of networkx...")
    arcpy.SetProgressor("step","Constructing the node graph of networkx...",0,len(Net.NodeList), 1) 
    G=nx.Graph()
    for node in Net.NodeList:
        arcpy.SetProgressorLabel("Reading the Node with FID of " + str(node.ID) + " ...") 
        G.add_node(node.ID)
        arcpy.SetProgressorPosition()
    arcpy.ResetProgressor()
    
    arcpy.SetProgressor("step","Constructing the edge graph of networkx...",0,len(Net.EdgeList), 1) 
    for edge in Net.EdgeList:
        arcpy.SetProgressorLabel("Reading the Edge with FID of " + str(edge.ID) + " ...") 
        G.add_edge(edge.FirstPoint.ID, edge.LastPoint.ID, weight=edge.weight,connect = edge.connect)
        arcpy.SetProgressorPosition()
    arcpy.ResetProgressor()
    '''
    Create table of point ID and degree
    '''
    env.workspace=(OutputFolder)
    arcpy.env.overwriteOutput = True
    
    arcpy.AddMessage("Creating point table...")
    arcpy.CreateTable_management(OutputFolder,str(TableName)+".dbf")
    arcpy.AddField_management(str(TableName)+".dbf","NodeFID" , "SHORT")
    arcpy.AddField_management(str(TableName)+".dbf","Degree" , "SHORT")  
    pointrows = arcpy.InsertCursor(str(OutputFolder)+"\\"+str(TableName)+".dbf")
    for p in Net.NodeList:
        pointrow = pointrows.newRow()
        pointrow.setValue("NodeFID",p.ID)
        pointrow.setValue("Degree",p.degree)
        pointrows.insertRow(pointrow)
    del p, pointrows
    # '''
    # Checking edges in graph
    # debug only
    # '''
    # for n,nbrs in G.adjacency_iter():
    #     for nbr,eattr in nbrs.items():      
    #         data=eattr['weight']
    #         print('(%d, %d, %.3f)' % (n,nbr,data))
    '''
    Calculate networkx value for each node
    '''
#     arcpy.AddMessage("Calculating page rank values...")
#     pr= nx.pagerank_numpy(G)
    arcpy.SetProgressor("step","Constructing the node graph of networkx...",0,9, 1) 
    
    arcpy.SetProgressorLabel("Calculating page rank values... ")
    arcpy.SetProgressorPosition()
    arcpy.AddMessage("Calculating page rank values...")
    
    pr= nx.pagerank_numpy(G,weight="None")
    arcpy.SetProgressorLabel("Calculating page rank values weighted by weight... ")
    arcpy.SetProgressorPosition()
    arcpy.AddMessage("Calculating page rank values weighted by weight...")
    
    wpr= nx.pagerank_numpy(G,weight="weight")
    
    arcpy.SetProgressorLabel("Calculating page rank values weighted by connect... ")
    arcpy.SetProgressorPosition()
    arcpy.AddMessage("Calculating page rank values weighted by connect...")
    
    cpr= nx.pagerank_numpy(G,weight="connect")
        
    arcpy.SetProgressorLabel("Calculating load centrality... ")
    arcpy.SetProgressorPosition()
    arcpy.AddMessage("Calculating load centrality...")
    ld= nx.load_centrality(G,weight="None")
    
    arcpy.SetProgressorLabel("Calculating degree centrality... ")
    arcpy.SetProgressorPosition()    
    arcpy.AddMessage("Calculating degree centrality...")
    dg= nx.degree_centrality(G)
    
    arcpy.SetProgressorLabel("Calculating closeness centrality... ")
    arcpy.SetProgressorPosition() 
    arcpy.AddMessage("Calculating closeness centrality...")
    clns= nx.closeness_centrality(G)
    
    arcpy.SetProgressorLabel("Calculating betweenness centrality... ")
    arcpy.SetProgressorPosition()
    arcpy.AddMessage("Calculating betweenness centrality...")
    btwn= nx.betweenness_centrality(G,weight="None")
    
    arcpy.SetProgressorLabel("Calculating eigenvector centrality... ")
    arcpy.SetProgressorPosition()
    arcpy.AddMessage("Calculating eigenvector centrality...")
    egnvct= nx.eigenvector_centrality_numpy(G)
    arcpy.ResetProgressor()
    
    arcpy.AddMessage("Writing result to table...")
    arcpy.AddField_management(str(TableName)+".dbf","pgrnk" , "FLOAT")
    arcpy.AddField_management(str(TableName)+".dbf","wpgrnk" , "FLOAT")
    arcpy.AddField_management(str(TableName)+".dbf","cpgrnk" , "FLOAT")
    arcpy.AddField_management(str(TableName)+".dbf","loadcnt" , "FLOAT")
    arcpy.AddField_management(str(TableName)+".dbf","degreecnt" , "FLOAT")
    arcpy.AddField_management(str(TableName)+".dbf","clnscnt" , "FLOAT")
    arcpy.AddField_management(str(TableName)+".dbf","btnscnt" , "FLOAT")
    arcpy.AddField_management(str(TableName)+".dbf","egvnctcnt" , "FLOAT")
    
    rowcount = arcpy.GetCount_management(str(OutputFolder)+"\\"+str(TableName)+".dbf")
    arcpy.SetProgressor("step","Start reading edges and nodes",0,int(rowcount.getOutput(0)), 1) 
    rows = arcpy.UpdateCursor(str(OutputFolder)+"\\"+str(TableName)+".dbf")
    for row in rows:
        arcpy.SetProgressorLabel("Updating the Node with FID of " + str(row.getValue("NodeFID")) + " ...")
        for n in G:
            if row.getValue("NodeFID")==n:
                row.setValue("pgrnk",pr.get(n))
                row.setValue("wpgrnk",wpr.get(n))
                row.setValue("cpgrnk",cpr.get(n))
                row.setValue("loadcnt",ld.get(n))
                row.setValue("degreecnt",dg.get(n))
                row.setValue("clnscnt",clns.get(n))
                row.setValue("btnscnt",btwn.get(n))
                row.setValue("egvnctcnt",egnvct.get(n))

                rows.updateRow(row) 
        arcpy.SetProgressorPosition()
    arcpy.ResetProgressor()
    del row,rows,wpr,ld,dg,clns,btwn,egnvct

    arcpy.AddMessage("Done!")
    
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
