#!/user/bin/python

##from thread import start_new_thread, allocate_lock
from threading import Thread, RLock
class aggroMgr(Thread):
   """
   Aggro manager class
   keeps track of aggro and changes it based on input
   """

   # member constants
   AGGRO_MIN_VALUE = 0   # happy
   AGGRO_MAX_VALUE = 100  # angry
   AGGRO_TIME_INTERVAL = 10
   AGGRO_COOLOFF_VALUE = 5
   NEUTRAL = 10
   UPSET = 30
   IRRITATED = 45
   FURIOUS = 60
   ENRAGED = 85

   __file = 'aggro.txt'


   # default constructor
   def __init__(self, t=AGGRO_TIME_INTERVAL):
      from beliefSys import beliefSys
      from os import sys
      import time
      # time() is not as precise as clock() on windows
      # the opposite seems true for unix, but we're
      # only concerned with seconds here
      # ie, it does not matter
      self._DEFAULT = aggroMgr.NEUTRAL
      self._last_input = time.time()
      self._time_int = t
      self._aggro = self._DEFAULT
      self._lock = RLock()
      self._aggroWords = {} # shouldn't be a per instance var
      self._parseAggroWds()
      self._beliefs = beliefSys(self._aggroWords)
      Thread.__init__(self)
      self.setDaemon(True)
      self.start()


   def _parseAggroWds(self):
      """
      reads through aggro file
      and propogates _aggroWords dictionary
      """
      try:
         aggroFile = open(aggroMgr.__file, 'r')
         linenr = 0
         while True:
            line = aggroFile.readline()
            line = line.strip(' \t')
            if line == '':
               break # eof
            linenr += 1
            if line[0] == '#' or line[0] == '\n':
               continue
            ##print repr(linenr)+':', repr(line)
            self._addAggroWd(line, linenr)
         aggroFile.close()
      except IOError:
         print aggroMgr.__file + ': cannot be opened'

   def _addAggroWd(self, string, linenr=-1):
      """
      helper function to propogate _aggroWords dictionary.
      checks for bad input.
      """
      from beliefSys import separate
      line = separate(string)
      if len(line) != 2:
         print aggroMgr.__file+'@'+repr(linenr)+': bad syntax'
         return None # lines should be 'word number'
      try:
         self._aggroWords[ line[0] ] = int(line[1])
      except ValueError:
         print aggroMgr.__file+'@'+repr(linenr) + ': invalid syntax'

   def addWord(self, word, value):
      """
      appends passed in word to aggro file.
      inputs should be a string and int, respectively
      """
      # check for spaces in word...
      #  dunno if aggro should change on phrases
      if ' ' in word or type(value).__name__ != 'int':
         return None
      try:
         aggroFile = open(aggroMgr.__file, 'a')
         newword = word + ' ' + repr(value)
         aggroFile.write('\n' + newword)
         aggroFile.close()
         ## add new word to _aggroWords
         self._addAggroWd(newword)
      except IOError:
         print aggroMgr.__file + ': cannot be opened'
         
   def stop(self):
      """
      stops the aggroMgr's thread
      """
      self._Thread__stop()

   # gravitate towards neutral aggro over time
   # inherited from Thread, called from start()
   ##### SHOULD NOT BE CALLED MANUALLY #####
   def run(self):     
      from time import time as time, sleep as sleep
      while True:
         sleep(self._time_int)
         if time()-self._last_input > self._time_int*2:
            # it has been over 2x _time_int since last time
            # shift() was called -- cooldown to default aggro in steps
            if self._lock.acquire(False):
               # not locked
               default = self._DEFAULT
               aggro = self._aggro # supposedly thread safe
               try:
                  if aggro > default: # angry
                     if aggro-aggroMgr.AGGRO_COOLOFF_VALUE < default:
                        self._aggro = default
                     else:
                        self._aggro -= aggroMgr.AGGRO_COOLOFF_VALUE
                  elif aggro < default: # happy
                     if aggro+aggroMgr.AGGRO_COOLOFF_VALUE > default:
                        self._aggro = default
                     else:
                        self._aggro += aggroMgr.AGGRO_COOLOFF_VALUE
               finally:
                  self._lock.release()
               # print "aggro cooled down!"
            # else: # for debugging
               # print "aggroMgr cooloff locked & restarting"
         if not self.isAlive():
            break
      # restart thread...
      # not sure if this will crash if too many threads are created
      # Thread.__init__(self)
      # self.setDaemon(True)
      # self.start()
      
   def _shiftAggroWds(self, inputs):
      """
      iterate through each sentence containing aggro words
      """
      from beliefSys import beliefSys as bs
      delta = 0
      aggroWords = self._aggroWords
      name = type(inputs).__name__
      if name == 'str':
         # only one aggro word
         if inputs in aggroWords:
            delta += aggroWords[inputs]
      elif name == 'list':
         for i in xrange(len(inputs)):            
            negcount = 0
            sentence = inputs[i]
            # iterate through each word
            for j in xrange(len(sentence)):               
               # no word should be in both
               if sentence[j] in bs.negatelist:
                  negcount += 1
               elif sentence[j] in aggroWords:
                  delta += aggroWords[ sentence[j] ]
            if negcount%2 == 1:
               # not double negative
               delta = -delta
      return delta

   def shift(self, inputs):
      """
      changes the "private" aggro value
      inputs = [
                 inputStr,
                 [[ag wd, ag wd, ag wd, ...],[...],...],
                 actionStr
               ]
      """
      try:
         if type(inputs).__name__ != 'list' \
            or type(inputs[0]).__name__ != 'str' \
            or type(inputs[1]).__name__ != 'list' \
            or type(inputs[2]).__name__ != 'str':
            return None
      except IndexError:
         return None
      if inputs[2].lower() == 'safe': # safe word entered
         self._lock.acquire()
         try:
            self._aggro = aggroMgr._DEFAULT
         finally:
            self._lock.release()
      elif inputs[2].lower() == 'enrage': # insta anger word
         self._lock.acquire()
         try:
            self._aggro = aggroMgr.ENRAGED
         finally:
            self._lock.release()
      else: # normal shift
         beliefs = self._beliefs
         aggroWords = self._aggroWords
         delta = 0
         if self.query() == 0:
            # if bot is "happy", believe anything that's not a question
            # and has hamster in it. don't bother with beliefs if happy
            from beliefSys import separate as sep
            if '?' not in inputs[0] \
               and 'hamster' in sep(inputs[0], True):
               beliefs.add(inputs[0])
         else:
            delta = beliefs.query(inputs[0])
         delta += self._shiftAggroWds(inputs[1])
         from time import time as time
         self._lock.acquire() # wait until run() finishes writing
         try:
            aggro = self._aggro
            if aggro+delta <= aggroMgr.AGGRO_MIN_VALUE:
               self._aggro = aggroMgr.AGGRO_MIN_VALUE
            elif aggro+delta >= aggroMgr.AGGRO_MAX_VALUE:
               self._aggro = aggroMgr.AGGRO_MAX_VALUE
            else:
               self._aggro += delta
            # set time to reflect that input was just received
            # so that it doesn't cooloff
            self._last_input = time()
         finally:
            self._lock.release()
   
   def getwords(self):
      """
      get the list of aggro words
      """
      return self._aggroWords.keys()
      
   def getnegates(self):
      """
      get the list of negation words
      """
      from beliefSys import beliefSys as bs
      return bs.negatelist

   # gets anger level
   # returns 1-5
   def query(self):
      """
      returns anger level value - ranges from 0-5
      """
      aggro = -1
      # i hear accessing is thread safe.. but im not sure
      self._lock.acquire()
      try:
         aggro = self._aggro
      finally:
         self._lock.release()
      if aggroMgr.AGGRO_MIN_VALUE <= aggro and aggro < aggroMgr.NEUTRAL:
         return 0
      elif aggroMgr.NEUTRAL <= aggro and aggro < aggroMgr.UPSET:
         return 1
      elif aggroMgr.UPSET <= aggro and aggro < aggroMgr.IRRITATED:
         return 2
      elif aggroMgr.IRRITATED <= aggro and aggro < aggroMgr.FURIOUS:
         return 3
      elif aggroMgr.FURIOUS <= aggro and aggro < aggroMgr.ENRAGED:
         return 4
      elif aggroMgr.ENRAGED <= aggro:
         return 5
      
      
