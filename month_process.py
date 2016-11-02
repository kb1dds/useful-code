#!/bin/python
# Produce monthly plots analyzing time usage
#
# Usage:
#  python month_process.py month
#
# Copyright (c) 2015, Michael Robinson
# Distribution of unaltered copies permitted for noncommercial use only
# All other uses require express permission of the author
# This software comes with no warrantees express or implied

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# load the data 
df=pd.read_csv(sys.argv[1] + ".csv")

# Identify states, projects
states=['A','G','R','T','S','P','C']
stcolors=['r','m','g','c','y','b','k']
projects=sorted(list(set(df.iloc[:,4])))
tasks=sorted(list(set(df.iloc[:,5])))

# Aggregate total time on each state
state_times=np.array([sum(df[df.iloc[:,3]==st].iloc[:,2]) for st in states])
overhead_ratio=sum(state_times[0:2])/sum(state_times[0:5])*100.

plt.figure()
plt.subplot(2,2,1)
plt.title('Time breakdown for ' + sys.argv[1] + ', total: ' +str(sum(df.iloc[:,2]))+ ' hours, overhead ratio: ' + str(int(overhead_ratio)) + '%')
plt.pie(state_times,labels=states,colors=stcolors)

# Stacked bar graph: bars: project, split by state
plt.subplot(2,2,2)
plt.title('Project time breakdown')
totals=np.zeros(len(projects))
for i in range(len(states)):
    st=states[i]
    state_times=np.array([sum(df[np.logical_and(df.iloc[:,3]==st, df.iloc[:,4]==pr)].iloc[:,2]) for pr in projects])
    plt.bar(np.arange(len(projects)),height=state_times,bottom=totals,color=stcolors[i])
    totals+=state_times
plt.xticks(np.arange(len(projects))+0.35,projects,rotation=80)
plt.legend(states)

# state & task

# Compute hours per workday histogram
workdays=[sum(df[df.iloc[:,0]==day].iloc[:,2]) for day in set(df.iloc[:,0])]
plt.subplot(2,2,3)
plt.title('Median workday length: ' + str(int(np.median(workdays)*10)/10.))
plt.hist(workdays)
plt.xlabel('Hours')
plt.ylabel('Frequency')

## Compute hours on email per workday histogram
emailtime=[60*sum(df[np.logical_and(df.iloc[:,5]=='email',df.iloc[:,0]==day)].iloc[:,2]) for day in set(df.iloc[:,0])]
#plt.subplot(2,2,4)
#plt.title('Mean minutes on email: ' + str(int(np.mean(emailtime))))
#plt.hist(emailtime)
#plt.xlabel('Minutes')
#plt.ylabel('Frequency')

# time of day histograms by state
plt.subplot(2,2,4)
start_times=[[int(tm[0:2]) for tm in df[df.iloc[:,3]==st].iloc[:,1]] for st in states]
plt.hist(start_times,color=stcolors,bins=np.arange(24),histtype='bar',stacked=True)
plt.xlabel('Work start times')

print 'Monthly statistics for ' + sys.argv[1]
print 'Total hours: ' + str(sum(df.iloc[:,2]))
print 'Median workday: ' + str(int(np.median(workdays)*10)/10.) + ' hours'
print 'Overhead ratio: ' + str(int(overhead_ratio)) + '%'
print 'Mean minutes on email: ' + str(int(np.mean(emailtime)))

plt.show()
