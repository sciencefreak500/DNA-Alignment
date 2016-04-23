import tkFileDialog as filedialog
from Tkinter import *
import sys
import time

root = Tk()
filename = filedialog.askopenfilename()
FwdGET = []
fwdopen = open(filename,'r')
for line in fwdopen:
    FwdGET.append(line)
    print line
fwdopen.close()

filename = filedialog.askopenfilename()
RevGET = []
revopen = open(filename,'r')
for line in revopen:
    RevGET.append(line)
    print line
fwdopen.close()
root.destroy()

FwdSeq = FwdGET[-1]
RvSeq = RevGET[-1]

#test sequence
#FwdSeq = "ATGCGCAAATTGGCCGCGGGGATTAGTCGAGAGATCCTCGATCCCCCGCGATTAGACTGATCGAGCGCTATCCGAGTCAGCTATC"
#RvSeq =  "GATAGCTGACTCGGATAGCGCTCGATCAGTCTAATCGCGGGGGATCGAGGATCTCTCGACTAATCCCCGCGGCCAATTTGCGCAT"
#RvSeq =  "GCTGACTCGGAGGAGCTGACTCGGATAGCTCGGGAGCTGACTCGGGAGCTGACTCGGATAGTCGCGGGG"

#Step 1: Read in Forward and Reverse to strings
#Step 2: Get Compliment of Reverse -- DONE
#Step 3: Get Reverse Order of Reverse Compliment --DONE
#Step 4: Align to Forward, check for overlap



#gets the compliment strand
def getCompliment(ForwardSeq):
    Compliment = '';
    for i in ForwardSeq:
        if i == 'A':
            Compliment+='T';
        elif i == 'T':
            Compliment+='A';
        elif i == 'G':
            Compliment+='C';
        else:
            Compliment+='G';
    return Compliment;

#flips order of sequence (from 3->5, to 5->3)
def ReverseOrder(strand):
    return strand[::-1]



def Alignment(template, comparison):
    allignArray = [];
    first = 0
    second = 0
    templateArray = []
    comparisonArray = []
    for t_index,t_char in enumerate(template):
        for c_index,c_char in enumerate(comparison):
            if t_char == c_char:
                #print "t_vs_c: " + str(t_index) + ":" + str(c_index)
                count = 1
                if t_index + count == len(template):
                    first = len(template)-1
                else:
                    first = t_index + count;
                #print first
                if c_index + count == len(comparison):
                    second = len(comparison)-1
                else:
                    second = c_index + count;
                #print second
                while first < len(template) or second < len(comparison):
                    if template[first] == comparison[second]:
                        #print str(first) + ":" + str(second)
                        if(first == len(template)-1 or second == len(comparison)-1):
                            #print "breaking on the 84"
                            allignArray.append([template[t_index:first+1],comparison[c_index:second+1]])
                            break;
                        else:
                            count+= 1;
                        if t_index + count == len(template):
                            first = len(template)-1
                        else:
                            first = t_index + count;
                        if c_index + count == len(comparison):
                            second = len(comparison)-1
                        else:
                            second = c_index + count;
                    else:
                        #print "breaking at the equal compare"
                        allignArray.append([template[t_index:first],comparison[c_index:second]])
                        break



    for i in allignArray:
        var1, var2 = i
        templateArray.append(var1)
        comparisonArray.append(var2)

    
    templateArray.sort(key = len)
    comparisonArray.sort(key = len)
    top5Temp = templateArray[-5:]
    compBefore = comparisonArray[-5:]
    
    top5Comp = []
    for i in compBefore:
        #print "starting with " + i;
        compComp = getCompliment(i);
        revComp = ReverseOrder(compComp);
        #print "now we have " + revComp
        top5Comp.append(revComp);

    return [top5Temp, top5Comp]


def makeHTML(ForwardTotal, ReverseTotal, resultForward, resultReverse):
    FwdStartNum = ForwardTotal.find(resultForward[-1])
    FwdEndNum = len(resultForward[-1]) + FwdStartNum
    beginSpan = '<span style="border: solid 1px black; background-color: yellow;">';
    endSpan = '</span>';
    NewForward = ForwardTotal[0:FwdStartNum] + beginSpan + resultForward[-1] + endSpan + ForwardTotal[FwdEndNum:len(ForwardTotal)];

    RevStartNum = ReverseTotal.find(resultReverse[-1])
    RevEndNum = len(resultReverse[-1:]) + RevStartNum
    beginSpan = '<span style="border: solid 1px black; background-color: yellow;">';
    endSpan = '</span>';
    NewReverse = ReverseTotal[0:RevStartNum] + beginSpan + resultReverse[-1] + endSpan + ReverseTotal[RevEndNum:len(ReverseTotal)];
    
    file = open('Results.html','w')
    file.write('<html><body>')
    file.write('<div style="border: solid 1px;padding: 5px; word-wrap:break-word;background-color:#F3EDED;margin:10px;"> <h1>Forward Sequence: </h1>')
    file.write('<div style="font-size:larger;display:block;padding:5px;">')
    file.write(NewForward)
    file.write('</div>')
    file.write('<div style="font-size:larger;display:block;padding:5px;">Alignment Starts on: <b>')
    file.write(str(FwdStartNum))
    file.write('</b> bp</div>')
    file.write('</div>')
    file.write('<div style="border: solid 1px;padding: 5px; word-wrap:break-word;background-color:#F3EDED;margin:10px;"> <h1>Reverse Sequence: </h1>')
    file.write('<div style="font-size:larger;display:block;padding:5px;">')
    file.write(NewReverse)
    file.write('</div>')
    file.write('<div style="font-size:larger;display:block;padding:5px;">Alignment Starts on: <b>')
    file.write(str(RevStartNum))
    file.write('</b> bp</div>')
    file.write('</div>')
    file.write('<div style="font-size:larger;display:block;padding:5px;color:green;">')
    file.write(resultForward[-1])
    file.write('</div>')
    file.write('<div style="font-size:larger;display:block;padding:5px;color:green;">')
    file.write(resultReverse[-1])
    file.write('</div>')
    file.write('</body></html>')

    file.close()

#---------------------------------------------------------------------------
               
theComp = getCompliment(RvSeq);
RvCompFlipped = ReverseOrder(theComp);


ForwardResults, ReverseResults = Alignment(FwdSeq,RvCompFlipped)

print ForwardResults[-1:]
print ReverseResults[-1:]

makeHTML(FwdSeq,RvSeq,ForwardResults,ReverseResults)



sys.exit()
