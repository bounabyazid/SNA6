#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 09:12:08 2019

@author: Yazid Bounab
"""

from nltk import pos_tag, word_tokenize
text = 'Google is a friend of Facebook and Yahoo shouts at Microsoft because Stackoverflow is giving out hats.'
text='amazon'
for word, pos in pos_tag(word_tokenize(text)):
    print (word, pos)