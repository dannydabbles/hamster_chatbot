#!/usr/bin/python

########Imports################################
   ########System Stuff###########################
import random
import sys
import getopt
from nltk.corpus import wordnet as wn
from time import strftime as datetime

   ########Our Stuff##############################
from output import *
from lexicon import *
from mindStruct import *
from aggroMgr import *
from inputs import *

########Global Variables#######################
senttypes = []

   ########Options################################

      ########Option Flags###########################
#jumpflag
userkbflag = False
userkb = None
angerflag = False

      ########Option Code############################
optlist, args = getopt.getopt(sys.argv[1:], 'jak:')
for opt in optlist:
    if opt[0] == "-j":
        print "jumpflag on"
        mind.jumpflag = True
    if opt[0] == "-a":
        print "angerflag on"
        angerflag = True
    if opt[0] == "-k":
        print "userkbflag on"
        userkbflag = True
        userkb = opt[1]

########Main Function##########################
def main():    

    if userkbflag is True:
        loadknow(userkb)

    filename = datetime('%y%m%d%H%M%S') + '.log'
    try:
        log = open(filename,'w')

        angerlvl = aggro.query()
        angerlvlprev = angerlvl
        
      ### main while loop ###
        while True: #=D =) =| =( D=
            
            try:
                input = None
                if angerlvl in range(0,2):
                    input = raw_input("What have you to say?: ")
                elif angerlvl in range(2,4):
                    input = raw_input("What do you want?: ")
                elif angerlvl in range(4,6):
                    input = raw_input("YOU ARE NOT A HAMSTER!!!: ")
                else:
                    print "THE UNIVERSE HAS BROKEN!!!!!!!!!"
            except EOFError:
                aggro.stop()
                print '\n\t'+filename, 'created.'
                break

         # after getting input
            log.write('\n> ' + input)

            infoset = inputs(input)
            #print infoset
            aggro.shift(infoset)
            angerlvlprev = angerlvl
            angerlvl = aggro.query()
            if angerflag is True:
                print "Current anger level is: " + angerlvl.__str__()
        
            sent = getKnowledge(input)

            outsent = None

            senttype = infoset[2]

            if senttype is 'reflex':
                outsent = chooseOut(infoset, angerlvl, angerlvlprev, sent)
            elif senttype is 'know':
                if sent is not None:
                    outsent = Sentence('know', angerlvl, sent).__str__() + "  "
                else:
                    outsent = "I don't know anything about "+input+"."
            else:
                if senttype == 'empty':
                    outsent = "...?"
                else:
                    outsent = Sentence(senttype, angerlvl).__str__()
                

            # after printing output
            log.write('\n(anger level: ' + repr(angerlvl) + ') ' + outsent)
            
            print outsent
    except IOError:
        print filename + ': could not open file to write'
    log.close()
    return

########Bot Functions##########################
def chooseOut(infoset, angerlvl, angerlvlprev, sent):
    outsent = ""

    if angerlvl in range(0,2):
        outsent = magic(angerlvl, angerlvlprev, sent, infoset, 5, 4, 5, 3, 6)
    elif angerlvl in range(2,4):
        outsent = magic(angerlvl, angerlvlprev, sent, infoset, 4, 6, 3, 6, 5)
    elif angerlvl in range(4,6):
        outsent = magic(angerlvl, angerlvlprev, sent, infoset, 0, 7, 0, 14, 7)
    return outsent

def magic(angerlvl, angerlvlprev, sent, infoset, a, b, c, d, e):
    outsent = ""
    numtime = 13
    randl = [0,#knowledge
             0,#feeling
             0 #reflex
             ]
    #
    for i in range(numtime):
        ind = random.randint(0, 2)
        randl[ind] += 1

    if angerlvl != angerlvlprev:
        outsent += Sentence('feel', angerlvl).__str__() + "  "

    if sent is None:
        if randl[1] >= a:
            outsent += Sentence('reflex', angerlvl, infoset[0].rstrip(".!?")).__str__() + "  "
        elif randl[2] >= b:
            outsent += Sentence('reflex', angerlvl, infoset[0].rstrip(".!?")).__str__() + "  "
        if outsent == "":
            outsent += Sentence('reflex', angerlvl, infoset[0].rstrip(".!?")).__str__() + "  "
    else:
        if randl[1] >= c:
            if random.randint(0, 1) == 0:
                outsent += Sentence('reflex', angerlvl, infoset[0].rstrip(".!?")).__str__() + "  "
            else:
                outsent += Sentence('know', angerlvl, sent).__str__() + "  "
        elif randl[0] >= d:
            outsent += Sentence('know', angerlvl, sent).__str__() + "  "
        elif randl[2] >= e:
            outsent += Sentence('reflex', angerlvl, infoset[0].rstrip(".!?")).__str__() + "  "
        if outsent == "":
            outsent += Sentence('reflex', angerlvl, infoset[0].rstrip(".!?")).__str__() + "  "
    return outsent

########Script Stuff###########################
print "Hello, my name is Harvey. I'm kind of shy.\n"+"I love hamsters, but I don't like talking about myself.\n"+"Let's have a conversation!"
main()
