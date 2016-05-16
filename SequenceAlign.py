import tkFileDialog as filedialog
from Tkinter import *
import tkMessageBox
import webbrowser
import random
import sys, traceback
import difflib
from  __builtin__ import any as b_any
from random import randint

FwdSeq = ''
RvSeq = ''
root = Tk()

def GetSeqFiles():
    global FwdSeq;

    global RvSeq;
    
    repeat = True
    while repeat:
        filename = filedialog.askopenfilename()
        
        try:
            fwdopen = open(filename,'r')
            repeat = False
        except:
            result = tkMessageBox.askquestion("Error", "An Error Occurred. Continue with Loading Forward Data? If 'Yes' is selected, please choose the Forward Sequence you want to Align.", icon='warning')
            if result == 'yes':
                repeat = True
            else:
                tkMessageBox.showinfo("Error", "The Program will now close.")
                try:
                    root.destroy()
                except:
                    print "already closed tk"
                    
                sys.exit()


    FwdGET = []           
    for line in fwdopen:
        FwdGET.append(line)

    fwdopen.close()

    repeat = True
    while repeat:
        filename1 = filedialog.askopenfilename()
        
        try:
            revopen = open(filename1,'r')
            repeat = False
        except:
            result = tkMessageBox.askquestion("Error", "An Error Occurred. Continue with Loading Reverse Data? If 'Yes' is selected, please choose the Reverse Sequence you want to Align.", icon='warning')
            if result == 'yes':
                repeat = True
            else:
                tkMessageBox.showinfo("Error", "The Program will now close.")
                try:
                    root.destroy()
                except:
                    print "already closed tk"
                    
                sys.exit()

    RevGET = []
    
    for line1 in revopen:
        RevGET.append(line1)

    revopen.close()
    try:
        root.destroy()
    except:
        print "already closed tk"

    FwdSeq = FwdGET[-1]
    RvSeq = RevGET[-1]

    print "end of file get: " + str(len(RvSeq))


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

def Alignment(template,comparison):
    seqlist = []
    for temp_index, i in enumerate(template):
        for comp_index, j in enumerate(comparison):
            count = 0
            string = ''
            try:
                while template[temp_index + count] == comparison[comp_index + count]:
                    string += template[temp_index + count]
                    count += 1
            except:
                pass
            if len(string) > 1:
                seqlist.append(string)
            
    seqlist = sorted(set(seqlist))
    seqlist.sort(key = len, reverse = True)

    
    FullTemp = []
    for i in seqlist:
        NotFound = True
        for j in seqlist:
            if i in j and i != j:
                NotFound = False
                break
        if NotFound == True:
            FullTemp.append(i)
            
    FullComp = []
    for i in FullTemp:
        x = ReverseOrder(getCompliment(i));
        FullComp.append(x)

    return [FullTemp, FullComp]


def makeHTML(ForwardTotal, ReverseTotal, resultForward, resultReverse):
   
    NewForward = ForwardTotal
    NewReverse = ReverseTotal
    Style = '<style>'
    divID = 1

    print "NewReverse in HTML: " +  str(len(NewReverse))
    if resultForward == []:
        print "Error in file selection. No results found. Please select Forward and Reverse again."
        ProgramFormat()

    if resultReverse == []:
        print "Error in file selection. No results found. Please select Forward and Reverse again."
        ProgramFormat()

    for index in range(0,len(resultForward)):
        divs = 'divID' + str(divID)
        ColorPicker = 'rgba(' + str(randint(0,255)) + ',' + str(randint(0,255)) + ',' + str(randint(0,255)) + ',' + str(0.5) + ')'
        beginSpan = '<span id="' + divs +'" style="border: solid 1px black; background-color: ' + ColorPicker + ';">';
        endSpan = '</span>';

        Style += '#' + divs + ':hover{color: yellow;}'
        NewForward = NewForward.replace(resultForward[index],beginSpan + resultForward[index] + endSpan)
        NewReverse = NewReverse.replace(resultReverse[index],beginSpan + resultReverse[index] + endSpan)

        FwdStartNum = NewForward.find(resultForward[-1])
        RevStartNum = NewReverse.find(resultReverse[-1])

        divID += 1
   
    Style +='</style>'

    num = 0.0
    deno = 0.0
    for i in resultForward[-1]:
        if i =='C' or i == 'G':
            num += 1;
        deno += 1;

    
    GCRatio = round((num/deno)*100,2)
    
    
    file = open('Results.html','w')
    file.write('<html><body style="padding: 0px 10px;">')
    file.write(Style)
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

    file.write('<ul>')
    file.write('<li><div style="font-size:larger;display:block;padding:5px;">Length of Aligned Segment: <b>')
    file.write(str(len(resultForward[-1])))
    
    file.write('</b> bp</div></li>')
    
    file.write('<li><div style="font-size:larger;display:block;padding:5px;">G-C Ratio of Aligned Segment: <b>')
    file.write(str(GCRatio))
    file.write('</b> %</div></li>')
    file.write('</ul>')
    
    file.write('<div style="font-size:larger;display:block;padding:5px;color:green;"><b>Longest Forward</b><div>')
    file.write(resultForward[-1])
    file.write('</div></div>')
    file.write('<div style="font-size:larger;display:block;padding:5px;color:green;"><b>Longest Reverse</b><div>')
    file.write(resultReverse[-1])
    file.write('</div></div>')
    file.write('</body></html>')

    file.close()



def ProgramFormat():
    GetSeqFiles()
                   
    theComp = getCompliment(RvSeq);
    RvCompFlipped = ReverseOrder(theComp);

    Alignment(FwdSeq, RvCompFlipped)
    
    ForwardResults, ReverseResults = Alignment(FwdSeq,RvCompFlipped)

    makeHTML(FwdSeq,RvSeq,ForwardResults,ReverseResults)
    url = "Results.html"
    webbrowser.open(url, new=2)
    
    sys.exit()
    
#---------------------------------------------------------------------------

ProgramFormat()
