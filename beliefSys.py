#!/user/bin/python

from nltk.corpus import wordnet as wn

# helper function
def separate(string, morph=False):
   """
   returns list of space separated words
   gets rid of (most) punctuation
   if the optional morph bool is True, it
   turns each word into its singular form
   through the use of nltk.corpus.wordnet.morphy
   """
   #from nltk.corpus import wordnet as wn # hangs on load
   import re
   punct = '[ ,.?!;:\"\(\)\\n]'
   wdlist = re.split(punct, string.lower())
   while '' in wdlist: # get rid of empty elements
      wdlist.remove('')
   ##print wdlist
   if morph:
      morphy = wn.morphy
      for i in xrange(len(wdlist)):
         tmp = morphy(wdlist[i])
         if tmp is not None:
            wdlist[i] = tmp
   return wdlist
   
# string should be repr(wn.synsets('word')[n])
def getPOS(string):
   # should be 'n','a','v',...
   return re.split('[.]', string)[1]

# this function is not very useful...
def replaceUnderscores(list):
   """
   replaces underscores in the passed in list
   with spaces
   """
   import re
   for i in xrange(len(list)):
      if '_' in list[i]:
         list[i] = re.sub('[_]', ' ', list[i])

def addUnderscores(sublist):
   """
   worker function for checkForPhrases
   strings along words with '_' and appends
   them to a list as it does so.
   returns the list with '_' joined strings
   """
   possible = []
   string = sublist[0]
   for i in xrange(len(sublist)-1):
      string += '_' + sublist[i+1]
      possible.append( string )
   return possible
      
# takes a while the first time it's called
def checkForPhrases(list):
   """
   checks for phrases in wordnet by looking
   at the synsets of adjacent words in the list 
   with '_' between them instead of spaces
   returns a list of phrases followed by their
   original starting index in the passed in list
     eg) ['hamsters', 'fight', 'off', 'predators', 
          'with', 'their', 'fierce', 'venom']
      returns
         ['fight_off', 1]
   """
   # phrases longer than this are dumb
   # i'd even say that phrases of length 4 are dumb
   max_phrase_length = 4
   low = 0
   high = max_phrase_length
   max = len(list)
   phrases = [] # stores phrases that appeared
   possible = [] # stores possible phrases
   for i in xrange(max-1):
      if high+i >= max:
         high = max-i
      possible.extend( addUnderscores( list[low+i:high+i] ) )
   # possible should now contain a list of adjacent
   # words from list with '_' between them
   synsets = wn.synsets
   poss_length = len(possible)
   for i in xrange(poss_length):
      if len(synsets( possible[i] )) > 0:
         phrases.append( possible[i] )
         # find where the phrase started
         if i == poss_length-1:
            phrases.append( max-2 )
         elif i in range(poss_length-max_phrase_length+1, poss_length-1):
            phrases.append( max-3 )
         else:
            phrases.append( i/(max_phrase_length-1) )
   return phrases

def removeDuplicates(dupes):
   """
   remove duplicates occuring in the input list
   """
   dupes.sort()
   d = {}
   for i in xrange(len(dupes)):
      # propagate the dictionary with word:count pairs
      if dupes[i] not in d:
         d[ dupes[i] ] = dupes.count( dupes[i] )
   k = iter(d)
   for k in d:
      for i in xrange(d[k]-1):
         dupes.remove( k )
         
def getSyns(word):
   """
   grab all synonyms for 'word' from wordnet
   return them in a list (w/ no duplicates)
   """
   synlist = []
   synsets = wn.synsets
   set = synsets(word)
   for i in xrange(len(set)):
      synlist.extend( set[i].lemma_names )
   removeDuplicates(synlist)
   ###replaceUnderscores(synlist)
   return synlist

class beliefSys:
   """
   Belief System (somewhat of a misnomer)
   sets up the bot's beliefs (stored in beliefs.txt)
   affects aggro based on how many times each word in the
   input occurs in the beliefs.
   """
   
   __file = 'beliefs.txt'
   __learnedfile = 'beliefs_learned.txt'
   stoplist = [
      'the', 'to', 'of', 'and', 'a', 'an', 'am',
      'in', 'that', 'or', 'but', 'is', 'be', 'are',
      'was', 'do', 'at', 'as', 'on', 'been', 'being',
      'than', 'then', 'were', 'oh', 'so', 'too',
      'uh', 'by', 'very', 'any', 'maybe', 'even',
      'only', 'um', 'hmm', 
   ]
   negatelist = [
      'not', 'don\'t', 'can\'t', 'won\'t', 'never',
      'haven\'t', 'cannot', 'isn\'t', 'wasn\'t', 'no',
   ]


   def __init__(self, aggroWords):
      # stores each line as a list seperated on
      # spaces and punctuation
      self._aggroWords = aggroWords # dictionary
      self._beliefs = []
      self._parseBeliefs()
      self._parseBeliefs(beliefSys.__learnedfile)


   # should not be called explicitly outside of class
   def _parseBeliefs(self, f=__file):
      """
      reads through beliefs file, stores each space seperated
      word into the _beliefs list.
      parses out (most) punctuation
      blank lines & lines beginning with '#' are ignored
      so: _beliefs =
         [
          ['word', 'word', 'word', ...],
          ...
         ]
      """
      try:
         beliefsFile = open(f, 'r')
         linenr = 0
         currlist = []
         while True:
            line = beliefsFile.readline()
            line = line.strip(' \t')
            if line == '':
               break # eof
            linenr += 1
            # uncomment below to echo back file as its read
            ##print repr(linenr)+':', repr(line)
            if line[0] == '#' or line[0] == '\n':
               continue
            self._addBelief(line)
         beliefsFile.close()
      except IOError:
         print f + ': cannot be opened'

   def _addBelief(self, string):
      """
      adds more beliefs into the belief structure
      ie: throws more strings into the _beliefs list
      """
      import re
      addthis = separate(string)
      if len(addthis) > 0:
         # check for phrases
         tmp = checkForPhrases(addthis)
         # replace the non underscored phrase with
         # the underscored one
         # eg: [...'fight','off'...] => [...'fight_off'...]
         for i in xrange(0, len(tmp), 2):
            length = len(re.split('[_]', tmp[i]))
            for j in xrange(length):
               addthis.pop(tmp[i+1])
            addthis.insert( tmp[i+1], tmp[i] )
         self._beliefs.append(addthis)

   def query(self, inStr):
      """
      returns a shift amount based on word frequency
      will only cause a shift if 'hamster' is in the input
      or if there is an intersection between the input and
      the aggro words
      """
      from sets import Set as set
      if type(inStr).__name__ != 'str':
         return 0
      # synlist = list of list of synonyms
      # each sub-list contains the synonyms for a word in the input
      synlist = []
      aggroWords = self._aggroWords
      words = separate(inStr, True)
      if len(words) == 0:
         return 0 # empty input
      w = set(words) # set containing all the input words
      a = set(aggroWords.keys()) # set containing every aggro word
      x = w.intersection(a) # the intersection of the two
      if 'hamster' not in words and len(x) == 0:
         # aggro a little bit if all the words are unfamiliar
         return 3
      from math import ceil
      shift = 0
      #if 'hamster' not in words:
      negcount = 0
      while len(x) > 0:
         word = x.pop()
         if word in beliefSys.negatelist:
            negcount += 1
         else:
            shift += aggroWords[ word ]
      if negcount%2 == 1: # not double neg => flip
         shift = -shift
      if 'hamster' in words:
         count_off_pcnt = .2
         # only go through beliefs if user input 'hamster' somewhere
         # only look to decrease
         for i in xrange(len(words)):
            ##synlist.append( getSyns(words[i]) ) # very strict?
            synlist.extend( getSyns(words[i]) ) # very lenient?
         browniepts = 0
         for i in xrange(len(self._beliefs)):
            belief = self._beliefs[i]
            # check word count between input and belief --
            # the closer the differnce is to 0, the better
            word_diff = abs( len(words) - len(belief) )
            good_range = ceil( count_off_pcnt * len(belief) )
            if word_diff in xrange(int(good_range)):
               # allow for matching only if off by count_off_pcnt%
               pts = 0 # add a '.0' to increase downshift amt
               mincount = min(len(words), len(belief))
               for j in xrange(mincount):
                  if belief[j] in words or belief[j] in synlist:
                     # try to match any belief word to any word
                     # contained in either the formatted input list
                     # or its synonym list (all synonyms for all words)
                     # -- if synlist is appended, then it only tries
                     # to match synonyms if the two words are in the
                     # same position in the statement
                     pts += 1
               # accumumlate deaggro amount for every belief
               browniepts += ceil( pts/mincount )
         shift -= browniepts
      # end if
      return shift

   def add(self, belief, f=__learnedfile):
      """
      appends new beliefs to beliefs file
      input should be a list of strings or a single string
      """
      typename = type(belief).__name__
      if (typename != 'list' and typename != 'str') \
         or len(belief) == 0:
         return None
      newbelief = ''
      if typename == 'str':
         # i can't think of what, if anything, should not
         # be added to the beliefs
         newbelief = belief
      else:
         newbelief = ' '.join(belief)
      try:
         beliefsFile = open(f, 'a')
      except IOError:
         beliefsFile = open(f, 'w')
      beliefsFile.write('\n' + newbelief)
      beliefsFile.close()
      # add new belief to _beliefs
      self._addBelief(newbelief)

