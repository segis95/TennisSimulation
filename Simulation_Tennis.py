# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 19:40:37 2016

@author: Sergey
"""

import pandas as pd
import xlrd
import numpy
import math

path = 'C:\Users\Sergey\Desktop\Simulation Tennis\\'
eps = math.log(2)/240.0
def tofloat(s):
    if (s == '') or (s == u'') or (s == u' '):
        return 0.0
    else:
        return float(s)
        
def parse_data(n):
        
    rd = xlrd.open_workbook(path + str(2000 + n) +'.xls',formatting_info=False )
    sheet = rd.sheet_by_index(0)
    goodlist = numpy.array([sheet.row_values(i) for i in range(1,sheet.nrows)])
    indexes_good = [i for i in range(1,len(goodlist)) if (goodlist[i][27] == 'Completed')]
    goodlist = goodlist[indexes_good]
    final_list = [[tofloat(goodlist[i][3]), goodlist[i][9], goodlist[i][10],\
    tofloat(goodlist[i][15]) + tofloat(goodlist[i][17]) + tofloat(goodlist[i][19]) + tofloat(goodlist[i][21]) + tofloat(goodlist[i][23]),\
    tofloat(goodlist[i][16]) + tofloat(goodlist[i][18]) + tofloat(goodlist[i][20]) + tofloat(goodlist[i][22]) + tofloat(goodlist[i][24])] for i in range(len(goodlist))]
    
    return final_list
    
def Y_ij(x,y):
    Lp = set(Pairs_match[(x,y)])
    L = [games[i] for i in Lp]
    summ = 0
    for match in L:
        if (match[1] == x):
            summ = summ + math.exp(-eps*(match[0] - 38335.0)) * match[3]
        else:
            summ = summ + math.exp(-eps*(match[0] - 38335.0)) * match[4]
    return summ
    
def iteration(d):

    d1 = d.copy()
    n = 0
    for x in d1.keys():
        n = n + 1
        s1 = sum([Y_ij(x,y) for y in SP if (y != x)])
        s2 = sum([(Y_ij(y,x) + Y_ij(x,y))/(d1[x] + d1[y]) for y in SP if (y != x)])
        d1[x] = s1/s2

    return d1
    
    
        
"""    
L5 = parse_data(5)
L6 = parse_data(6)
L7 = parse_data(7)
L8 = parse_data(8)
L9 = parse_data(9)

SP1 = set([L5[i][1] for i in range(len(L5))]).union([L6[i][1] for i in range(len(L6))], [L7[i][1] for i in range(len(L7))], [L8[i][1] for i in range(len(L8))])
SP2 = set([L5[i][2] for i in range(len(L5))]).union([L6[i][2] for i in range(len(L6))], [L7[i][2] for i in range(len(L7))], [L8[i][2] for i in range(len(L8))])
SP = SP1.union(SP2)

games = L5 + L6 + L7 + L8

Winners = set([games[i][1] for i in range(len(games))])
players = dict.fromkeys(SP,1)
#Pairs_match = {(x,y):[i for i in range(len(games)) if ((games[i][1] == x)and(games[i][2] == y)or(games[i][1] == y)and(games[i][2] == x))] for x in SP for y in SP}
"""
"""
players = dict.fromkeys(SP,1)
for i in range(100):
    if (i%10 == 0):
        print(i)
    players  = iteration(players)
"""
win = 0
loss = 0
for m in L9:
    x = m[1]
    y = m[2]
    
    if ((x not in SP) or (y not in SP)):
        continue
    if (players[x] > players[y]):
        win = win + 1
    else:
        loss = loss + 1

print(win)
print(loss)