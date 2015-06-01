# -*- coding: utf-8 -*-
'''
Created on May 27, 2015

@author: root
'''
import sys
reload(sys)
sys.setdefaultencoding('utf-8')  # @UndefinedVariable

import gensim



STOP_WORDS_PATH='../data/stop.txt'
stopword_list=[]

def load_stopword(path=STOP_WORDS_PATH):
	word_list = []
	with open(path, 'r') as fr:
		for i in fr.readlines():
			word_list.append(i)
	return word_list


