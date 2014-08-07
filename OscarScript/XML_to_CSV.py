#! /usr/bin/env python

import re
p1=re.compile('\<detection\ (.*)\ \/\>')
p2=re.compile('[0-9]*\.?[0-9]*')
result=[]
counter=-1
with open('Tracked_TracksOnly.xml') as f:
    lines=f.readlines()
    for line in lines:
        if 'detection' in line:
            _temp=filter(None, p2.findall(p1.findall(line)[0]))
            if _temp[0]=='0':
                counter+=1
            result.append(str(counter)+','+','.join(_temp[:-1]))
with open('Processed_XML_FlyTracker.csv', 'w') as f:
    print>>f, 'ID,t,x,y'
    for item in result:
        print>>f, item