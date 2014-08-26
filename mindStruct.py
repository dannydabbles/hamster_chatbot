#!/usr/bin/python

    ################Import Fields#######################
import random
import sys
from nltk.corpus import wordnet as wn

class Idea:
    ################Data Fields#########################

    word = None
    variations = None
    connections = None

    jumpflag = False

    ################Constructor#########################

    def __init__(self, word, sent):
        word = word.rstrip(".,\';:\"\'?!)")
        word = word.strip("$%&(")
        word = word.lower()
        if not sentdict.has_key(word):
            sentdict[word] = list()
        sentdict[word].append(sent)
        self.word = word
        self.variations = list()
        self.connections = list()
        words.append(self)
        return

    ################Functions###########################

    def add(self, word, sent):
        tptr = find(word)
        temp = None
        if(tptr is None):
            temp = Idea(word, sent)
        else:
            temp = tptr
        self.connections.append(temp)
        return temp

    def addI(self, ide, sent):
        self.connections.append(ide)
        return ide

    def jump(self):
        if(not self.connections): 
            return None
        random.shuffle(self.connections)
        next = iter(self.connections).next()
        if mind.jumpflag is True:
            print "|" + self.word + "|->|" + next.word + "|"
        return next

    def find(self, fword):
        fword = fword.lower()
        fword = fword.rstrip("\n.,!?")
        synlist = list()
        for syn in wn.synsets(fword):
            synlist.extend(syn.lemma_names)
        synlist = list(set(synlist))
        random.shuffle(words)
        for fiword in synlist:
            for s in stoplist:
                if fiword.lower() == s:
                    if fiword in synlist:
                        synlist.remove(fiword)
                    continue
            for w in words:
                if fiword == w.word:
                    return w
        return None

    def printOut_rec(self, curr, depth):
        depth += 1
        if depth > 10:
            return curr.word
        next = self.jump()
        if next is None: 
            return curr.word 
        else: 
            return(curr.word + " " + next.printOut_rec(next, depth))

    def printOut(self, fword):
        temp = self.find(fword.lower())
        if temp is None:
            print "No such word as " + fword
        else:
            print temp.printOut_rec(temp, 0)
        return

    def readIn(self, word1, word2, sent):
        temp1 = None
        for w in words:
            if(w.word == word1):
                temp1 = w
                break
        temp2 = None
        for w in words:
            if(w.word == word2): 
                temp2 = w
                break
        if(temp1 is None):
            temp1 = Idea(word1, sent)
        else:
            flag = False
            for w in sentdict[temp1.word]:
                if w == sent:
                    flag = True
            if not flag:
                sentdict[temp1.word].append(sent)
        if(temp2 is None):
            temp2 = Idea(word2, sent)
        else:
            flag = False
            for w in sentdict[temp2.word]:
                if w == sent:
                    flag = True
            if not flag:
                sentdict[temp2.word].append(sent)
        if(temp1.word == temp2.word): return
        temp1.addI(temp2, sent)
        return

    def readSentence(self, sent):
        sent = sent.rstrip()
        sent = sent.lstrip()
        sent = sent.rstrip("\n.!?")
        wordl = sent.split(' ')
        checker = False
        for w in wordl:
            for s in stoplist:
                if w.lower() == s:
                    wordl.remove(w)
                    checker = True
                    break
            if checker: continue
            loc = wordl.index(w)
            temword = w.lower()
            temword = wordl[loc].rstrip("\,\.\!\?\:\"\'\)\]\-\}\ \\")
            temword = wordl[loc].rstrip("\,\.\!\?\:\"\'\)\(\[\-\{\ \\")
            wordl[loc] = temword

        #print wordl
        for w in wordl:
            for s in stoplist:
                if w.lower() == s:
                    wordl.remove(w)
                    break
        p = None
        for w in wordl:
            if p is None:
                p = w
                continue
            self.readIn(p, w, sent)
            p = w
        return

   ################Data Fields#########################

words = list()
stoplist = ["the",    "be",    "to",    "of",      "and", 
            "a",      "in",    "that",  "have",    "i", 
            "it",     "for",   "not",   "on",      "with", 
            "he",     "as",    "you",   "do",      "at",
            "this",   "but",   "his",   "by",      "from", 
            "they",   "we",    "say",   "her",     "she",
            "or",     "an",    "will",  "my",      "one",
            "all",    "would", "there", "their",   "what",
            "so",     "up",    "out",   "if",      "about", 
            "who",    "get",   "which", "go",      "me",
            "when",   "make",  "can",   "like",    "time",
            "no",     "just",  "him",   "know",    "take",
            "people", "into",  "year",  "your",    "good",
            "some",   "could", "them",  "see",     "other",
            "than",   "then",  "now",   "look",    "only", 
            "come",   "its",   "over",  "think",   "also",
            "back",   "after", "use",   "two",     "how",
            "our",    "work",  "first", "well",    "way",
            "even",   "new",   "want",  "because", "any",
            "these",  "give",  "day",   "most",    "us"
            "is",     "is",    "am",    "are",     "was", 
            "were",   "be",    "being", "been",    "etc.",
            "",
            ]

sentdict = dict()

mind = Idea("","")

    ################Program Main Functions##############

def chooseWord(sent):
    if sent is None:
        return None
    sent = sent.rstrip()
    sent = sent.lstrip()
    sent = sent.rstrip("\n.!?")
    wordl = sent.split(' ')
    while True:
        checker = False
        for w in wordl:
            for s in stoplist:
                if w.lower() == s:
                    wordl.remove(w)
                    checker = True
                    break
            if checker: continue
            loc = wordl.index(w)
            temword = w.lower()
            temword = wordl[loc].rstrip("\,\.\!\?\:\"\'\)\]\-\}\ \\")
            temword = wordl[loc].rstrip("\,\.\!\?\:\"\'\)\(\[\-\{\ \\")
            wordl[loc] = temword
        #print wordl
        for w in wordl:
            for s in stoplist:
                if w.lower() == s:
                    wordl.remove(w)
                    break
        random.shuffle(wordl)
        tester = None
        if len(wordl) != 0:
            tester = wordl[0]
        if tester is None:
            return None
        if mind.find(tester) is None:
            if tester in wordl:
                wordl.remove(tester)
            continue
        else:
            break    
    return wordl[0]    

def getSentence(input):
    if input is None:
        return None
    input = input.rstrip()
    input = input.rstrip("\n.,;:-!?")
    input = input.lstrip()
    inputl = input.lower()
    ide = mind.find(inputl)
    if ide is None:
        #print "The word "+input+" does not exist."
        return None
    else:
        if mind.jumpflag is True:
            print "|"+ide.word+"|"
        random.seed(random.seed())
        rand  = random.randint(0,6)
        if(rand == 0): rand = 0
        elif(rand == 1): rand = 0
        elif(rand == 2): rand = 1
        elif(rand == 3): rand = 1
        elif(rand == 4): rand = 1
        elif(rand == 5): rand = 2
        elif(rand == 6): rand = 2
        if(rand == 0): 
            ide = ide
        if(rand == 1): 
            idet = ide.jump()
            if(idet is not None):
                ide = idet
            else:
                ide = ide
        if(rand == 2): 
            idet = ide.jump()
            if(idet is not None):
                ide = idet
                idet = ide.jump()
                if(idet is not None):
                    ide = idet
                else:
                    ide = ide
            else:
                ide = ide
        #print ide.word 
        random.shuffle(sentdict[ide.word])
        if len(sentdict[ide.word][0]) != 0:
            return sentdict[ide.word][0]
        else:
            return None
    return None

def getKnowledge(input):
    if input is None:
        return None
    input = input.rstrip()
    input = input.rstrip("\n.,:;!?")
    input = input.lstrip()
    inputl = input.lower()
    aword = chooseWord(inputl)
    if aword is not None:
        retword = getSentence(aword)
        return retword
    return None

def loadknow(filename):
    try:
        FILE = open(filename)  #sys.argv[1]
    except IOError:
        print "There is no such file as "+filename
        return
    while True:
        line = FILE.readline()
        line.rstrip(".:;?!\'\"")
        if line == "": break
        #print line
        mind.readSentence(line)
    return

def mindMain():
    loadknow("knowledge.dat")
    while True:
        try:
            input = raw_input("Please give a sentence: ")
        except EOFError:
            print
            break
        input = input.rstrip()
        input = input.rstrip("\n.!?")
        input = input.lstrip()
        inputl = input.lower()
        aword = chooseWord(inputl)
        sent = getSentence(aword)
        if sent is None:
            print "That sentence has nothing I recognize."
            continue
        print sent
    return

    ################Test Code###########################

#print "========================TEST=========================="
loadknow("knowledge.dat")


"""
mind.readSentence("This is cool.")
mind.readSentence("my name is cool bob.")
mind.readSentence("the name of the store is red.")
mind.readSentence("red is my favorite store.")
mind.printOut("this")
mind.printOut("This")
mind.printOut("This")
mind.printOut("name")
mind.printOut("name")
mind.printOut("name")
print sentdict["name"]
print sentdict["cool"]
print sentdict["red"]
print sentdict[""]

def blah():
    while True:
        try:
            input = raw_input("Please give a word: ")
        except EOFError:
            print
            break
        input = input.rstrip()
        input = input.rstrip("\n.!?")
        input = input.lstrip()
        inputl = input.lower()
        ide = mind.find(inputl)
        if ide is None:
            print "The word "+input+" does not exist."
        else:
            random.seed(random.seed())
            rand  = random.randint(0,6)
            if(rand == 0): rand = 0
            elif(rand == 1): rand = 0
            elif(rand == 2): rand = 1
            elif(rand == 3): rand = 1
            elif(rand == 4): rand = 1
            elif(rand == 5): rand = 2
            elif(rand == 6): rand = 2
            if(rand == 0): 
                ide = ide
            if(rand == 1): 
                idet = ide.jump()
                if(idet is not None):
                    ide = idet
                else:
                    ide = ide
            if(rand == 2): 
                idet = ide.jump()
                if(idet is not None):
                    ide = idet
                    idet = ide.jump()
                    if(idet is not None):
                        ide = idet
                    else:
                        ide = ide
                else:
                    ide = ide
        #print ide.word 
            random.shuffle(sentdict[ide.word])
            if len(sentdict[ide.word][0]) != 0:
                print sentdict[ide.word][0]
    return

"""

#Sam's Random Thing:
#--from nltk.corpus import wordnet as wn
