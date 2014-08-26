#!/usr/bin/env python

import random
from string import upper

import lexicon
#######HELPERS###############################

def cleanprint(subjdp, verbp, anger):
    "for formatting output"
    puncdic = {0:".", 1:".", 2:"!", 3:"!!", 4:"!!!", 5:"!!!!"}
    return "%s %s%s" % (str(subjdp),
                      " ".join(verbp),
                      puncdic[anger])
    
def lexpicker(lexitem, lexindex):
    "Picks a lexeme from a dict"
    l = len(lexitem[lexindex])-1
    r = random.randint(0,l)
    return lexitem[lexindex][r]


########GRAMMAR OBJECTS######################

def vp(v, agr, objsem, tense, angerlev, fact):
    "assemble a verb phrase"
    if v.subcatsyn=='np':
        ind = agreement(agr, tense, v.morph)
        comp = lexpicker(lexicon.n, angerlev)
        return v.lex[ind], np(comp, v.subcatsem).lex
    elif v.subcatsyn=='adjp':
        ind = agreement(agr, tense, v.morph)
        comp = lexpicker(lexicon.adj, angerlev)
        return v.lex[ind], adjp(comp, v.subcatsem).lex
    elif v.subcatsyn=='cp':
        ind = agreement(agr, tense, v.morph)
        return v.lex[ind] + " that",fact
    elif v.subcatsyn=='none':
        ind = agreement(agr, tense, v.morph)
        return v.lex[ind]


def agreement(agr, tense, morph):
    "the different morphological forms of verbs are in a list. This sets up agreement by matching agr to list indice"
    if morph == 'regular':
        if agr == '1sg' and tense=='pres':
            return 0
        elif agr == '3sg' and tense=='pres':
            return 1
        elif tense=='past':
            return 2
        elif agr == '1pl' and tense =='pres':
            return 0
        elif agr == 'ing':
            return 4
    elif morph == 'irregular':
        if agr == '1sg' and tense=='pres':
            return 0
        elif agr == '3sg' and tense=='pres':
            return 1
        elif tense=='past':
            return 2
        elif agr == '1pl' and tense =='pres':
            return 5

def dp(d, semtype, case):
    "Determiner Phrase:Assembles an np based on vp args and syn requirements."
    for lex in d:
        if lex.case == case and lex.semtype == semtype:
            return lex


def np(n, semtype):   
     if n.semtype == semtype:
         return n

def adjp(adj, semtype):
    "Assembles an adjp based on vp args and syn requirements."
    if adj.semtype == semtype:
        return adj

def cp(fact, semtype):
    "Picks a fact based on vp args and syn requirements. -was for testing"
    for lex in fact:
     if lex.semtype == semtype:
         return lex

def build(Sentence):
    if Sentence.action == 'feel' or Sentence.action == 'know':
        verb = lexpicker(lexicon.v, Sentence.action)  
        subjdp = dp(lexicon.d,Sentence.subj,case='nom')
        verbp = vp(verb, subjdp.agr, Sentence.objsem,
               Sentence.tense, Sentence.anger, Sentence.fact)
        return cleanprint(subjdp, verbp, Sentence.anger)
    elif Sentence.action == 'reflex':
        #I will key these to aggro and move them to lexicon file
        responses = ["I don't care about " +"\"" + Sentence.fact + "\".",
                     "Oh, "+ "\"" + Sentence.fact + "\"" " is irrelevant to me.",
                     "\""+Sentence.fact+"\"" + " is really not interesting to me.",
                     "You speak of trivial things.",
                     "LOL. That's all I have to say about that.",
                     "Uh-huh. That's nice.",
                     "\""+Sentence.fact+"\""+ " is stupid. Why would anyone talk about that?"]
        reslen = len(responses)-1
        ind = random.randint(0, reslen)
        return responses[ind]
    elif Sentence.action == 'greeting':
        return greet(Sentence)
    elif Sentence.action == 'safe':
        return "I suddenly feel great! :D"
    elif Sentence.action == 'enrage':
        return "YOU WOULDN'T LIKE ME WHEN I'M ANGRY!!!!!"

def reflex(Sentence):
    pass

def greet(Sentence):
    greeting = lexpicker(lexicon.g, Sentence.anger)
    return greeting.lex
        

class Sentence(object):
    "this will eventually scale to do imperatives and questions. just not yet"
    def __init__(self,action, anger, fact=None, objsem=None, subj='self', type='dec', tense = 'pres'):
        self.type = type
        self.tense = tense
        self.subj = subj
        self.fact = fact
        self.action = action
        self.objsem = objsem
        self.anger = anger

    def __str__(self):
            return build(self)
        

            




def main():
    pass
 
if __name__=="__main__":
    main()
 
 