'''
Created on Sep 17, 2013

@author: Xuebin Wei
weixuebin@gmail.com
Dept of GGY, UGA
Test the random selection method and power-law simulation
Debug only
'''
# 
import random
import math

random.seed()

#class test():
#    def __init__(self,w):
#        self.weight=w
#        
##tlist=[]
##
##for i in range(1,200):
##    tlist.append(test(random.randrange(10)))
##    print tlist[i-1].weight
#
#tlist=[test(0),test(500)]
#
#print tlist
#
#
#
#for i in range(1,1000):
#    TotalWeight = 0
#    linknumber = 0
#    for tl in tlist:
#        TotalWeight =TotalWeight + tl.weight
#    
#    # generate judge value for next link selection
#    JudgeLinkValue = random.randint(0,TotalWeight)
#    
#    while ((JudgeLinkValue - tlist[linknumber].weight) >0):
#        JudgeLinkValue = JudgeLinkValue - tlist[linknumber].weight
#        linknumber = linknumber+1
#        
#
#    print "\t"+ str(tlist[linknumber].weight)
#    
# def GetRandom():
#     '''
#     Test length permit generation 
#     '''
#     r1=random.random()
#     r2=random.random()
#     gset = 5000 + 1000*math.sqrt (2*math.log (1/(1-r1 ))) * math.cos(2*math.pi *r2);
#     return gset;
# 
# for i in range(0,1000):
# #     print random.normalvariate(5000,1000)
# #     print GetRandom()
# #     print random.gauss(5000,1000)
#     print random.expovariate(1.0/5000.0)

#from PowerLawGen import *
#a=2.5
#mean = 5000.0
#xmin = mean*((a-2.0)/(a-1.0))
#print xmin
#x = randht(1000,'xmin',1000,'powerlaw',a); 
#for i in x:
#    print i


'''
test power law generation
'''
# MeanLength = 5000
# alpha = 2.5
# 
# xmin = float(MeanLength)*((alpha-2.0)/(alpha-1.0))
# #xmin = 1000.0
# #print xmin
# 
# for i in range(0,1000):
#     LengthPermit = float(xmin)*math.pow(1.-random.random(),-1./(alpha-1.))
#     print LengthPermit

'''
test Wuhan trip distribution
'''
for p in range(0,1000):
    judgevalue  = random.randint(0,1000)
    # the link with greater weight will more likely be selected
    i = 0
    TripRang=[43,206,206,146,336,63]
    while (judgevalue - TripRang[i]>0):
        judgevalue = judgevalue - TripRang[i]
        i = i +1
    if i ==0:
        print random.uniform(0.0,1000)
    elif i ==1:
        print random.uniform(1000.0,3000.0)
    elif i ==2:
        print random.uniform(3000.0,5000.0)
    elif i ==3:
        print random.uniform(5000.0,8000.0)
    elif i ==4:
        print float(8000.1)*math.pow(1.-random.random(),-1./(2.5-1.))
#     else:
#         print ""