__author__ = 'mcguit1'
#Python script to extract URLS and parameters from cumbersome Appscan Report
import xml.etree.ElementTree as ET
import sys
import argparse
import mimetypes



def writeLine(destfile,outformat, issue,url,param):
    sep = ","
    if outformat == 'csv':
        csvString = issue.strip() + sep + url.strip() + sep + param + "\n"
        destfile.write(csvString)
        print(csvString)
    else:

        destfile.write("URL: " + url)
        destfile.write("Parameter: " + param)

def parse_urls(existfile, destfile,outformat):
    # if it says TOC and then issue, get the issue behind it (idx -1)
    # if it says TOC and then something else, ignore the something else.
    print("trying " + existfile)
    try:
        with open(existfile):
            issue = ""
            f = open(existfile)
            finishedLine = False
            flist = f.readlines()
            f.close()
            dest = open(destfile,'w')

            countUrl = 0
            countFileLines = 0
            url = ""
            entity = ""
            backup = 1
            springForward = 1
            for idx, line in enumerate(flist):
               # print(8)
                countFileLines = countFileLines + 1

                if line.find('TOC') > -1:
                    #print(9)

                    nextLine = flist[idx + 1]
                    #correct for differences in format:
                    if nextLine.strip() == "":
                        nextLine = flist[idx+3]
                        backup = 2
                        springForward = 2
                    if nextLine.find('Issue') > -1:
                        issue = flist[idx - backup]
                        # break issue:
                        rinx = issue.rfind(" ")
                        issue = issue[0:rinx]
                        #issue = issueParts[0]


                if line.find('URL:') > -1:

                    url = flist[idx+springForward]

                if line.find('Entity:') > -1:

                    entity = flist[idx+springForward]
                    finishedLine = True
                    entityParts = entity.split()
                    entity = entityParts[0]
                    spare = entityParts[1]

                if finishedLine:
                    writeLine(dest,outformat,issue,url,entity)
                    finishedLine = False

    except IOError as e:
        print e
    except TypeError as te:
        print te
    except:
        print("Unexpected error:", sys.exc_info()[0])


if __name__ == "__main__":
    # this part only works if called from command line:
    print("appscan sucks!!!")
    parser = argparse.ArgumentParser(description="hash incoming text")
    parser.add_argument('--file','-f', required=True)
    parser.add_argument('--dest','-d',default='dest.csv')
    parser.add_argument('--outformat','-o', default='csv')
    args = parser.parse_args()

    parse_urls(args.file,args.dest,args.outformat)