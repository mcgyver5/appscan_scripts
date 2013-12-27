__author__ = 'mcguit1'
#Python script to extract URLS and parameters from cumbersome Appscan Report
import xml.etree.ElementTree as ET
import sys

existingfile = ""
destfile = ""
numargs = len(sys.argv)
if numargs == 3:
    existfile = sys.argv[1]
    destfile = sys.argv[2]
else:
    print ("needs two params: the name of an existing text file and the name of the destination file")
    exit()

f = open(existfile)

count = 0
flist = f.readlines()
f.close()
dest = open(destfile,'w')

for idx, line in enumerate(flist):

    if line.find('URL:') > -1:
        url = flist[idx].strip() + " " + flist[idx+1]
        #urlv = flist[idx +2]
        print flist[idx].strip() + " " + flist[idx+1]

        dest.write(url)
    if line.find('Entity:') > -1:
        entity = flist[idx].strip() + " " + flist[idx+1]
        print flist[idx].strip() + " " + flist[idx+1]
        dest.write(entity)