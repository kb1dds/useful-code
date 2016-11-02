#!/bin/python
# Produce time and effort analyses needed on a typical AU T&E cert form:
# Percentage instructional time (T)
# Percentage service and administrative time (S+A)
# Percentages for each research project (R+G)
#
# Usage:
#  python te_process.py month1 month2 ...
#
# Copyright (c) 2016, Michael Robinson
# Distribution of unaltered copies permitted for noncommercial use only
# All other uses require express permission of the author
# This software comes with no warrantees express or implied

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# load the data 
df=pd.concat([pd.read_csv(sys.argv[i] + ".csv") for i in range(1,len(sys.argv))])

# Identify states, projects
states=['A','G','R','T','S','P','C']
projects=sorted(list(set(df.iloc[:,4])))
tasks=sorted(list(set(df.iloc[:,5])))

# Aggregate total time on each state
state_times=np.array([sum(df[df.iloc[:,3]==st].iloc[:,2]) for st in states])
overhead_ratio=sum(state_times[0:2])/sum(state_times[0:5])*100.

# Total hours working (excluding consulting time)
hours_academic=sum(df[df.iloc[:,3]!='C'].iloc[:,2])

# Percentage instructional time (T)
perc_teaching=state_times[3]*100./hours_academic

# Percentage service and administrative time (S+A)
perc_service=(state_times[0]+state_times[4])*100./hours_academic

# Percentage business development (P)
perc_bd=state_times[5]*100./hours_academic

# Percentages for each research project (R+G)
perc_proj=[]
for pr in projects:
    hours_proj = sum(df[np.logical_and(df.iloc[:,3]=='R',df.iloc[:,4]==pr)].iloc[:,2])
    hours_proj += sum(df[np.logical_and(df.iloc[:,3]=='G',df.iloc[:,4]==pr)].iloc[:,2])
    if hours_proj < 5:
        perc_proj.append(None)
    else:
        perc_proj.append(hours_proj*100/hours_academic)

perc_research=sum([p for p in perc_proj if p != None])

# Output!
print "Total academic hours: {:.1f}".format(hours_academic)
print "----"
print "Instructional: {:.1f}%".format(perc_teaching)
print "Service and administrative: {:.1f}%".format(perc_service)
print "Proposals and business development: {:.1f}%".format(perc_bd)
print "Named research projects: {:.1f}%".format(perc_research)
print "Other research projects: {:.1f}%".format(100-perc_teaching-perc_service-perc_bd-perc_research)
for i,pr in enumerate(projects):
    if perc_proj[i] != None:
        print " Project '" + pr +"': {:.1f}%".format(perc_proj[i])
