#!/usr/bin/python

iallagro=['you','your']
agro=['evil','bad','good','hamster']

import nltk
import re
from aggroMgr import *
from nltk.corpus import wordnet as wn

aggro = aggroMgr()

def inputs(sentence):
	sentence = sentence.strip()
	sets= ['',[],'']
	if(sentence==''):
		sets[2]='empty'
		return sets
	if(sentence[-1]!="."):
		sentence=sentence+"."
	hams=False
	agro=aggro.getwords()
	agro.extend(aggro.getnegates())
	sentences=re.split(r'\.|\?|!',sentence)
	t=0
	words=[]
	for word in sentences:
		words.append(re.split(r' |,|\"',word))
		t+=1
		if(t>1):
			sets[1].append([])
	if(len(sets[1])==0):
		sets[1].append([])
	if(len(words[0])==1 and words[0][0].lower()=='coprophagia'):
		sets[2]='safe'
		return sets
	if(len(words[0])==1 and words[0][0].lower()=='defenestration'):
		sets[2]='enrage'
		return sets
	if(len(wn.synsets(words[0][0]))!=0):
		if(wn.synsets(words[0][0])[0].definition=='an expression of greeting'):
			sets[2]='greeting'
       	sets[0]=sentence
	for word in words:
		for w in word:
			if (w.lower()=='hamster' or w.lower()=='hamsters'):
				hams=True
	t=0
	for word in words:
		for w in word:
			if w.lower()=='you' or w.lower()=='your' or w.lower()=="you're" or w.lower()=='harvey':
				sets[1][t].append(w)
		       	for ag in agro:
					if (hams==True and w.lower()==ag.lower()):
						sets[1][t].append(w)
		t+=1
	if(len(sets[2])==0):
		sets[2]='reflex'
	return sets
