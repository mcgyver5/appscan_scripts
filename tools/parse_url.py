__author__ = 'mcguit1'
#Python script to extract URLS and parameters from cumbersome Appscan Report
import xml.etree.ElementTree as ET
import sys
import argparse
import mimetypes
import re
import Tkinter, tkFileDialog



def allowed_issue(issue):
    print(str(issue))
    issue = int(issue)
    if issue in [0,1,2,3,4,5]:
        print("is in  0 - 5")
        if issue == 1:
            return "Cross-Site Scripting"
        elif issue == 2:
            return "SQL"
        elif issue == 3:
            return "Privilege"
        elif issue == 4:
            return "Forgery"
        elif issue == 5:
            return "Traversal"
        return "All"
    else:
        msg = "issue must be 0 - 5"
        raise argparse.ArgumentTypeError(msg)


def writeLine(destfile,outformat, issue,url,param):
    sep = ","
    if outformat == 'csv':
        csvString = issue.strip() + sep + url.strip() + sep + param + "\n"
        destfile.write(csvString)
        print(csvString)
    else:

        destfile.write("URL: " + url)
        destfile.write("Parameter: " + param)

def parse_issue(lines):
    pass

def parse_document(existfile, destfile, outformat, issueString):
    #signature:  TEXT ##  followed by blank line followed by TOC = new issue
    #  ISSUE ## of ## followed by TOC = one issue


    try:
        with open(existfile):
            issue = ""
            f = open(existfile)
            finishedLine = False
            flist = f.readlines()
            f.close()
            dest = open(destfile,'w')
            countFileLines = 0
            url = ""
            entity = ""
            backup = 1
            springForward = 1

            for idx, line in enumerate(flist):
                #print("i")
                # match TEXT, three spaces, two digits  followed by blank line followed by TOC
                # match TEXT, three spaces, one or two digits
                patternString = r"[\S]+[ ]+[0-9]?$"
                pattern = re.compile(patternString)

                if pattern.match(line):
                    lineNext = flist[idx+2]
                    if lineNext.find("TOC") > -1:
                        print(line)

    except IOError as e:
        print e
    except TypeError as te:
        print te
    except:
        print("Unexpected error:", sys.exc_info()[0])

def parse_urls(existfile, destfile,outformat,issueString):
    variants = False
    try:
        with open(existfile):
            issue = ""
            f = open(existfile)
            finishedLine = False
            flist = f.readlines()
            f.close()
            dest = open(destfile,'w')
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
                if variants:
                    print("hello variants")

                if finishedLine:
                    #print(issue + " " + issueString)
                    if issueString == 'All' or issue.find(issueString) > -1:
                        writeLine(dest,outformat,issue,url,entity)
                    finishedLine = False

    except IOError as e:
        print e
    except TypeError as te:
        print te
    except:
        print("Unexpected error:", sys.exc_info()[0])


if __name__ == "__main__":
    # this part gets called if called from command line:
    parser = argparse.ArgumentParser(description="hash incoming text")
    parser.add_argument('--file','-f', required=False,help='file name to process')
    parser.add_argument('--dest','-d',default='dest.csv',help='output file name')
    parser.add_argument('--outformat','-o', default='csv',help='output format can be csv or txt default is csv')
    parser.add_argument('--issue','-i', default='0', type=allowed_issue, help='limit output 1 = cross site scripting, 2 = sqli 3 = Privilege Escalation 4 = CSRF 5 = dir traverse')
    args = parser.parse_args()
    # if --file parameter not present, use tkfiledialog to ask for one:
    if args.file == None:
        file = tkFileDialog.askopenfilename(title="SFD")
    else:
        file = args.file

    #parse_document(args.file,args.dest,args.outformat,args.issue)
    parse_urls(file,args.dest,args.outformat,args.issue)