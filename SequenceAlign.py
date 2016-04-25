import tkFileDialog as filedialog
from Tkinter import *
import webbrowser
import random

FwdSeq = ''
RvSeq = ''

def GetSeqFiles():
    global FwdSeq;
    global RvSeq;
    root = Tk()
    filename = filedialog.askopenfilename()
    FwdGET = []
    fwdopen = open(filename,'r')
    for line in fwdopen:
        FwdGET.append(line)

    fwdopen.close()

    filename = filedialog.askopenfilename()
    RevGET = []
    revopen = open(filename,'r')
    for line in revopen:
        RevGET.append(line)

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
    top10Temp = templateArray[-10:]
    compBeforeUnfixed = comparisonArray[-10:]
    top10Temp.reverse()
    compBeforeUnfixed.reverse()
    #topTemp = top10Temp
    #TopCompBefore = compBeforeUnfixed

    #'''

    dontadd = False
    topTemp = []
    TopCompBefore = []
    for i in top10Temp:
        for j in top10Temp:
            if i in j and i != j:
                if len(j) > len(i):
                    dontadd = True
        if dontadd == False:
            topTemp.append(i);
        else:
            dontadd = False;

    for i in compBeforeUnfixed:
        for j in compBeforeUnfixed:
            if i in j and i != j:
                if len(j) > len(i):
                    dontadd = True
        if dontadd == False:
            TopCompBefore.append(i);
        else:
            dontadd = False;
     #'''
    topComp = []
    for i in TopCompBefore:
        #print "starting with " + i;
        compComp = getCompliment(i);
        revComp = ReverseOrder(compComp);
        #print "now we have " + revComp
        topComp.append(revComp);
    
    topTemp.sort(key = len)
    topComp.sort(key = len)
    
    return [topTemp, topComp]


def makeHTML(ForwardTotal, ReverseTotal, resultForward, resultReverse):

    ColorPicker = ['yellow','burlywood','lightcoral','green','orange','lightgreen','lightsteelblue','lightblue','pink']
    NewForward = ForwardTotal
    NewReverse = ReverseTotal

  
    
    for index, i in enumerate(resultForward):
        num = index
    
        FwdStartNum = NewForward.find(resultForward[num])
        FwdEndNum = len(resultForward[num]) + FwdStartNum
        beginSpan = '<span style="border: solid 1px black; background-color: ' + random.choice(ColorPicker) + ';">';
        endSpan = '</span>';
        NewForward = NewForward[0:FwdStartNum] + beginSpan + resultForward[num] + endSpan + NewForward[FwdEndNum:len(NewForward)];

    for index, i in enumerate(resultReverse):
        num = index

        RevStartNum = NewReverse.find(resultReverse[num])
        RevEndNum = len(resultReverse[num]) + RevStartNum
        beginSpan = '<span style="border: solid 1px black; background-color: ' + random.choice(ColorPicker) + ';">';
        endSpan = '</span>';
        NewReverse = NewReverse[0:RevStartNum] + beginSpan + resultReverse[num] + endSpan + NewReverse[RevEndNum:len(NewReverse)];


    

    num = 0.0
    deno = 0.0
    for i in resultForward[-1]:
        if i =='C' or i == 'G':
            num += 1;
        deno += 1;

    
    GCRatio = round((num/deno)*100,2)
            
    
    file = open('Results.html','w')
    file.write('<html><body style="padding: 0px 10px;">')
    file.write('<div style="border: solid 1px;padding: 5px; word-wrap:break-word;background-color:#F3EDED;margin:10px;"> <h1>Forward Sequence: </h1>')
    file.write('<div style="font-size:larger;display:block;padding:5px;">')
    file.write(NewForward)
    file.write('</div>')
    file.write('<div style="font-size:larger;display:block;padding:5px;">Alignment Starts on: <b>')
    file.write(str(FwdStartNum))
    file.write('</b> bp</div>')
    file.write('</div>')
    file.write('<div style="border: solid 1px;padding: 5px; word-wrap:break-word;background-color:#F3EDED;margin:10px;"> <h1>Reverse Sequence: </h1>')
    file.write(ReverseTotal)
    file.write('<div style="font-size:larger;display:block;padding:5px;">')
    file.write(NewReverse)
    file.write('</div>')
    file.write('<div style="font-size:larger;display:block;padding:5px;">Alignment Starts on: <b>')
    file.write(str(RevStartNum))
    file.write('</b> bp</div>')
    file.write('</div>')

    file.write('<ul>')
    file.write('<li><div style="font-size:larger;display:block;padding:5px;">Length of Aligned Segment: <b>')
    file.write(str(len(resultForward[-1])))
    
    file.write('</b> bp</div></li>')
    
    file.write('<li><div style="font-size:larger;display:block;padding:5px;">G-C Ratio of Aligned Segment: <b>')
    file.write(str(GCRatio))
    file.write('</b> %</div></li>')
    file.write('</ul>')
    
    file.write('<div style="font-size:larger;display:block;padding:5px;color:green;">')
    file.write(resultForward[-1])
    file.write('</div>')
    file.write('<div style="font-size:larger;display:block;padding:5px;color:green;">')
    file.write(resultReverse[-1])
    file.write('</div>')
    file.write('</body></html>')

    file.close()

#---------------------------------------------------------------------------

GetSeqFiles()
               
theComp = getCompliment(RvSeq);
RvCompFlipped = ReverseOrder(theComp);

ForwardResults, ReverseResults = Alignment(FwdSeq,RvCompFlipped)



makeHTML(FwdSeq,RvSeq,ForwardResults,ReverseResults)



url = "Results.html"
webbrowser.open(url, new=2)


sys.exit()
