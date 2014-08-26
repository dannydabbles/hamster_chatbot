#!/usr/bin/env python

from string import upper


####LEXICAL OBJECTS#######
class Greet(object):
    "Greetings which will display alone"
    
    def __init__(self, lex=None, semtype=None, syntype = 'greet'):
        self.lex = lex
        self.semtype = semtype
        self.syntype = syntype
        
    def __str__(self):
        return self.lex

class Det(object):
    "Determiners"
    
    def __init__(self, lex=None, semtype=None, dettype=None, case=None, subcatsyn=None, agr=None, syntype='det'):
        self.lex = lex
        self.semtype = semtype
        self.syntype = syntype
        self.dettype = dettype
        self.case = case
        self.subcatsyn = subcatsyn
        self.agr = agr
    
    def upper(self):
        return self.lex.upper
 
    
    def __str__(self):
        return self.lex

class Noun(object):
    "Nouns"
    
    def __init__(self, lex=None, semtype=None, syntype='noun', dettype=None, angerlev=None,
                 case=None, subcat=None):
        self.lex = lex
        self.semtype = semtype
        self.syntype = syntype
        self.dettype = dettype
        self.angerlev = angerlev
        self.case = case
        self.subcat = subcat
 
    
    def __str__(self):
        return self.lex
    

class Adjective(object):
    "Adjectives"
    
    def __init__(self, lex=None, semtype=None, angerlev=None, subcat=None,syntype='adj'):
        self.lex = lex
        self.semtype = semtype
        self.syntype = syntype
        self.angerlev = angerlev
        self.subcat = subcat
 
    
    def __str__(self):
        return self.lex

class Verb(object):
    """verbs - assumes regular verb. Irregular ones like 'to be' need to be marked
    irregular in morph for agreement. Morphology is handled by a list."""
    def __init__(self, lex, angerlev=None, semtype=None, subcatsem=None, subcatsyn=None,syntype='verb', morph='regular'):
        self.lex= lex
        self.semtype = semtype
        self.syntype = syntype
        self.subcatsyn = subcatsyn
        self.subcatsem = subcatsem
        self.morph = morph
        self.angerlev = angerlev
        
    def __str__(self):
        return self.lex

class Fact(object):
    "Facts. They totally cheat and are treated like strings."
    
    def __init__(self, lex=None, semtype=None, syntype='fact',subcat=None):
        self.lex = lex
        self.semtype = semtype
        self.syntype = syntype
        self.subcat = subcat
 
    
    def __str__(self):
        return self.lex
    
#####LEXICON###########################################

d = [Det('I', 'self', 'pronoun', 'nom', 'nothing', agr=('1sg')),\
    Det('the', 'def', dettype='def', subcatsyn='np')]

#Adjectives are stored in a dictionary keyed to anger level.
adj= {0:[Adjective('fine', 'feeling', angerlev=0),\
         Adjective('ok', 'feeling', angerlev=0), \
         Adjective('good', 'feeling', angerlev=0)],\
    1:[Adjective('mildly angry', 'feeling', angerlev=1),\
     Adjective('mad', 'feeling', angerlev=1),\
     Adjective('upset', 'feeling', angerlev=1)],\
    2:[Adjective('irate', 'feeling', angerlev=2),\
     Adjective('rage-filled', 'feeling', angerlev=2),\
     Adjective('furious', 'feeling', angerlev=2),\
     Adjective('choleric', 'feeling', angerlev=2),\
     Adjective('maddened', 'feeling', angerlev=2)],\
    3:[Adjective('fuming', 'feeling', angerlev=3),\
     Adjective('storming', 'feeling', angerlev=3),\
     Adjective('frenzied', 'feeling', angerlev=3),\
     Adjective('rabid', 'feeling', angerlev=3)],
    4:[Adjective('wrathful', 'feeling', angerlev=4),\
    Adjective('livid', 'feeling', angerlev=4),\
    Adjective('outraged', 'feeling', angerlev=4),\
    Adjective('seething', 'feeling', angerlev=4)],\
    5:[Adjective('berserk', 'feeling', angerlev=5),\
     Adjective('maniacal', 'feeling', angerlev=5),\
     Adjective('hysterical', 'feeling', angerlev=5),\
     Adjective('violent', 'feeling', angerlev=5),\
     Adjective('pissed off', 'feeling', angerlev=5)]}

#nouns are only for feeling so they are in a dict keyed to anger level
n = {0:[Noun('fine', 'feeling', angerlev=0),\
    Noun('good', 'feeling', angerlev=0),\
    Noun('ok', 'feeling', angerlev=0)],\
    1:[Noun('angry', 'feeling', angerlev=1),\
    Noun('annoyance', 'feeling', angerlev=1)],\
    2:[Noun('vexation', 'feeling', angerlev=2),\
    Noun('hatred', 'feeling', angerlev=2),\
    Noun('fury', 'feeling', angerlev=2),\
    Noun('mad', 'feeling', angerlev=2)],
    3:[Noun('fuming', 'feeling', angerlev=3),\
    Noun('frenzied', 'feeling', angerlev=3),\
    Noun('rabid', 'feeling', angerlev=3)],\
    4:[Noun('wrathful', 'feeling', angerlev=4),\
    Noun('outrage', 'feeling', angerlev=4)],\
    5:[Noun('maniacal', 'feeling', angerlev=5),\
    Noun('hysterical', 'feeling', angerlev=5),\
    Noun('hysteria', 'feeling', dettype='def', angerlev=5),\
    Noun('violence', 'feeling', angerlev=5),\
    Noun('rage', 'feeling', dettype='def', angerlev=5)]}

#verbs are in a dict keyed to sem value
v = {'feel':[Verb(['feel', 'feels', 'felt', 'felt', 'feeling'],'feel', subcatsem='feeling', subcatsyn='np'),\
        Verb(['grow', 'grows', 'grew', 'grown', 'growing'],'feel', subcatsem='feeling', subcatsyn='adjp'),\
        Verb(['am', 'is', 'was', 'been','being', 'are', 'were'], 'feel', subcatsem='feeling', subcatsyn='adjp')],\
    'know':[Verb(['know', 'knows', 'knew', 'known', 'knowing'], 'know', subcatsem='fact', subcatsyn='cp'),\
            Verb(['believe', 'believes', 'believed', 'believed', 'believing'], 'know', subcatsem='fact', subcatsyn='cp'), \
            Verb(['fancy', 'fancies', 'fancied', 'fancied', 'fancying'], 'know', subcatsem='fact', subcatsyn='cp'),\
            Verb(['reckon', 'reckons', 'reckoned', 'reckoned', 'reckoning'], 'know', subcatsem='fact', subcatsyn='cp')]}

f = [Fact("hamsters are furry", 'furry'),\
     Fact("hamster tails are stubby", 'tail'),\
    Fact("I like hamsters a lot", 'like')]

g = {0:[Greet("Hello! :\)"),
     Greet("Hi!"),
     Greet("Oh, hello there!")],
    1:[Greet("Hello."),
        Greet("Greetings."),
        Greet("Salutations.")],
    2:[Greet("Hey."),
       Greet("Hello."),
       Greet("Oh, hey.")],
    3:[Greet("Oh, it's you."),
       Greet("What do you want?"),
       Greet("*sigh*")],
    4:[Greet("What? Are you talking to me??"),
       Greet("Whatever."),
       Greet("What do you want?")],
    5:[Greet("WHAT DO YOU WANT?!"),
       Greet("GO AWAY!!!!"),
       Greet("WHY ARE YOU TALKING TO ME?!!")]}