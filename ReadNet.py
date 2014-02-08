'''
Created on Sep 24, 2013
@author: Xuebin Wei
weixuebin@gmail.com
Dept of GGY, UGA

Read the Net class 
Debug only
Inspect the graphy or walk path instance
'''
#import pickle
import cPickle as pickle


Netfile = r'C:\UGA\Paper\randomwalking\RandomWalkingPy\data\Network\Atlanta_Dekable_Script.net'


unpicklefile = open(Netfile, 'rb')
Net = pickle.load(unpicklefile)
#Net = pickle.load(unpicklefile)
#for walk in Net.walks:
#    print walk.number
#    print walk.walklength
#    print walk.lenthpermit
#    print walk.points
#    print walk.edges
    
#for Edge in Net.EdgeList:
#    print '----'
#    print Edge.ID
#    print Edge.connect
#    print Edge.weight
#    for edge in Edge.FirstPoint.EdgeList:
#        print"\t----"
#        print "\t" + str(edge.ID)
#        print "\t" + str(edge.weight)
#        print "\t"+ str(edge.connect)
#    for edge in Edge.LastPoint.EdgeList:
#        print"\t===="
#        print "\t" + str(edge.ID)
#        print "\t" + str(edge.weight)
#        print "\t" + str(edge.connect)
#    
for Node in Net.NodeList:
    print '===='
    print Node.ID
    print Node.degree
    print Node.weight
    for edge in Node.EdgeList:
        print "\t---"
        print "\t" + str(edge.ID)
        print "\t" + str(edge.connect)
        print "\t" + str(edge.weight)

#print Net